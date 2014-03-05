import sys
import getopt
import team
import seasonSummary
import random
import tkinter
import math
from scipy.sparse import *
from scipy import *
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


def makeMatrix(teamDict, seasonDict):
    """
    function makeMatricies will create sparse matricies based on the data
    in the seasonDict dictionary.  The matricies are as follows:

        wlMatrix: win loss matrix where 1 indicates win and 0 indicates loss
        pdMatrix: point differential matrix where entry [i,j] indicates the point differential in a game between team i and team j (score for team i - score for team j)
        pfMatrix: points for matrix where entry [i,j] indicates teh points scored by team i on team j
        paMatrix: points against matrix where entry [i,j] indicates the points scored against team i by team j

    Note that the matricies are bundled in respective dictionaries with the season designator as a key

    Input:
        dict    seasonDict  dictionary storing all season results

    Return:
        tuple   (wlDict, pdDict, pfDict, paDict) dictionaries with matricies
    """
    wlDict = {}
    pdDict = {}
    pfaDict = {}    
    numTeams = len(teamDict.keys())

    seasons = list(seasonDict.keys())

    wlRow = []
    wlCol = []
    wlData = []
    pdRow = []
    pdCol = []
    pdData = []
    pfaRow = []
    pfaCol = []
    pfaData = []

    for season in seasons:

        wlRow.clear()
        wlCol.clear()
        wlData.clear()
        pdRow.clear()
        pdCol.clear()
        pdData.clear()
        pfaRow.clear()
        pfaCol.clear()
        pfaData.clear()

        results = seasonDict[season]
        for game in results:
            wTeam = teamDict[int(game[2])].getIndex()
            wScore = int(game[3])
            lTeam = teamDict[int(game[4])].getIndex()
            lScore = int(game[5])

            #
            # append 1 to (lTeam,wteam)
            wlRow.append(lTeam)
            wlCol.append(wTeam)
            wlData.append(1)

            #
            # append point difference for at (lTeam,wTeam) 
            pdRow.append(lTeam)
            pdCol.append(wTeam)
            pdData.append(wScore -lScore)

            #
            # append points scored on lTeam at (lTeam,wTeam) and points score on wTeam at (wTeam,lTeam)
            pfaRow.append(lTeam)
            pfaCol.append(wTeam)
            pfaData.append(wScore)

            pfaRow.append(wTeam)
            pfaCol.append(lTeam)
            pfaData.append(lScore)


        wlMatrix = coo_matrix((wlData, (wlRow, wlCol)),shape=(numTeams,numTeams))
        rowi = wlMatrix.getrow(78)

        
        pdMatrix = coo_matrix((pdData, (pdRow, pdCol)),shape=(numTeams,numTeams))
        pfaMatrix = coo_matrix((pfaData, (pfaRow, pfaCol)),shape=(numTeams,numTeams))
        

        wlDict[season] = wlMatrix
        pdDict[season] = pdMatrix
        pfaDict[season] = pfaMatrix

    return 




def main():
    """
    
    main is the main function for the kmm program.  

    """

    teamDict = {}
    seasonDict = {}
    
    teamDict = readTeamList()
    seasonDict = readSeasonResults()
    makeMatrix(teamDict, seasonDict)
    print ('Done!')



if __name__ == "__main__":
    main()
