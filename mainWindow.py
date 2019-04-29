#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from data_source import *
#from data_source_actuall import *
from data_source_historical import *
from data_source_suspicious import *
import re
import multiprocessing
import plot
from repeater import TimedScraper

def getData(data):
    list1=data.get_data_just_names_and_dates()
    listToShow=[]
    for i in list1:
            tmp=data.get_parametr_data_new(i[0], i[1], i[2])
            listToShow.append(tmp)
    return listToShow


def sortByDate(data):
    list1=data.get_data_just_names_and_dates_sort_by_date()
    listToShow=[]
    for i in list1:
        tmp = data.get_parametr_data_new(i[0], i[1], i[2])
        listToShow.append(tmp)
    return listToShow

def sortByPrice(data):
    list1=data.get_data_just_names_and_dates()
    listToShow=[]
    for i in list1:
            tmp = data.get_parametr_data_new(i[0], i[1], i[2])

            k=0
            for j in listToShow:
                print (j)
                if j[6]!=None and tmp[6]!=None:#gdy mozliwe remisy
                    if max(j[4], j[5],j[6]) < max(tmp[4], tmp[5],tmp[6]):
                        break
                elif j[6]==None and tmp[6]==None:
                    if max(j[4], j[5]) < max(tmp[4], tmp[5]):
                        break
                elif j[6]==None:
                    if max(j[4], j[5]) < max(tmp[4], tmp[5], tmp[6]):
                        break
                else:
                    if max(j[4], j[5], j[6]) < max(tmp[4], tmp[5]):
                        break
                k=k+1
            listToShow.insert(k,tmp)
    return listToShow






class mainWindow(QWidget):
    th = TimedScraper()
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFixedSize(900,600)
        self.interfejs()

    def addCall(self):
        AddWindow(self)

    def interfejs(self):

        layoutA=QVBoxLayout()


    # Napis glowny
        title=QLabel("APLIKACJA BUKMACHERSKA", self)
        title.setFixedSize(980,40)
        title.setAlignment(QtCore.Qt.AlignCenter)

        font = QFont()
        font.setPointSize(16)
        font.setWeight(80)
        title.setFont(font)
        layoutA.addWidget(title)

        # przyciski
        DodajBtn = QPushButton("Dodaj mecz", self)
        DodajBtn.setMaximumWidth(200)
        DodajBtn.setStyleSheet("font: bold; color: dark blue; background-color: white; border-color: beige")
        DodajBtn.clicked.connect(self.addCall)
        koniecBtn = QPushButton("Zakończ", self)
        koniecBtn.setMaximumWidth(200)
        koniecBtn.setStyleSheet("font: bold;color: dark blue; background-color: white; border-color: beige")
        koniecBtn.clicked.connect(QApplication.instance().quit)
        OdswiezBtn = QPushButton("Odśwież widok", self)
        OdswiezBtn.setMaximumWidth(200)
        OdswiezBtn.setStyleSheet("font: bold; color: dark blue; background-color: white; border-color: beige")
        OdswiezBtn.clicked.connect(self.refresh)

        inputImg = QImage("data/logo.jpeg")
        imgDisplayLabel = QLabel()
        imgDisplayLabel.setPixmap(QPixmap.fromImage(inputImg))
        imgDisplayLabel.setScaledContents(True)
        imgDisplayLabel.setFixedSize(200, 150)

        btnGroup = QVBoxLayout()
        btnGroup.addWidget(DodajBtn)
        btnGroup.addWidget(OdswiezBtn)
        btnGroup.addWidget(koniecBtn)
        btnGroup.setSpacing(0)

        gridLayout=QGridLayout()
        gridLayout.addWidget(imgDisplayLabel, 0,2)
        gridLayout.addLayout(btnGroup, 0,0)
        gridLayout.setColumnStretch(1, -2)
        layoutA.addLayout(gridLayout)

        tab_widget = QTabWidget()
        self.actual=MyTab("Aktualne")
        self.historical=MyTab("Historyczne")
        self.suspicious=MyTab("Podejrzane")
        tab_widget.addTab(self.actual, "Aktualne")
        tab_widget.addTab(self.suspicious, "Podejrzane")
        tab_widget.addTab(self.historical, "Historyczne")
        layoutA.addWidget( tab_widget)
        #layoutA.addLayout(layoutB)
        self.setLayout(layoutA)


        #self.setGeometry(20, 20, 850, 600)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 165, 0))
        self.setPalette(p)
        self.setWindowTitle("Aplikacja bukmacherska")
        self.show()

    def refresh(self):
        self.actual.table_model.selectionchange(0)
        self.suspicious.table_model.selectionchange(0)
        self.historical.table_model.selectionchange(0)


