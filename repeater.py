import scraper
from threading import Thread
import time

class TimedScraper(Thread):
    def __init__(self,url,interval,repetitions=None):
        Thread.__init__(self)
        self.interval   = interval
        self.url = url
        self._shouldRun = True
        self.start()

    def run(self):
        while self._shouldRun:
            self.getData()
            time.sleep(self.interval)

    def getData(self):
        try:
            print( scraper.match_scraper(self.url) )
            #put data to database ?
        except Exception as  e: 
            print ( 'failed to get data ', e ) 
        pass

    def stop(self):
        self._shouldRun = False


print ("starting...")

## added 2 matches for now
Threads = [
 TimedScraper(
'https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=186&region=6484&league=3893&oppty=139108562', 10 )
,
TimedScraper(
'https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=186&region=6484&league=3893&oppty=139108563', 20 )

]


rep=0

try:
    while True:

        #we would handle user interactions here
        
        if rep == 1:
            print ( 'stoping one thread' ) 
            Threads[0].stop()

        if rep == 3 :
            break
        
        time.sleep(60)
        print ( '60 sec passed' ) 
        rep+=1

finally:
     for th in Threads:
         th.stop() # better in a try/finally block to make sure the program ends!
