import unittest
import sys
sys.path.insert(0, '../')
import os
import repeater
import scraper
from unittest.mock import patch

#to run this tests, enter this folder, python3 tests.py

class TestRepeater(unittest.TestCase):

    def setUp(self):
        print('remove db (sts) in current folder')
        try:
            os.remove("sts")
        except:
            print('not found db file to remove')

        self.scraper = repeater.TimedScraper()

        
        pass
    
    '''
    Test for Update function from TimedScraper()
    Call update once with some object in bets array and check if they behave correctly
    '''
    def test01_Check_Update_Call_Once(self):
        #mocking in such way that neither db or internet is needed in this test
        def notifyMock(o,data):
            self.assertEqual(data[0][0],'data','Incorrect data was passed something wrong in method')

        def getDataMock(url):
            self.assertNotEqual(url ,'test.url2','data should not be fetched from url with 2 min interval')
            return 'data'
            

        with patch.object(repeater.TimedScraper, "notify" , notifyMock),patch.object(scraper, "getData" , getDataMock):
            
            #should be notified and data taken from url
            self.scraper.bets.append(['test.url1',1,0])
            
            #notifty should not have that as we call update only once
            self.scraper.bets.append(['test.url2',2,0])
            
            self.scraper.update()

            self.assertTrue( self.scraper.bets[0][2] == 0 and self.scraper.bets[1][2] == 1 , 'Incorrect incrementation of time'  )
            
    def test02_Check_add_Function(self):
        pass

        
    def tearDown(self):
        print('tests passed')
        pass

if __name__ == '__main__':
    unittest.main()