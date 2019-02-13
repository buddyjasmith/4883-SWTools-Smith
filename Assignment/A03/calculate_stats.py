"""
Course: cmps 4883
Assignemt: A03
Date: 2/13/19
Github username: buddyjasmith
Repo url: https://github.com/buddyjasmith/4883-SWTools-Smith
Name: Buddy Smith
Description:
    The program calls functions to solve the given questions produced by Dr. Griffin.
    The program uses data stored in the folder 'Data/', representing NFL games played
    between 2009-2018. These games are iterated through while data is being collected.
"""


import os, sys
import json
import pprint as pp
import ujson
from termcolor import colored

AllPlayers={}
"""
Tries to open a file 
"""
##############################################################
# openFileJson(path)
# This function was written by Dr. G., it attempts to open a file
# using a given path, path.  It then checks if the file is of json
# format.
#
# Params:
#    path: path of file to be checked

# Returns:
#    returns the json file data
def openFileJson(path):
    try:
        f = open(path, "r")
        data = f.read()
        if is_json(data):
            return json.loads(data)
        else:
            print("Error: Not json.")
            return {}
    except IOError:
        print("Error: Game file doesn't exist.")
    return {}


##############################################################
# is_json(myjson)
# This function checks if the file passed is json format
#
# Params:
#    my_json [file]
# Returns:
#    the function attempts to load the json file. If a ValueError occurs
#    it returns false.  It it was successfully loaded, true is returned.

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

##############################################################
# getFiles(path)
# This function returns all files in a given path directory.
# If a git file exists in the directory, the git file is removed.
# Written by Dr. G.
#
# Params:
#    path : directory path where files will be collected from
#
#
# Returns:
#    The function returns all files in a given directory

def getFiles(path):
    files = []
    for dirname, dirnames, filenames in os.walk(path):
        # print path to all subdirectories first.
        # for subdirname in dirnames:
        #     print(os.path.join(dirname, subdirname))

        # print path to all filenames.
        for filename in filenames:
            # print(os.path.join(dirname, filename))
            files.append(os.path.join(dirname, filename))

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        if '.git' in dirnames:
            # don't go into any .git directories.
            dirnames.remove('.git')
    return files


##############################################################
# getAllPlayerNames()
# This function collects all user names in the Directory path
# and unique id associated with each player. each player is stored
# in the Dictionary AllPlayers{} for easy access to player names for
# later print out.
#
# Params:
#    none
# Returns:
#    none

def getAllPlayerNames():

    print(colored("Collecting all player IDS and Names that played in 2009-2018 season",'blue'))
    path = 'Data/'
    files = getFiles(path)
    files = sorted(files)
    x = 0
    for file in files:
        data = openFileJson(file)
        for gameid, gamedata in data.items():
            if gameid != 'nextupdate':
                # print('GameID: %s' % str(gameid))
                for driveid, drivedata in gamedata['drives'].items():
                    #print(driveid)
                    if driveid != 'crntdrv':
                        for playid, playdata in drivedata['plays'].items():  # in drives json file
                            # print(playdata)
                            for k, play in playdata['players'].items():
                                #print(play)
                                if (k != '0'):
                                    # print("PlayerID: %s" % str(k))

                                    for i in play:
                                        #print(i)
                                        for key, value in i.items():
                                            if key == 'playerName':
                                                if k not in AllPlayers.items():

                                                    AllPlayers[k]=[]
                                                    AllPlayers[k] = value

    print (colored("\t-All names and ID's have been collected.",'green'))
    return


##############################################################
# getPlayerTeams
# This function finds the number of teams associated with each
# player id. The results are stored in Players[id]=[teams]. Defunct
# teams are removed from all the playerids, and the player who has played
# for the most teams is printed to screen
#
# Params:
#    none
# Returns:
#    none

