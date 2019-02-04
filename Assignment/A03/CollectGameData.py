import os
import json
import urllib.request

#Vars
missedIDS = {}      #store missed game IDS and URLs
allIDS = {}         #store all Game IDs and URLs
path = "/home/drew/SoftwareTools/scrapeGameData/Data/"      #system Path
url = "http://www.nfl.com/liveupdate/game-center/"          #self exp.
os.mkdir(path, 0o777)                                       #create new directory to store json files

#Open json file to read data
with open('gameids.json') as f:
    collection = json.load(f)




#Iterate through json structure and collect gameID and URL to download data.
#Keys and values are store in allIDS.
for gameType, data in collection.items():
            # Get preseason games
            if gameType == 'PRE':
                continue
            elif gameType == 'REG':
                for year, weeks in data.items():
                    for week, ids in weeks.items():
                        for id in ids:
                            newURL = url + '%s/%s_gtd.json' % (id, id)
                            allIDS[id] = newURL
            elif gameType == 'POST':
                for year, ids in data.items():
                    for id in ids:
                        newURL = url + '%s/%s_gtd.json' % (id, id)
                        allIDS[id] = newURL

#Attempt downloading json files of game data
for key, value in allIDS.items():
    try:
        #print("Downloading Game: %s @ %s" % (key,value))
        urllib.request.urlretrieve(value, path + key + '.json')
    except:
        print('Failed to Download GameID: %s' % key)
        missedIDS[key] = value
# End for loop

#Attempt to redownload missed addresses
if len(missedIDS) >0:
    print("These game ids were not downloaded due to error:")
    # print(missedIDS)
    print("Attempting to download again.")
    for key,value in missedIDS.items():
        try:
            print("GameID: %s.  Attempting to download" % key)
            urllib.request.urlretrieve(value, path + key + '.json')
            print("%s successfully downloaded" % key)
        except:
            print("Unable to download GameID:: %s. Perform manual download." % key)
    # End for loop
else:
    print("All Entries were sucessfully downloaded!")
