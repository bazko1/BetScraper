#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class mainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def interfejs(self):

        layout=QVBoxLayout()


    # Napis glowny
        title=QLabel("APLIKACJA BUKMACHERSKA", self)
        title.setFixedSize(500,40)
        title.setAlignment(QtCore.Qt.AlignCenter)

        font = QFont()
        font.setPointSize(16)
        font.setWeight(80)
        title.setFont(font)

        # przyciski
        DodajBtn = QPushButton("Dodaj mecz", self)
        DodajBtn.setMaximumWidth(200)
        DodajBtn.setStyleSheet("font: bold; color: dark blue; background-color: white; border-color: beige")
        DodajBtn.clicked.connect(AddWindow)
        koniecBtn = QPushButton("Zakończ", self)
        koniecBtn.setMaximumWidth(200)
        koniecBtn.setStyleSheet("font: bold;color: dark blue; background-color: white; border-color: beige")
        koniecBtn.clicked.connect(QApplication.instance().quit)

        # layout.setSpacing(0)
        layout.addWidget(title)
        layout.addWidget(DodajBtn)
        layout.addWidget(koniecBtn)

        # tabs
        tab_widget = QTabWidget()
        tab_widget.addTab(MyTab(), "Aktualne")
        tab_widget.addTab(MyTab(), "Podejrzane")
        tab_widget.addTab(MyTab(), "Historyczne")



        # Add tabs to widget
        layout.addWidget(tab_widget)
        self.setLayout(layout)

        self.setGeometry(20, 20, 500, 500)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 165, 0))
        self.setPalette(p)
        self.setWindowTitle("Aplikacja bukmacherska")
        self.show()


class MyTab(QWidget):
    def __init__(self):
        super().__init__()

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
        btn1 = QPushButton("btn1")
        btn2 = QPushButton("btn2")
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
        self.pokaz(str)

    def pokaz(self,str):
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