def getPlayerTeams():
    print(colored("\n\n1: Find the player that played for the most teams.",'blue'))

    Players = {} # initialize dict
    path = 'Data/'
    files = getFiles(path)
    files = sorted(files)
    x = 0
    for file in files:
        data = openFileJson(file)
        for gameid, gamedata in data.items():
            if gameid != 'nextupdate':

                for driveid, drivedata in gamedata['drives'].items():

                    if driveid != 'crntdrv':
                        for playid, playdata in drivedata['plays'].items(): #in drives json file

                            for k,play in playdata['players'].items():
                                if( k != '0'):



                                    for i in play:

                                        for key,value in i.items():
                                            #If key equals clubcode, store the value in team to use in dict, clubcode comes before playername
                                            if(key =='clubcode'):
                                                team = value

                                            if(key == 'playerName'):
                                                if k not in Players:
                                                    Players[k] = set()
                                                Players[k].add(team)

    #remove all bullshit clubcodes from, these are on nfl.com...no idea why
    wtfTeamCodes = {'AFC','NFC','APR','RIC','NPR','SAN'}
    for key, value in Players.items():
        value.discard('AFC')
        value.discard('NFC')
        value.discard('APR')
        value.discard('NPR')
        value.discard('SAN')
        value.discard('RIC')
    Player = {}
    # get length of number of teams, store in new dict
    for key, value in Players.items():
        d = {key:len(value)}
        Player.update(d)
    max = 0

    for key, value in Player.items():
        if(int(value) > max):
            max = int(value)
            k = key
            v = value
    name = AllPlayers.get(k,None)
    print(colored("\t-The player: %s has played for %s teams." % (name,str(v)),'green'))

    return


##############################################################
# multipleTeams
# This function is not finished!  NonWorking!!!
# This function stores the number of teams each player played on
# each year in Players[years][id] = [teams].  
#
# Params:
#    none
# Returns:
#    none
def multipleTeams():
    Players = {}
    path = 'Data/'
    files = getFiles(path)
    year = list(range(2009, 2019))
    statID = 0


    #files = getFiles(path)
    files = sorted(files)
    print(colored("\n\n3: Find the player that played for the most team in each year",'blue'))

    for file in files:
        data = openFileJson(file)
        for gameid, gamedata in data.items():


            if gameid != 'nextupdate':
                year = gameid[:4]
                for driveid, drivedata in gamedata['drives'].items():

                    if driveid != 'crntdrv':
                        for playid, playdata in drivedata['plays'].items(): #in drives json file

                            for k,play in playdata['players'].items():
                                if( k != '0'):


                                    for i in play:

                                        for key,value in i.items():
                                            # If key equals clubcode, store the value in team to use in dict, clubcode comes before playername
                                            if (key == 'clubcode'):
                                                team = value

                                            if (key == 'playerName'):
                                                if year not in Players.keys():
                                                    Players[year]= {}
                                                if k not in Players[year].keys():
                                                    Players[year][k] = set()
                                                Players[year][k].add(team)
        # remove all bullshit clubcodes from, these are on nfl.com...no idea why
        wtfTeamCodes = {'AFC', 'NFC', 'APR', 'RIC', 'NPR', 'SAN'}
        for key in Players.items():
            for k, v in key.items():
                v.discard('AFC')
                v.discard('NFC')
                v.discard('APR')
                v.discard('NPR')
                v.discard('SAN')
                v.discard('RIC')
        pp.pprint(Players)

