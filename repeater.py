import scraper
from threading import Thread
import time
import os
from data_source_actuall import DataSourceActuall
from data_source_historical import DataSourceHistorical
from data_source_suspicious import DataSourceSuspicious
        

class TimedScraper(Thread):

    'Array with arrays [url,updateTime,timeLeft]'
    bets = [  ]
    
    unitMin = 1
    unitSec = unitMin * 60
    
    _shouldRun = True
    
    def __init__(self,observer=None):
        Thread.__init__(self,daemon=True)
        self.database = DataSourceActuall()
        self.h = DataSourceHistorical()
        self.s = DataSourceSuspicious()

    '''Main runner waits time specified in unitSec and calls update function'''
    def run(self):
        while self._shouldRun:
            time.sleep(self.unitSec)
            self.updateM()
            

    def updateM(self):
        push=[]
        for bet in self.bets:
            bet[2]+=self.unitMin
            if bet[2] == bet[1]:
                bet[2] = 0
                push.append( scraper.getData( bet[0] ) )                

        if len(push) > 0 :
            self.notifyM(push)
        pass

    
    def addM(self,url,interval):
        self.notifyM( [scraper.getData( url )] )
        self.bets.append( [url , interval , 0 ] )
        if len(self.bets) == 1:
            self.start()
        pass


    def notifyM(self,data):
        for d in data:
            self.database.insert_data(d)

