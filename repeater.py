import scraper
from threading import Thread
import time
import os
os.environ['TZ'] = 'utc'
class FakeDatabase():

    def notify(self,data):
        print('FakeDatabase (or gui) adding new data : ')
        for d in data:
            print(d)
        print()
        #self.data.append( data )

class TimedScraper(Thread):

    'Array with arrays [url,updateTime,timeLeft]'
    bets = [  ]
    
    unitMin = 1
    unitSec = unitMin * 60
    
    _shouldRun = True
    
    def __init__(self,observer=None):
        Thread.__init__(self,daemon=True)
        self.observer=observer
        #self.start()
        

    def run(self):
        while self._shouldRun:
            print('sleep for 60 sec, currTime : ',time.strftime("%H:%M",time.gmtime()) )
            time.sleep(self.unitSec)
            self.update()

    def update(self):
        print('update')
        push=[]
        for bet in self.bets:
            bet[2]+=self.unitMin
            if bet[2] == bet[1]:
                bet[2] = 0
                push.append( scraper.getData( bet[0] ) )                

        if len(push) > 0 :
            self.observer.notify(push)
        pass

    
    def add(self,url,interval):
        self.observer.notify( [scraper.getData( url )] )
        #self.observer.notify( url )
        self.bets.append( [url , interval , 0 ] )
        if len(self.bets) == 1:
            self.start()
        pass



    def stop(self):
        self._shouldRun = False

d=FakeDatabase()
t=TimedScraper(d)
t.add(
    'https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=201&region=6582&league=4555&oppty=182940380'
,1)
t.add('Bet 2 data',1)

t.add('https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=201&region=6582&league=4555&oppty=182877745' 
, 2 )
#t.add('Bet 4 data',4)

while True:
    time.sleep(60)


    
