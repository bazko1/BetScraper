#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QBoxLayout


class mainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def interfejs(self):

        layout=QVBoxLayout()

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

        #layout.setSpacing(0)
        layout.addWidget(title)
        layout.addWidget(AktualneBtn)
        layout.addWidget(HistoryczneBtn)
        layout.addWidget(PodejrzaneBtn)
        layout.addWidget(DodajBtn)
        layout.addWidget(koniecBtn)

        self.setLayout(layout)

        self.setGeometry(20, 20, 500, 500)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 165, 0))
        self.setPalette(p)
        self.setWindowTitle("Aplikacja bukmacherska")
        self.show()



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = mainWindow()
    sys.exit(app.exec_())
