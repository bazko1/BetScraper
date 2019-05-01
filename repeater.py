import scraper
from threading import Thread
import time
import os
from data_source_actuall import DataSourceActuall
from data_source_historical import DataSourceHistorical
from data_source_suspicious import DataSourceSuspicious
import datetime



class TimedScraper(Thread):

    'Array with arrays [url,updateTime,timeLeft]'
    bets = []
    
    unitMin = 1
    unitSec = unitMin * 60
    
    _shouldRun = True
    
    def __init__(self,observer=None):
        Thread.__init__(self,daemon=True)
        self.a = DataSourceActuall()
        self.h = DataSourceHistorical()
        self.s = DataSourceSuspicious()
        self.loadActuallUrls()
        

    '''Main runner waits time specified in unitSec and calls update function'''
    def run(self):
        while self._shouldRun:
            time.sleep(self.unitSec)
            self.update()
            

    def update(self):
        push=[]
        for bet in self.bets:
            bet[2]+=self.unitMin
            if bet[2] == bet[1]:
                bet[2] = 0
                push.append( (scraper.getData( bet[0] ),bet[0] ) )                

        if len(push) > 0:
            self.notify(push)
        
        
        pass

    
    def add(self,url,interval):
        
        data = scraper.getData( url )
        
        if data[0] == 'Error':
            print('repeater.py(57): Failed to get data')
            return

        #insert match data to actuall
        self.a.insert_data(data)
        
        if data[3] =='X':
            d = (data[0].replace('.', '-'), data[2], data[4], url, interval) 
        else:
            d = (data[0].replace('.', '-'), data[2], data[3], url, interval) 
            
        #insert url and interval 
        self.a.insert_url_int( d )
        
        self.bets.append( [url , interval , 0 ] )
        
        #start main thread if we have first url
        if len(self.bets) == 1 and not self.is_alive():
            self.start()
        pass


    'data is information scraped using scraper' 'data tuple (scraped(url),url) '
    def notify(self,data): 
        
        now = datetime.datetime.now()

        for d,url in data:
            
            #if we get error in previously added match it probably already started
            #but we got it in base so we can get from it
            if d[0] == 'Error':
                d = self.a.get_data_byURL(url)[0]

            #check if match should be in historical and removed from actual.
            Mdt = datetime.datetime.strptime( d[0] + " " + d[1] ,"%d-%m-%Y %H:%M")

            if now >= Mdt:
                
                #Set IsActual=0 so we percieve this data as historical
                
                if d[3] == 'X':
                    self.a.set_data_historical( d[2], d[4] , d[0] )
                else:
                    self.a.set_data_historical( d[2], d[3] , d[0] )
                
                #remove from refresh array
                self.bets = list(filter( lambda x : not url in x  ,self.bets))

            elif d[0] != 'Error' :
                self.a.insert_data(d)
                
            else: 
                print('repeater.py(110): failed to download ' + d[1] )
                #match not started and d[0] == 'Error'
                #we will not add anything and hope sts will fix itself so we can get data later
                pass
                

    def loadActuallUrls(self):
        urls=[]
        intervals=[]

        for u,i in self.a.get_all_urlint():
            if not u in urls:
                self.bets.append( [u , int(i) , 0 ] )
                urls.append(u)
                intervals.append(int(i))
        
        if len(urls) > 0 and not self.is_alive():
            self.start()
        
        print('repeater.py(129): loaded actual matches : ' , urls , 'with ints : ', intervals )

    def removeFromQueue(self,host,away,date):
        
        dbUrls = map( lambda x : x[0],self.a.get_url(host,away,date) )
        thUrls = map(lambda x : x[0] , self.bets )    

        for url in dbUrls:
            if url in thUrls:
                print('repeater.py(138) : removing url from queue : ' + url )
                self.bets = list( filter( lambda x : not url in x  ,self.bets) )
                print( 'repeater.py ', self.bets )