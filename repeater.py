import scraper
from threading import Thread
import time
import os
os.environ['TZ'] = 'utc'
class FakeDatabase():
    data=[]
    def notify(self,data):
        print('FakeDatabase (or gui) adding new data : ' + str(data) )
        self.data.append( data )

class TimedScraper(Thread):

    'Array with tuples (url,time)'
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
                push.append(bet[0])
                #push.( scraper.getData( url ) )                

        if len(push) > 0 :
            self.observer.notify(push)
        pass

    
    def add(self,url,interval):
        #self.observer.notify( scraper.getData( url ) )
        self.observer.notify( url )
        self.bets.append( [url , interval , 0 ] )
        if len(self.bets) == 1:
            print('There was bet added starting...')
            self.start()
        pass



    def stop(self):
        self._shouldRun = False

d=FakeDatabase()
t=TimedScraper(d)
t.add('Bet 1 data',1)
t.add('Bet 2 data',1)

time.sleep(60)
t.add('Bet 3 data',2)
t.add('Bet 4 data',4)

while True:
    time.sleep(60)


    