##############################################################
# mostYardsRushedForLoss()
# This function collects all playerids and yards of players who have
# rushed for negative yardage.  The player with the biggest defecit
# is printed to screen
#
# Params:
#    none
# Returns:
#    none
def mostYardsRushedForLoss():
    Players = {}
    path = 'Data/'
    files = getFiles(path)

    statID = 0


    #files = getFiles(path)
    files = sorted(files)
    print(colored("\n\n3: Find the player that had the most yards rushed for a loss.",'blue'))

    for file in files:
        data = openFileJson(file)
        for gameid, gamedata in data.items():
            if gameid != 'nextupdate':

                for driveid, drivedata in gamedata['drives'].items():

                    if driveid != 'crntdrv':
                        for playid, playdata in drivedata['plays'].items(): #in drives json file

                            for k,play in playdata['players'].items():
                                if( k != '0'):


                                    for i in play:

                                        for key,value in i.items():

                                            if key == 'playerName':
                                                name = value
                                            elif key == "statId":
                                                if value == 10:
                                                   statID = value
                                            elif key == 'yards' and statID == 10:
                                                try:
                                                    if value < 0:
                                                        if k not in Players.keys():
                                                            Players[k] = []
                                                        Players[k].append(int(value))
                                                    statID = 0



                                                except TypeError:
                                                    statID = 0
                                                    name=''
    Player ={}
    largestLoss = 0
    for key, value in Players.items():
        val = sum(value)
        if val < largestLoss:
            largestLoss = val
            id = key

    name = AllPlayers.get(id, None)
    print(colored("The player with the most rushes for a loss:",'green'))
    print(colored("\t-%s for a loss of %s yards" %(name,largestLoss),'green'))





##############################################################
# mostRushedForLoss()
# This function collects all playerids and rush attempts of players who have
# rushed for negative yardage.  The player with the most negative attempts
# is printed to screen
#
# Params:
#    none
# Returns:
#    none
def mostRushesForLoss():
    Players = {}
    path = 'Data/'
    files = getFiles(path)

    statID = 0


    #files = getFiles(path)
    files = sorted(files)
    print(colored("\n\n4: Find the player that had the most rushes for a loss.",'blue'))

    for file in files:
        data = openFileJson(file)
        for gameid, gamedata in data.items():
            if gameid != 'nextupdate':

                for driveid, drivedata in gamedata['drives'].items():

                    if driveid != 'crntdrv':
                        for playid, playdata in drivedata['plays'].items(): #in drives json file

                            for k,play in playdata['players'].items():
                                if( k != '0'):


                                    for i in play:

                                        for key,value in i.items():

                                            if key == 'playerName':
                                                name = value
                                            elif key == "statId":
                                                if value == 10:
                                                   statID = value
                                            elif key == 'yards' and statID == 10:
                                                try:
                                                    if value < 0:
                                                        if k not in Players.keys():
                                                            Players[k] = []
                                                        Players[k].append(1)
                                                    statID = 0
                                                except TypeError:
                                                    statID = 0
                                                    name =''

    mostRushLoss = 0
    for key, value in Players.items():
        val = sum(value)
        if val > mostRushLoss:
            mostRushLoss = val
            id = key
    name = AllPlayers.get(id,None)
    print(colored("\t-The player: %s had %s rushes for a loss" % (name,mostRushLoss),'green'))



##############################################################
# mostPassesForLoss()
# This function collects all playerids and pass attempts that have resulted in
# negative yardage. The results are stored in a dictionary and the top result
# is printed to the screen
# Params:
#    none
# Returns:
#    none
def mostPassesforLoss():
    Players = {}
    path = 'Data/'
    files = getFiles(path)
    statID = 0
    files = sorted(files)
    print(colored("\n\n5: Find the player(s) with the most number of passes for a loss.",'blue'))
    for file in files:
        data = openFileJson(file)
        for gameid, gamedata in data.items():

            if gameid != 'nextupdate':

                for driveid, drivedata in gamedata['drives'].items():

                    if driveid != 'crntdrv':
                        for playid, playdata in drivedata['plays'].items():  # in drives json file

                            for k, play in playdata['players'].items():
                                if (k != '0'):


                                    for i in play:
                                        #print(i)
                                        for key, value in i.items():


                                            if key == "statId":
                                                if value == 15:
                                                    statID = value
                                            elif key == 'yards' and statID == 15:
                                                try:
                                                    if value < 0:
                                                        if k not in Players.keys():
                                                            Players[k] = []

                                                        # print(value)
                                                        Players[k].append(1)
                                                    statID = 0



                                                except TypeError:
                                                    statID = 0


    numberOfLosses = 0
    for key, value in Players.items():

        val = sum(value)
        #print(val)
        if val > numberOfLosses:
            numberOfLosses = val
            id = key

    name = AllPlayers.get(id,None)
    print(colored("\t-%s had the most number of passes for a loss of %s yards" %(name,numberOfLosses),'green'))