class ResultCell(QWidget):

    def __init__(self, table, i, name):
        super().__init__()
        self.index=i
        self.table=table
        self.name=name
        self.result1=QLineEdit()
        self.result2=QLineEdit()
        colon=QLabel(":")
        self.result1.setMaxLength(4)
        self.result1.setValidator(QIntValidator(0, 1000))
        self.result2.setMaxLength(4)
        self.result2.setValidator(QIntValidator(0, 1000))
        self.result2.returnPressed.connect(self.onPressed)
        self.result1.returnPressed.connect(self.onPressed)
        layout3=QHBoxLayout()
        layout3.addWidget(self.result1)
        layout3.addWidget(colon)
        layout3.addWidget(self.result2)
        self.setLayout(layout3)
        self.setFixedSize(100,40)
        self.show()

    def onPressed(self):
        if (self.result1.text()==""):
            SmallMessageWindow("brak")

            return
        if (self.result2.text()==""):
            SmallMessageWindow("brak")
            return
        else:
            SmallMessageWindow("ok")
            result = (self.table.mylist[self.index][0], self.table.mylist[self.index][2], self.table.mylist[self.index][3], self.result1.text(), self.result2.text())
            if self.name=="a":
                mainWindow.th.a.insert_result(result)
            if self.name=="h":
                mainWindow.th.h.insert_result(result)
            if self.name=="s":
                mainWindow.th.s.insert_result(result)

class Check(QWidget):
    def __init__(self, table, i, name):
        super().__init__()
        self.index=i
        self.table=table
        self.name=name
        self.box=QCheckBox("", self)
        self.box.stateChanged.connect(self.clickBox)
        #self.box.setGeometry(30,30,20,20)
        layout3=QVBoxLayout()
        layout3.addWidget(self.box)
        self.setLayout(layout3)
        self.show()

    def clickBox(self):
        RemoveWindow(self)

class RemoveWindow(QDialog):
    def __init__(self, p):
        super().__init__()
        self.parent=p
        self.delete()

    def delete(self):
        self.setWindowTitle("Usuń mecz")
        self.setWindowModality(Qt.ApplicationModal)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 165, 0))
        self.setPalette(p)

        layout4 = QVBoxLayout()
        okBtn = QPushButton("USUŃ")
        anulujBtn = QPushButton("ANULUJ")
        self.wpisz1 = QLineEdit()
        self.wpisz2 = QLineEdit()
        tekst1 = QLabel("Czy na pewno chcesz usunąć mecz?")
        layout4.addWidget(tekst1)
        layout4.addWidget(okBtn)
        layout4.addWidget(anulujBtn)
        buttonBox = QDialogButtonBox()
        okBtn.clicked.connect(self.remove)
        anulujBtn.clicked.connect(self.close)
        layout4.addWidget(buttonBox)
        self.setLayout(layout4)
        self.exec_()

    def remove(self):
        result = (self.parent.table.mylist[self.parent.index][2], self.parent.table.mylist[self.parent.index][3], self.parent.table.mylist[self.parent.index][0])
        if self.parent.name == "a":
            mainWindow.th.a.delete_specific_data(result[0], result[1], result[2])
        if self.parent.name == "h":
            mainWindow.th.h.delete_specific_data(result[0], result[1], result[2])
        if self.parent.name == "s":
            mainWindow.th.s.delete_specific_data(result[0], result[1], result[2])
        msg=QMessageBox()
        msg.setWindowTitle("Komunikat")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Mecz został usunięty")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
        self.close()

