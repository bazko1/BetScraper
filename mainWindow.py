#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QGridLayout 
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout 

def layout_widgets(layout):
    return (layout.itemAt(i) for i in range(layout.count()))


class mainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setGeometry(20, 20, 500, 500)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 165, 0))
        self.setPalette(p)
        self.setWindowTitle("Aplikacja bukmacherska")
        self.Views={}
        layout=QVBoxLayout()
        self.setLayout(layout)
        
        self.preparemainView()
        self.prepareAddBetView()
        
        self.currView='main'
        self.setView('main')

    

    def hideView(self,view):
        for w in self.Views[view]:
            w.hide()
    def hideCurrView(self):
        self.hideView(self.currView)

    def showView(self,view):
        for w in self.Views[view]:
            w.show()
    

    def setView(self,view):
        if self.currView:
            self.hideView(self.currView)
        
        self.showView(view)
        self.currView=view
        self.show()
    
    def showAddView(self):
        self.setView('add')

    def showMainView(self):
        self.setView('main')


    def addBet(self):
        print(self.currUrl.text())
    
    def prepareAddBetView(self):
        layout=self.layout()

        layout=self.layout()

        title=QLabel("Dodaj mecz", self)
        title.setFixedSize(500,40)
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setWeight(80)
        title.setFont(font)

        
        insert=QLineEdit("",self)
        layout.addWidget(insert)
        self.currUrl=insert

        addBtn = QPushButton("Dodaj", self)
        layout.addWidget(addBtn)
        addBtn.clicked.connect(self.addBet)

        powrtBtn = QPushButton("Powrót", self)
        layout.addWidget(powrtBtn)
        powrtBtn.clicked.connect(self.showMainView)

        self.Views['add']=[title,powrtBtn,addBtn,insert]
        self.hideView('add')

    def preparemainView(self):

        layout=self.layout()
        

	# Napis glowny

        title=QLabel("STRONA GŁÓWNA", self)
        title.setFixedSize(500,40)
        title.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setPointSize(16)
        font.setWeight(80)
        title.setFont(font)

        # przyciski
        AktualneBtn = QPushButton("Aktualne mecze", self)
        HistoryczneBtn = QPushButton("Historyczne mecze", self)
        PodejrzaneBtn = QPushButton("Podejrzane mecze", self)
        DodajBtn = QPushButton("Dodaj mecz", self)
        koniecBtn = QPushButton("Koniec", self)
        koniecBtn.clicked.connect(QApplication.instance().quit)
        
        DodajBtn.clicked.connect(self.showAddView)

        #layout.setSpacing(0)
        layout.addWidget(title)
        layout.addWidget(AktualneBtn)
        layout.addWidget(HistoryczneBtn)
        layout.addWidget(PodejrzaneBtn)
        layout.addWidget(DodajBtn)
        layout.addWidget(koniecBtn)
        
        self.Views['main']=[
            title,
            AktualneBtn,
             HistoryczneBtn,
             PodejrzaneBtn,
             DodajBtn,
             koniecBtn
             ]
        
        self.hideView('main')
        #self.setLayout(layout)
        #groupBox.show()
        

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = mainWindow()
    sys.exit(app.exec_())
