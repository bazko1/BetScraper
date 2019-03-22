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


# piłka nożna
#print(match_scraper(

 #   'https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=184&region=6480&league=15905&oppty=170415620'))
# koszykówka
#print(match_scraper(
#'https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=186&region=6484&league=3893&oppty=139108562'
#'https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=184&region=6499&league=74171&oppty=180376313'
#) 
#)

# tenis
#print(match_scraper(
#    'https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=185&region=6609&league=76050&oppty=181052469'))
# siatkowka
#print(match_scraper(
 #   'https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=183&region=6502&league=4142&oppty=175906997'))
# hokej
#print(match_scraper(
#    'https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=188&region=6484&league=4077&oppty=140240642'))