class MyTab(QWidget):
    def __init__(self, name):
        super().__init__()
        self.setWindowTitle(name)
        self.table_view=QTableView()
        self.table=self.AddTable(name)
        layout2=QVBoxLayout()
        sort_text=QLabel("Sortuj według: ")
        cb = QComboBox()
        cb.addItems(["Data dodania zakładu", "Data rozgrywki", "Kwota zakładu"])
        cb.currentIndexChanged.connect(self.table_model.selectionchange)
        layout2.addWidget(sort_text)
        layout2.addWidget(cb)
        layout2.addWidget(self.table_view)
        self.setLayout(layout2)

    def AddTable(self, name):
        self.table_model=MyTableModel(name, self)
        self.table_view.setModel(self.table_model)
        self.AddColumn7_8_9()
        self.table_view.setColumnWidth(2,70)
        self.table_view.setColumnWidth(1, 90)
        self.table_view.setMinimumWidth(1)
        self.table_view.setColumnWidth(6, 50)
        self.table_view.setColumnWidth(5, 80)
        self.table_view.setColumnWidth(7, 80)
        self.table_view.setColumnWidth(0, 75)


    def AddColumn7_8_9(self):
        ile=self.table_model.rowCount(self)
        for i in range(0, ile):
            self.table_view.setIndexWidget(self.table_model.index(i, 9), ShowButton(i,self.table_model) )
            self.table_view.setIndexWidget(self.table_model.index(i, 8), ResultCell(self.table_model, i, self.table_model.name))
            self.table_view.setIndexWidget(self.table_model.index(i,0), Check(self.table_model, i, self.table_model.name))


class ShowButton(QPushButton):
    def __init__(self,id,table):
        super(ShowButton,self).__init__("Pokaż wykres")
        self.setStyleSheet("background-color: beige;border-color: beige")
        self.id = id
        self.table = table
        self.clicked.connect(self.showPlot )
        

    def showPlot(self):
        Args=( self.table.mylist[self.id][0], self.table.mylist[self.id][2], self.table.mylist[self.id][3])
        multiprocessing.Process(target=Plot , args=Args , daemon=True).start()
        

class MyTableModel(QAbstractTableModel):

    def __init__(self, name, parent):
        super().__init__()
        self.mylist=[]
        self.parent=parent
        self.name=""
        
        if (name=="Aktualne"):
            self.name="a"
            self.mylist=getData(mainWindow.th.a)
        if (name=="Historyczne"):
            self.name="h"
            self.mylist=getData(mainWindow.th.h)
        if (name=="Podejrzane"):
            self.name="s"
            self.mylist=getData(mainWindow.th.s)

    def rowCount(self,parent):
        return len(self.mylist)

    def columnCount(self,parent):
        return 10


    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.column()==8:
                return ""
            if index.column()==9:
                return ""
            if index.column()==0:
                return  ""
            if index.column() == 6:
                return self.mylist[index.row()][7]
            if index.column() == 7:
                return self.mylist[index.row()][6]
            return self.mylist[index.row()][index.column()-1]
        return None

    def headerData(self, column, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal:
            if column==1:
                return QtCore.QVariant('Data')
            if column==2:
                return QtCore.QVariant('Godzina')
            if column==3:
                return QtCore.QVariant('Drużyna 1')
            if column==4:
                return QtCore.QVariant('Drużyna 2')
            if column==5:
                return QtCore.QVariant('Wygrana 1')
            if column==6:
                return QtCore.QVariant('X')
            if column==7:
                return QtCore.QVariant('Wygrana 2')
            if column==8:
                return QtCore.QVariant('Wynik meczu')
            if column==9:
                return QtCore.QVariant('Pokaż wykres')
            if column==0:
                return QtCore.QVariant("Usuń")


    def selectionchange(self, i):
            self.beginResetModel()
            self.mylist=[]
            self.endResetModel()
            if (i == 0):
                if self.name=="a":
                    self.mylist=getData(mainWindow.th.a)
                if self.name == "h":
                    self.mylist=getData(mainWindow.th.h)
                if self.name == "s":
                    self.mylist=getData(mainWindow.th.s)
            if (i == 1):
                if self.name == "a":
                    self.mylist = sortByDate(mainWindow.th.a)
                if self.name == "h":
                    self.mylist = sortByDate(mainWindow.th.h)
                if self.name == "s":
                    self.mylist = sortByDate(mainWindow.th.s)
            if (i == 2):
                if self.name == "a":
                    self.mylist = sortByPrice(mainWindow.th.a)
                if self.name == "h":
                        self.mylist = sortByPrice(mainWindow.th.h)
                if self.name == "s":
                    self.mylist = sortByPrice(mainWindow.th.s)
            self.parent.AddColumn7_8_9()


class Plot():
    def __init__(self,date,home,away):
        #super().__init__()
        self.date = date
        self.home = home
        self.away = away
        self.makePlot()
        #self.dodaj()
        
    def makePlot(self):
        #print( dir(self.table) )
        #print(self.table)
        #print ("Rysuje wykres dla danych " , self.date ,self.home , self.away)
        betData = mainWindow.th.a.get_all_BetValues(self.home,self.away,self.date)
        if len(betData) > 0:
            if len( betData[0] ) == 3:
                winH = list ( map (lambda x : x[0] ,betData) )
                remisX = list ( map (lambda x : x[1] ,betData) )
                winA = list ( map (lambda x : x[2] ,betData) )
                plot.create_plot(self.home , self.away ,winH , winA , remisX )
            elif len( betData[0] ) == 2:
                winH = list ( map (lambda x : x[0] ,betData) )
                winA = list ( map (lambda x : x[1] ,betData) )
                plot.create_plot(self.home , self.away ,winH , winA  )


    def dodaj(self):
        self.setWindowTitle("Wykres kursów")
        self.setWindowModality(Qt.ApplicationModal)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 165, 0))
        self.setPalette(p)
        self.makePlot()
        self.exec()




