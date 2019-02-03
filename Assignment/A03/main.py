from beautifulscraper import BeautifulScraper
from pprint import pprint
scraper = BeautifulScraper()
import os
import json
from time import sleep


beauty = BeautifulScraper()
url = "http://www.nfl.com/schedules/"
years = list(range(2009, 2019))

weeks = list(range(1, 17))
preWeeks = list(range(1, 5))
postWeeks = list(range(1,2))
gameids = {'PRE':{}, 'REG':{},'POST':{}}


for year in years:
    gameids["PRE"][year] = {}
    for preWeek in preWeeks:
        gameids['PRE'][year][preWeek] =[]
        newURL = url + "%d/PRE%d" %(year,preWeek)
        #print(newURL)
        page = beauty.go(newURL)
        contents = page.find_all('div',{'class':'schedules-list-content'})
        print("Starting Preseason schedule for %d, week %d" %(year,preWeek))
        for content in contents:
            gameids['PRE'][year][preWeek].append(content['data-gameid'])
            #print(gameids['PRE'][year][preWeek])
            sleep(.05)
    gameids['REG'][year]={}
    print("Starting regular season process for year %d" %(year))
    for week in weeks:
        #print("Regualr Season. Year %d. Week %d" %(year,week))
        gameids['REG'][year][week] = []
        newURL = url + "%d/REG%d" %(year,week)
        page = beauty.go(newURL)
        contents = page.find_all('div', {'class': 'schedules-list-content'})
        for content in contents:
            gameids['REG'][year][week].append(content['data-gameid'])
            sleep(0.05)

    print("Starting POST Season scrap")
    newUrl = url + '%d/POST' % (year)
    gameids['POST'][year]=[]
    page = beauty.go(newUrl)
    contents = page.find_all('div', {'class': 'schedules-list-content'})

    for content in contents:
        gameids['POST'][year].append(content['data-gameid'])
        sleep(0.05)

with open('gameids.json','w') as outfile:
    json.dump(gameids,outfile)