##############################################################
# mostPenalties()
# This function collects the team with the most penalties and
# the team with the most yardage given to penalties. The results
# are printed to the screen for the user
#
# Params:
#    none
# Returns:
#    none

def MostPenalties():
    print(colored("\n\n6: Find the team with the most penalties.",'blue'))
    Teams = {} # initialize dict
    TeamPenaltyYards={}
    WTFTeamCodes=['AFC','NFC','APR', 'NPR','SAN','RIC']
    penaltyCodes=[5,93]
    flag = None
    path = 'Data/'
    files = getFiles(path)
    files = sorted(files)

    for file in files:
        data = openFileJson(file)
        for gameid, gamedata in data.items():
            if gameid != 'nextupdate':
                #print('GameID: %s' % str(gameid))
                for driveid, drivedata in gamedata['drives'].items():

                    if driveid != 'crntdrv':
                        for playid, playdata in drivedata['plays'].items(): #in drives json file

                            for k,play in playdata['players'].items():
                                if( k != '0'):



                                    for i in play:

                                        for key,value in i.items():
                                            #If key equals clubcode, store the value in team to use in dict, clubcode comes before playername
                                            if(key =="clubcode"):
                                                team = value


                                            elif(key=='statId'):
                                                if value in penaltyCodes:

                                                    if team not in Teams:
                                                        Teams[team]=[]
                                                    Teams[team].append(1)
                                                    flag=True
                                            elif key == 'yards' and flag == True:
                                                if team not in TeamPenaltyYards:
                                                    TeamPenaltyYards[team] = []
                                                try:
                                                    if value > 0:
                                                        TeamPenaltyYards[team].append(value)

                                                except TypeError:
                                                    pass
                                                flag = False


    #remove all bullshit clubcodes, these are on nfl.com...no idea why
    for wtf in WTFTeamCodes:
        Teams.pop(wtf,None)
        TeamPenaltyYards.pop(wtf,None)
    #pp.pprint(Teams)

    #Sum up all penalties
    max = 0
    for key, value in Teams.items():
        val = sum(value)
        #print(val)
        if(val > max):
            max = val
            name = key
    print(colored("\t-%s had the most penalties with %s" %(name,max),'green'))
    print(colored("\n\n7:Find the team with the most yards in penalties.",'blue'))
    #Sum up all penalty yardage
    max = 0
    for key, value in TeamPenaltyYards.items():
        val = sum(value)
        if val > max:
            max = val
            name = key
    print(colored("\t-%s has the most yard in penalties with %s yards" %(name,max),'green'))

def findCorrelation():
    import numpy