class AddWindow(QDialog):
    def __init__(self,upperWindow):
        super().__init__()
        self.upperWindow = upperWindow
        self.dodajView()
        
    def dodajView(self):


        self.setWindowTitle("Dodaj zakład")
        self.setWindowModality(Qt.ApplicationModal)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 165, 0))
        self.setPalette(p)

        layout1 = QVBoxLayout()
        okBtn = QPushButton("DODAJ")
        anulujBtn = QPushButton("ANULUJ")
        self.wpisz1 = QLineEdit()
        self.wpisz2 = QLineEdit()
        tekst1 = QLabel("Podaj link:")
        tekst2 = QLabel("Podaj czas aktualizacji:")
        layout1.addWidget(tekst1)
        layout1.addWidget(self.wpisz1)
        layout1.addWidget(tekst2)
        layout1.addWidget(self.wpisz2)
        layout1.addWidget(okBtn)
        layout1.addWidget(anulujBtn)
        buttonBox = QDialogButtonBox()
        okBtn.clicked.connect(self.add)
        anulujBtn.clicked.connect(self.close)
        layout1.addWidget(buttonBox)
        self.setLayout(layout1)
        self.exec_()

    def add(self):
        a=self.wpisz1.text()
        b=self.wpisz2.text()
        if a=="" or b=="":
            MessageWindow("brak")
        elif not self.checkTime(b):
            MessageWindow("czas")
        else:
            MessageWindow("ok")
            url=re.sub('\'','',self.wpisz1.text())
            interval = int(self.wpisz2.text())
            self.upperWindow.th.add( url , interval  )
            
            self.close()

    def checkTime(self, b):
        return  b.isdigit() and 121 > int(b) > 1
        

class MessageWindow(QMessageBox):
    def __init__(self, str):
        super().__init__()
        self.show(str)

    def show(self,str):
        msg= QMessageBox()
        msg.setWindowTitle("Komunikat")
        if str=="brak":
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Uzupełnij wszystkie pola")
            msg.setInformativeText("Mecz nie został dodany")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        if str=="czas":
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Niepoprawne dane w polu czas")
            msg.setInformativeText("Wpisz liczbę z przedziału 2-120")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        if str=="ok":
            msg.setIcon(QMessageBox.Information)
            msg.setText("Mecz został dodany")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

class SmallMessageWindow(QMessageBox):
    def __init__(self, str):
        super().__init__()
        self.show(str)

    def show(self,str):
        msg= QMessageBox()
        msg.setWindowTitle("Komunikat")
        if str=="brak":
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Uzupełnij wszystkie pola")
            msg.setInformativeText("Wynik nie został zapisany")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        if str=="ok":
            msg.setIcon(QMessageBox.Information)
            msg.setText("Wynik został zapisany")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    #a = DataSourceActuall()
    #h = DataSourceHistorical()
    #s = DataSourceSuspicious()
    okno = mainWindow()
    sys.exit(app.exec_())
    