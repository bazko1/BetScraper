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

global okno

def getData(data):
    list1=data.get_data_just_names_and_dates()
    listToShow=[]
    for i in list1:
            tmp=data.get_parametr_data_new(i[0], i[1], i[2])
            listToShow.append(tmp)
    return listToShow

#sortowanie wg daty meczu rosnaco
def sortByDate(data):
    list1=data.get_data_just_names_and_dates_sort_by_date()
    listToShow=[]
    for i in list1:
        tmp = data.get_parametr_data_new(i[0], i[1], i[2])
        listToShow.append(tmp)
    return listToShow

#sortowanie wg kwoty zakladu od najwiekszego
def sortByPrice(data):
    list1=data.get_data_just_names_and_dates()
    listToShow=[]
    for i in list1:
            tmp = data.get_parametr_data_new(i[0], i[1], i[2])

            k=0
            for j in listToShow:
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






class MainWindow(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(900,600)
        self.th = TimedScraper()
        self.interfejs()

    def addCall(self):
        AddWindow(self)

    def interfejs(self):
        layoutA=QVBoxLayout()


    # Napis glowny
        title=QLabel("APLIKACJA BUKMACHERSKA", self)
        title.setFixedSize(880,40)
        title.setAlignment(QtCore.Qt.AlignCenter)

        font = QFont()
        font.setPointSize(16)
        font.setWeight(80)
        title.setFont(font)
        layoutA.addWidget(title)

    # Przyciski
        dodajBtn = QPushButton("Dodaj mecz", self)
        dodajBtn.setMaximumWidth(200)
        dodajBtn.setStyleSheet("font: bold; color: dark blue; background-color: white; border-color: beige")
        dodajBtn.clicked.connect(self.addCall)

        koniecBtn = QPushButton("Zakończ", self)
        koniecBtn.setMaximumWidth(200)
        koniecBtn.setStyleSheet("font: bold;color: dark blue; background-color: white; border-color: beige")
        koniecBtn.clicked.connect(QApplication.instance().quit)

        odswiezBtn = QPushButton("Odśwież widok", self)
        odswiezBtn.setMaximumWidth(200)
        odswiezBtn.setStyleSheet("font: bold; color: dark blue; background-color: white; border-color: beige")
        odswiezBtn.clicked.connect(self.refresh)

        mailBtn = QPushButton("Dodaj email", self)
        mailBtn.setMaximumWidth(200)
        mailBtn.setStyleSheet("font: bold; color: dark blue; background-color: white; border-color: beige")
        mailBtn.clicked.connect(self.addMail)


        btnGroup = QVBoxLayout()
        btnGroup.addWidget(dodajBtn)
        btnGroup.addWidget(odswiezBtn)
        btnGroup.addWidget(mailBtn)
        btnGroup.addWidget(koniecBtn)
        btnGroup.setSpacing(0)

    #Obrazek-logo STS

        inputImg = QImage("data/logo.jpeg")
        imgDisplayLabel = QLabel()
        imgDisplayLabel.setPixmap(QPixmap.fromImage(inputImg))
        imgDisplayLabel.setScaledContents(True)
        imgDisplayLabel.setFixedSize(200, 150)



        gridLayout=QGridLayout()
        gridLayout.addWidget(imgDisplayLabel, 0,2)
        gridLayout.addLayout(btnGroup, 0,0)
        gridLayout.setColumnStretch(1, -2)
        layoutA.addLayout(gridLayout)

    #Zakładki
        tab_widget = QTabWidget()
        self.actual=MyTab("Aktualne",self)
        self.historical=MyTab("Historyczne",self)
        self.suspicious=MyTab("Podejrzane",self)
        tab_widget.addTab(self.actual, "Aktualne")
        tab_widget.addTab(self.suspicious, "Podejrzane")
        tab_widget.addTab(self.historical, "Historyczne")
        layoutA.addWidget( tab_widget)
        self.setLayout(layoutA)


        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 165, 0))
        self.setPalette(p)
        self.setWindowTitle("Aplikacja bukmacherska")
        self.setWindowIcon(QIcon('data/logo.jpeg'))
        self.show()

    def refresh(self):
        self.actual.table_model.selectionchange(0)
        self.suspicious.table_model.selectionchange(0)
        self.historical.table_model.selectionchange(0)
    
    def addMail(self):
        def handleEmailText():
            #TODO: Add check if it looks like email
            email = wpisz1.text()
            if email == "":
                MessageWindow("mailFAILURE")    
            else:
                self.th.ud.addEmail(email)
                MessageWindow("mailOK")
                dialog.close()
            
            
    
        dialog = QDialog()
        dialog.setWindowTitle("Dodaj email")
        dialog.setWindowModality(Qt.ApplicationModal)
        p = dialog.palette()
        p.setColor(dialog.backgroundRole(), QColor(255, 165, 0))
        dialog.setPalette(p)
        layout1 = QVBoxLayout()
        okBtn = QPushButton("DODAJ")
        anulujBtn = QPushButton("ANULUJ")
        wpisz1 = QLineEdit()
        tekst1 = QLabel("Podaj email:")
        layout1.addWidget(tekst1)
        layout1.addWidget(wpisz1)
        layout1.addWidget(okBtn)
        layout1.addWidget(anulujBtn)
        buttonBox = QDialogButtonBox()
        okBtn.clicked.connect( handleEmailText )
        anulujBtn.clicked.connect(dialog.close)
        layout1.addWidget(buttonBox)
        dialog.setLayout(layout1)
        dialog.exec_()
        pass


