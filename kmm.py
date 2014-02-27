import sys
import getopt
import team
import seasonSummary
import random
import tkinter
import math
from types import *
from tkinter import messagebox
from tkinter import filedialog
import csv


def readTeamList(filename = "teams.csv"):
    """
    function readTeamList will read in the team list from a 
    csv file (default value is teams.csv) The format for the 
    file is:
        
        teamID, team Name

    The data is stored in a dictionary with the team ID as the 
    key value

    Input:
        string  filename

    Return:
        dict    team dictionary
    """

    teamDict = {}

    csvFile = open(filename,"r",newline='')
    csvReader = csv.reader(csvFile,dialect='excel')

    index = -1
    for row in csvReader:
        if index >= 0:
            #
            # first row is the header
            newTeam = team.team(int(row[0]),row[1],index)
            teamDict[int(row[0])] = newTeam
        index = index + 1

    return teamDict


def readSeasonResults(filename = 'regular_season_results.csv'):
    """
    function readSeasonResults will read in the season results from
    a csv file (default value is regular_season_results.csv) The 
    format for the file is:
        
        season,daynum,wteam,wscore,lteam,lscore,wloc,numot

    where 
        season is the season designator (data from 1995-2013)
        daynum is the day number from teh start of the season
        wteam is the winning team ID
        wscore is the winning team score
        lteam is the losing team ID
        lscore is the losing team score
        wloc is the location fro teh winning team 'H' = home, 'A' = away, 'N' = neutral
        numot is the number of overtimes could be an int or 'NA'

    The data is stored as a dictionary of lists where the season is the key value
    and each record is a row in a list

    Input:
        string  filename

    Return:
        dict    season results dictionary
    """

    seasonDict = {}

    csvFile = open(filename,"r",newline='')
    csvReader = csv.reader(csvFile,dialect='excel')

    index = -1
    for row in csvReader:
        if index >= 0:
            #
            # first row is the header
            try:
                if row[0] in list(seasonDict.keys()):
                    #
                    # season exists in dictionary, append this row
                    seasonDict[row[0]].append(row)
                else:
                    #
                    # season doesn't exist yet
                    # create a new list 
                    seasonDict[row[0]] = []
                    seasonDict[row[0]].append(row)
            except Exception:
                print ('Error with dictionary keys')

        index = index + 1

    return seasonDict



def main():
    """
    
    main is the main function for the kmm program.  

    """

    teamDict = {}
    seasonDict = {}
    
    teamDict = readTeamList()
    seasonDict = readSeasonResults()
    print ('Done!')



if __name__ == "__main__":
    main()
