'''
Name: Buddy Smith
Class: 4883_Software_Tools
Desc: The program scrapes emojis from webfx.com/tools/emoji-cheat-sheet and
      stores the content and zips the file for easy uploading time.
'''
from beautifulscraper import BeautifulScraper
from zipfile import ZipFile
import os
import sys
import urllib.request

def collect_emoji(storage):
    '''
    This function collects photos from webfx.com/tools/emoji-cheat-sheet.
    :param storage: location for emojis to be stored
    :return: 1 if successful, 0 otherwise
    '''
    bs = BeautifulScraper()
    url = "https://www.webfx.com/tools/emoji-cheat-sheet/"

    page = bs.go(url)
    if(page):
        count = 0
        print("Beginning Scrape.")
        for emoji in page.find_all("span",{"class":"emoji"}):
            image_path = emoji['data-src']
            a,b,c = image_path.split("/")
            urllib.request.urlretrieve(url+image_path, storage + c)

def zip_emojis(directory):
    '''
    This function will turn the contents of a file into a zip folder.
    The name of the zip file will be stored as emojis.zip
    :param directory: location of directory to turn into a zip file
    :return:
    '''

    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    with ZipFile('emojis.zip','w') as f:
        for file in file_paths:
            f.write(file)

if __name__ == '__main__':
    '''
    Example parameters:
    python3 emoji_scraper.py /some/storage/location/
    '''
    if (len(sys.argv)==2):
        # Collect all emojis and store
        collect_emoji(sys.argv[1])

        # Zip directory of stored emojis
        zip_emojis(sys.argv[1])