#Pole do wpisania wyniku
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
            MessageWindow("brak2")
            return
        if (self.result2.text()==""):
            MessageWindow("brak2")
            return
        else:
            MessageWindow("ok2")
            result = (self.table.mylist[self.index][0], self.table.mylist[self.index][2], self.table.mylist[self.index][3], self.result1.text(), self.result2.text())
            if self.name=="a":
                okno.th.a.insert_result(result)
            if self.name=="h":
                okno.th.h.insert_result(result)
            if self.name=="s":
                okno.th.s.insert_result(result)

#Pole 'Usun' w tablicach z meczami
class Check(QWidget):
    def __init__(self, table, i, name):
        super().__init__()
        self.index=i
        self.table=table
        self.name=name
        self.box=QCheckBox("", self)
        self.box.stateChanged.connect(self.clickBox)
        layout3=QVBoxLayout()
        layout3.addWidget(self.box)
        self.setLayout(layout3)
        self.show()

    def clickBox(self):
        RemoveWindow(self)

#Okienko z informacja przy usuwaniu meczu
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
            #remove from refresh list
            okno.th.removeFromQueue(result[0],result[1],result[2])
            #remove from database
            okno.th.a.delete_specific_data(result[0], result[1], result[2])
        if self.parent.name == "h":
            okno.th.h.delete_specific_data(result[0], result[1], result[2])
        if self.parent.name == "s":
            okno.th.removeFromQueue(result[0],result[1],result[2])
            okno.th.s.delete_specific_data(result[0], result[1], result[2])
        MessageWindow("usun")
        self.close()

