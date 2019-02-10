
"""
Course: cmps 4883
Assignemt: A03
Date: 2/04/19
Github username: buddyjasmith
Repo url: https://github.com/buddyjasmith/4883-SWTools-Smith/edit/master/Assignment/A03/
Name: Buddy Smith
Description: 
    Using beautifulscraper, football game ids are scraped form NFL.com. The IDs are stored
    in the dict gameids.

"""

from beautifulscraper import BeautifulScraper
from pprint import pprint

import os
import json
from time import sleep


beauty = BeautifulScraper()
url = "http://www.nfl.com/schedules/"
years = list(range(2009, 2019))
weeks = list(range(1, 18)) # 17 weeks in season
preWeeks = list(range(1, 5))
postWeeks = list(range(1,2))
gameids = {'PRE':{}, 'REG':{},'POST':{}}


for year in years:
    gameids["PRE"][year] = {}
    for preWeek in preWeeks:
        gameids['PRE'][year][preWeek] =[]
        newURL = url + "%d/PRE%d" %(year,preWeek)           #create new URL
        page = beauty.go(newURL)                            #go to new url
        contents = page.find_all('div',{'class':'schedules-list-content'}) #collect contents
        for content in contents:
            gameids['PRE'][year][preWeek].append(content['data-gameid']) #append id with gameid
            sleep(.05)
            
    gameids['REG'][year]={}

    for week in weeks:
        gameids['REG'][year][week] = []
        newURL = url + "%d/REG%d" %(year,week)
        page = beauty.go(newURL)
        contents = page.find_all('div', {'class': 'schedules-list-content'})
        for content in contents:
            gameids['REG'][year][week].append(content['data-gameid'])
            sleep(0.05)


    newUrl = url + '%d/POST' % (year)
    gameids['POST'][year]=[]
    page = beauty.go(newUrl)
    contents = page.find_all('div', {'class': 'schedules-list-content'})
    # Traversal of weeks is not needed..  Stored as POST
    for content in contents:
        gameids['POST'][year].append(content['data-gameid'])
        sleep(0.05)

with open('gameids.json','w') as outfile:
    json.dump(gameids,outfile)







