import requests
from bs4 import BeautifulSoup


def match_scraper(url):
    s = requests.session()
    s=s.get(url)
    page = s.text
    bets = BeautifulSoup(page, features="html.parser")
    bets = bets.findAll('td', {'class': 'bet'})
    bets = BeautifulSoup(str(bets), features="html.parser")
    bets = bets.findAll('a', href=True)
    bets = [BeautifulSoup(str(b), features="html.parser") for b in bets]
    bets_numbers = [b.find('span').text for b in bets]

    bets_name = [b.find('a', href=True).text for b in bets]
    bets_name = [bb.replace("\n", "-") for bb in bets_name]
    bets_name = [bb.split('-')[1].strip() for bb in bets_name]
    information = BeautifulSoup(str(page), features="html.parser")
    information = information.findAll('div', {'class': 'shadow_box support_bets_offer'})
    information = BeautifulSoup(str(information), features="html.parser")
    information = information.find('a', {'class': 'openMenu'}).text
    if bets_name[1] == 'X':
        return information.replace('\n', ''), bets_name[0], bets_name[1], bets_name[2], bets_numbers[0], bets_numbers[
            1], bets_numbers[2]
    else:
        return information.replace('\n', ''), bets_name[0], bets_name[1], bets_numbers[0], bets_numbers[1]

def getData(url):
        out = None

        try :
                out = match_scraper(url)
        except Exception as e: 
                #print ( 'failed to get data ', e ) 
                out = ('Error',e)
        return out


