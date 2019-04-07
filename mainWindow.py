#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from database1 import *

class mainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1065,600)
        self.interfejs()

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
        DodajBtn.clicked.connect(AddWindow)
        koniecBtn = QPushButton("Zakończ", self)
        koniecBtn.setMaximumWidth(200)
        koniecBtn.setStyleSheet("font: bold;color: dark blue; background-color: white; border-color: beige")
        koniecBtn.clicked.connect(QApplication.instance().quit)

        mylabel=QLabel()
        pixmap=QPixmap("/home/teresa/sts.jpg")
        mylabel.setPixmap(pixmap)
        mylabel.setFixedSize(200,150)
        mylabel.move(900,500)


        inputImg = QImage("/home/teresa/sts.jpg")
        imgDisplayLabel = QLabel()
        imgDisplayLabel.setPixmap(QPixmap.fromImage(inputImg))
        imgDisplayLabel.setScaledContents(True)
        imgDisplayLabel.setFixedSize(200, 150)
        #imgDisplayLabel.setAlignment(QtCore.Qt.AlignRight)

        btnGroup = QVBoxLayout()
        btnGroup.addWidget(DodajBtn)
        btnGroup.addWidget(koniecBtn)
        btnGroup.setSpacing(0)
        #btnGroup.setAlignment(QtCore.Qt.AlignLeft)

        gridLayout=QGridLayout()
        gridLayout.addWidget(imgDisplayLabel, 0,2)
        gridLayout.addLayout(btnGroup, 0,0)
        gridLayout.setColumnStretch(1, -2)
        #gridLayout.setColumnStretch(2,50)
        layoutA.addLayout(gridLayout)


        # tabs
        tab_widget = QTabWidget()
        tab_widget.addTab(MyTab(), "Aktualne")
        tab_widget.addTab(MyTab(), "Podejrzane")
        tab_widget.addTab(MyTab(), "Historyczne")
        layoutA.addWidget(tab_widget)

        #layoutA.addLayout(layoutB)
        self.setLayout(layoutA)


        self.setGeometry(20, 20, 850, 600)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 165, 0))
        self.setPalette(p)
        self.setWindowTitle("Aplikacja bukmacherska")
        self.show()

class ResultCell(QWidget):

    def __init__(self):
        super().__init__()
        result1=QLineEdit()
        result2=QLineEdit()
        colon=QLabel(":")
        layout3=QHBoxLayout()
        layout3.addWidget(result1)
        layout3.addWidget(colon)
        layout3.addWidget(result2)
        self.setLayout(layout3)
        self.setFixedSize(100,40)
        self.show()

class MyTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,300,400)
        self.table_view=QTableView()
        self.AddTable()
        layout2=QVBoxLayout()
        sort_text=QLabel("Sortuj według: ")
        cb = QComboBox()
        cb.addItems(["Data dodania zakładu", "Data rozgrywki", "Kwota zakładu"])
        cb.currentIndexChanged.connect(self.selectionchange)
        layout2.addWidget(sort_text)
        layout2.addWidget(cb)
        layout2.addWidget(self.table_view)
        self.setLayout(layout2)

    def AddTable(self):

        self.table_view.showFullScreen()
        self.table_model=MyTableModel()
        self.table_view.setModel(self.table_model)
        self.table_view.setMinimumSize(300, 300)

        ile=self.table_model.rowCount(self)
        for i in range(0, ile):
            showButton=QPushButton("Pokaż wykres")
            showButton.setStyleSheet("background-color: beige;border-color: beige")
            showButton.clicked.connect(Plot)
            self.table_view.setIndexWidget(self.table_model.index(i, 9), showButton)
            self.table_view.setIndexWidget(self.table_model.index(i, 8), ResultCell())

    def selectionchange(self, i):
            if(i==0):
                print ("Sortuje wg daty wstawienia")

            elif (i==1):
                print("Sortuje wg daty rozgrywki")
            elif (i==2):
                print("Sortuje wg stawek kursów")



class MyTableModel(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self.mylist=a.get_data()

    def rowCount(self,parent):
        return len(self.mylist)

    def columnCount(self,parent):
        return len(self.mylist[0])


    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.column()==8:
                return ""
            if index.column()==9:
                return ""
            return self.mylist[index.row()][index.column()]
        return None

    def headerData(self, column, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal:
            if column==0:
                return QtCore.QVariant('Data')
            if column==1:
                return QtCore.QVariant('Godzina')
            if column==2:
                return QtCore.QVariant('Drużyna 1')
            if column==3:
                return QtCore.QVariant('X')
            if column==4:
                return QtCore.QVariant('Drużyna 2')
            if column==5:
                return QtCore.QVariant('Wygrana 1')
            if column==6:
                return QtCore.QVariant('Remis')
            if column==7:
                return QtCore.QVariant('Wygrana 2')
            if column==8:
                return QtCore.QVariant('Wynik meczu')
            if column==9:
                return QtCore.QVariant('Pokaz wykres')

class Plot(QDialog):
    def __init__(self):
        super().__init__()
        self.dodaj()

    def makePlot(self):
        print ("Rysuje wykres")

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
    def __init__(self):
        super().__init__()
        self.dodaj()

    def dodaj(self):


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
        elif self.check(b)==False:
            MessageWindow("czas")
        else:
            MessageWindow("ok")
            print(self.wpisz1.text() + '   ' +self.wpisz2.text())
            self.close()

    def check(self, b):
        #trzy znaki
        if len(b)<1 or len(b)>3:
            return False
        #pierwszy znak miedzy 1 a 9
        if ord(b[0])<49 or ord(b[0])>57:
            return False
        #liczba jednocyfrowa, musi byc miedzy 2 a 9
        if b[0]==1 and len(b)==1:
            return False
        #liczba dwucyfrowa,
        if len(b)==2:
            if (ord(b[1])<48 or ord(b[1])>57):
                return False
        #liczba trzycyfrowa, musi miec pierwsza cyfre 1
        if len(b)==3:
            if b[0]!="1":
                return False
        #liczba trzycyfrowa gdy najpierw jedynka, sprawdzenie drugiej cyfry
            if b[1]!="1" and b[1]!="0" and b[1]!="2":
                return False
        #liczba trzycyfrowa 120
            if b[1] == "2" and b[2] != "0":
                return False
            if (b[1] == "0" or b[1] == "1") and (ord(b[2]) < 48 or ord(b[2]) > 57):
                return False
        return True

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

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = mainWindow()
    sys.exit(app.exec_())