##############################################################
# FieldGoalStats
# This function solves all the questions related to field goal statistics:
# Longest field goal, Most Field Goals, and most missed field goals. The playerid
# is used to store stats related to each question in a seperate dictionary.  At the
# end, the results are printed to screen
#
# Params:
#    none
# Returns:
#    none
def FieldGoalStats():

    MostMissedFieldGoals={}
    MostFieldGoals ={}

    flag = None
    longest = 0
    path = 'Data/'
    files = getFiles(path)
    files = sorted(files)
    x = 0
    print(colored("\n\n10: Find the longest field goal",'blue'))

    for file in files:
        data = openFileJson(file)
        for gameid, gamedata in data.items():
            if gameid != 'nextupdate':

                for driveid, drivedata in gamedata['drives'].items():

                    if driveid != 'crntdrv':
                        for playid, playdata in drivedata['plays'].items():  # in drives json file

                            for k, play in playdata['players'].items():
                                if (k != '0'):


                                    for i in play:

                                        for key, value in i.items():
                                            #if statid == missed field goals!
                                            if key == 'statId' and value == 69:
                                               if k not in MostMissedFieldGoals.keys():
                                                   MostMissedFieldGoals[k] = []
                                               MostMissedFieldGoals[k].append(1)
                                            #Set flag to collect yardage
                                            if key == 'statId' and value == 70:
                                               flag = True
                                            elif key == 'yards' and flag == True:
                                                try:
                                                    if k not in MostFieldGoals.keys():
                                                        MostFieldGoals[k] = []

                                                    MostFieldGoals[k].append(1)      #always append, always present
                                                    if value > longest:       #Longest Field Goats
                                                        longest = value
                                                        name = k
                                                    flag = False            #set false
                                                except TypeError:
                                                    flag = False
                                                    pass
    #print Longest Field goal
    playerName = AllPlayers.get(name,None)
    print(colored("\t-%s had the longest field goal @ %s yards" % (playerName,longest),'green'))
    #Find Most missed field goals
    #Find who has the most field goals
    most = 0

    print(colored("\n\n11: Who has the most field goals.",'blue'))
    for key,value in MostFieldGoals.items():
        val = sum(value)
        if val > most:
            most = val
            id = key
    name = AllPlayers.get(id, None)
    print(colored("\t-%s has the most field goals of %s sucessful attempts." % (name,most),'green'))

    print(colored("\n\n12: Find who has the most missed field goals",'blue'))
    most = 0
    BiggestLooser ={}
    for key, value in MostMissedFieldGoals.items():
        val = sum(value)
        if val > most:
            most = val
            id = key
    name = AllPlayers.get(id,None)
    print(colored("\t-%s had the most missed field goals for %s times." %(name,most),'green'))

##############################################################
# mostDroppedPasses()
# This function collects all playerids and stats that are related to statid '115'
# The results are stored in a dict by the key playerid. At the end of the function,
# the playerid with the most dropped passes is printed to screen
#
# Params:
#    none
# Returns:
#    none
def findMostDroppedPasses():
    MostDroppedPasses ={}
    flag = None
    max = 0
    path = 'Data/'
    files = getFiles(path)
    files = sorted(files)
    x = 0
    print(colored("\n\n13: Find the most dropped passes.",'blue'))
    for file in files:
        data = openFileJson(file)
        for gameid, gamedata in data.items():
            if gameid != 'nextupdate':

                for driveid, drivedata in gamedata['drives'].items():

                    if driveid != 'crntdrv':
                        for playid, playdata in drivedata['plays'].items():  # in drives json file

                            for k, play in playdata['players'].items():

                                if (k != '0'):


                                    for i in play:

                                        for key, value in i.items():
                                            if key == 'statId' and value == 115:
                                                if k not in MostDroppedPasses.keys():
                                                    MostDroppedPasses[k]=[]
                                                MostDroppedPasses[k].append(1)
    most = 0
    Player ={}

    for k, v in MostDroppedPasses.items():
        value = sum(v)
        if value > most:
            most = value
            id = k
    name = AllPlayers.get(id,None)
    print(colored("\t-%s has the most dropped passes for %s" % (name,most),'green'))



##############################################################
# main()
# This function is the main function of the program. Functions are
# called from within to answer all given questions.
#
# Params:
#    none
# Returns:
#    none
def main():
    #Not related to questions, for easy player name lookup
    getAllPlayerNames()

    #Question 1
    getPlayerTeams()

    #Haven't got the sorting structure down for this question yet
    #Question 2
    #multipleTeams()

    #Question 3
    mostYardsRushedForLoss()

    #Question 4
    mostRushesForLoss()

    #Question 5
    mostPassesforLoss()

    #Question 6 and Question 7
    MostPenalties()

    #Question 10-12
    FieldGoalStats()

    #Question 13
    findMostDroppedPasses()




if __name__ == '__main__':
    main()