#Zakładki 'Aktualne', 'Podejrzane', 'Historyczne'
class MyTab(QWidget):
    def __init__(self, name,parent):
        super().__init__()
        self.th = parent.th
        self.setWindowTitle(name)
        self.table_view=QTableView()
        self.table=self.addTable(name)
        self.layout2=QVBoxLayout()
        sort_text=QLabel("Sortuj według: ")
        cb = QComboBox()
        cb.addItems(["Data dodania zakładu", "Data rozgrywki", "Kwota zakładu"])
        cb.currentIndexChanged.connect(self.table_model.selectionchange)
        self.layout2.addWidget(sort_text)
        self.layout2.addWidget(cb)
        self.layout2.addWidget(self.table_view)
        self.checkIsEmpty(name)
        self.setLayout(self.layout2)

    def checkIsEmpty(self, name):
        if self.table_model.rowCount(self) == 0 and self.layout2.count()==3:
            if name=="Aktualne":
                self.info=QLabel("Brak aktualnych meczów")
            if name=="Historyczne":
                self.info=QLabel("Brak historycznych meczów")
            if name=="Podejrzane":
                self.info=QLabel("Brak podejrzanych meczów")
            self.layout2.addWidget(self.info)
        elif self.layout2.count()==4 and self.table_model.rowCount(self)!=0:
                self.layout2.itemAt(3).widget().deleteLater()

    def addTable(self, name):
        self.table_model=MyTableModel(name, self)
        self.table_view.setModel(self.table_model)
        self.addColumn0_8_9()
        self.table_view.setColumnWidth(2,70)
        self.table_view.setColumnWidth(1, 90)
        self.table_view.setMinimumWidth(1)
        self.table_view.setColumnWidth(6, 50)
        self.table_view.setColumnWidth(5, 80)
        self.table_view.setColumnWidth(7, 80)
        self.table_view.setColumnWidth(0, 75)


    def addColumn0_8_9(self):
        ile=self.table_model.rowCount(self)
        for i in range(0, ile):
            self.table_view.setIndexWidget(self.table_model.index(i, 9), ShowButton(i,self.table_model,self.th) )
            self.table_view.setIndexWidget(self.table_model.index(i, 8), ResultCell(self.table_model, i, self.table_model.name))
            self.table_view.setIndexWidget(self.table_model.index(i,0), Check(self.table_model, i, self.table_model.name))

    def showInfo(self):
        self.inf=QWidget()
        layout=QVBoxLayout()
        self.info = QLabel("Brak aktualnych meczów")
        layout.addWidget(self.info)
        self.inf.setLayout(layout)
        self.inf.show()

#Przycisk 'Pokaz wykres'
class ShowButton(QPushButton):
    def __init__(self,id,table,th):
        super(ShowButton,self).__init__("Pokaż wykres")
        self.setStyleSheet("background-color: beige;border-color: beige")
        self.id = id
        self.table = table
        self.th = th
        self.clicked.connect(self.showPlot )
        

    def showPlot(self):
        date,home,away = self.table.mylist[self.id][0], self.table.mylist[self.id][2], self.table.mylist[self.id][3]
        betData = self.th.a.get_all_BetValues(home,away,date)
        dbResult = self.th.a.get_result(home,away,date)
        Args=(home,away,betData,dbResult)
        multiprocessing.Process(target=Plot , args=Args , daemon=True).start()
        

class MyTableModel(QAbstractTableModel):

    def __init__(self, name, parent):
        super().__init__()
        self.mylist=[]
        self.parent=parent
        self.name=""
        
        if (name=="Aktualne"):
            self.name="a"
            self.mylist=getData(parent.th.a)
        if (name=="Historyczne"):
            self.name="h"
            self.mylist=getData(parent.th.h)
        if (name=="Podejrzane"):
            self.name="s"
            self.mylist=getData(parent.th.s)

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
                return self.mylist[index.row()][6]
            if index.column() == 7:
                return self.mylist[index.row()][5]
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

    #zmiana kryteriow sortowania
    def selectionchange(self, i):
            self.beginResetModel()
            self.mylist=[]
            self.endResetModel()
            if (i == 0):
                if self.name=="a":
                    self.mylist=getData(okno.th.a)
                    self.parent.checkIsEmpty("Aktualne")
                if self.name == "h":
                    self.mylist=getData(okno.th.h)
                    self.parent.checkIsEmpty("Historyczne")
                if self.name == "s":
                    self.mylist=getData(okno.th.s)
                    self.parent.checkIsEmpty("Podejrzane")
            if (i == 1):
                if self.name == "a":
                    self.mylist = sortByDate(okno.th.a)
                    self.parent.checkIsEmpty("Aktualne")
                if self.name == "h":
                    self.mylist = sortByDate(okno.th.h)
                    self.parent.checkIsEmpty("Historyczne")
                if self.name == "s":
                    self.mylist = sortByDate(okno.th.s)
                    self.parent.checkIsEmpty("Podejrzane")
            if (i == 2):
                if self.name == "a":
                    self.mylist = sortByPrice(okno.th.a)
                    self.parent.checkIsEmpty("Aktualne")
                if self.name == "h":
                    self.mylist = sortByPrice(okno.th.h)
                    self.parent.checkIsEmpty("Historyczne")
                if self.name == "s":
                    self.mylist = sortByPrice(okno.th.s)
                    self.parent.checkIsEmpty("Podejrzane")
            self.parent.addColumn0_8_9()

