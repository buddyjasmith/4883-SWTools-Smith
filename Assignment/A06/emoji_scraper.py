from beautifulscraper import BeautifulScraper
from pprint import pprint
from bs4 import BeautifulSoup
import os
import json
from time import sleep

bs = BeautifulScraper()
url = "https://www.webfx.com/tools/emoji-cheat-sheet/ "
page = bs.go(url)
count = 0
collection_path = '../A06/emoji_collection'
for emoji in page.find_all("span",{"class":"emoji"}):
    image_path = emoji['data-src']
    print(url+image_path)
    count += 1
print(count)