#Okienko z wykresem
class Plot():
    def __init__(self,home,away,betData,dbResult):
        self.makePlot(home,away,betData,dbResult)

    def makePlot(self,home,away,betData,dbResult):
        if len(betData) > 0:
            if len( betData[0] ) == 3 and not None in betData[0]:
                winH = list ( map (lambda x : x[0] ,betData) )
                remisX = list ( map (lambda x : x[2] ,betData) )
                winA = list ( map (lambda x : x[1] ,betData) )
                plot.create_plot(home , away ,winH , winA , remisX , result=dbResult )
            elif len( betData[0] ) == 2 or None in betData[0]:
                winH = list ( map (lambda x : x[0] ,betData) )
                winA = list ( map (lambda x : x[1] ,betData) )
                plot.create_plot(home , away ,winH , winA ,result=dbResult  )
            




class AddWindow(QDialog):
    def __init__(self,upperWindow):
        super().__init__()
        self.upperWindow = upperWindow
        self.addView()
        
    def addView(self):
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
        okBtn.clicked.connect(self.checkInputData)
        anulujBtn.clicked.connect(self.close)
        layout1.addWidget(buttonBox)
        self.setLayout(layout1)
        self.exec_()

    def checkInputData(self):
        a=self.wpisz1.text()
        b=self.wpisz2.text()
        if a=="" or b=="":
            MessageWindow("brak1")
        elif not self.checkTime(b):
            MessageWindow("czas")
        else:
            url=re.sub('\'','',self.wpisz1.text())
            interval = int(self.wpisz2.text())
            result=self.upperWindow.th.add( url , interval  )
            if result=="Error":
                MessageWindow("link")
            else:
                MessageWindow("ok1")
                self.close()

    def checkTime(self, b):
        return  b.isdigit() and 121 > int(b) > 1
        
#Okienka z komunikatem
class MessageWindow(QMessageBox):
    def __init__(self, str):
        super().__init__()
        self.show(str)

    def show(self,str):
        msg= QMessageBox()
        msg.setWindowTitle("Komunikat")
        if str=="brak1":#gdy nie wszystkie pola sa wypelnione przy dodawaniu meczu
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Uzupełnij wszystkie pola")
            msg.setInformativeText("Mecz nie został dodany")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        if str=="brak2":#gdy nie wszystkie pola wypelnione przy dodawaniu wyniku
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Uzupełnij wszystkie pola")
            msg.setInformativeText("Wynik nie został zapisany")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        if str=="czas":
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Niepoprawne dane w polu czas")
            msg.setInformativeText("Wpisz liczbę z przedziału 2-120")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        if str=="link":
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Niepoprawny link")
            msg.setInformativeText("Podaj link do odpowiedniego meczu ze strony STS")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        if str=="ok1":
            msg.setIcon(QMessageBox.Information)
            msg.setText("Mecz został dodany")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        if str=="ok2":
            msg.setIcon(QMessageBox.Information)
            msg.setText("Wynik został zapisany")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        if str=="nowy":
            msg.setIcon(QMessageBox.Information)
            msg.setText("Nowy mecz w zakładce 'Podejrzane'")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        if str=="usun":
            msg.setIcon(QMessageBox.Information)
            msg.setText("Mecz został usunięty")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        if str=="mailOK":
            msg.setIcon(QMessageBox.Information)
            msg.setText("Email dodany")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        
        if str=="mailFAILURE":
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Niepoprawny email")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    okno = MainWindow()
    sys.exit(app.exec_())
    