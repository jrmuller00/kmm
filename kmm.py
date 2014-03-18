import sys
import getopt
import team
import seasonSummary
import random
import tkinter
import math
from scipy.sparse import *
from scipy.sparse.linalg import *
from scipy import *
from types import *
import numpy as np
import scipy as sp
from tkinter import messagebox
from tkinter import filedialog
import csv


def read_team_list(filename = "teams.csv"):
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


def read_season_results(filename = 'regular_season_results.csv'):
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


def make_matrix(teamDict, seasonDict, alphas, ntrend=5):
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
    sMatrixDict = {}
 
    numTeams = len(teamDict.keys())

    seasons = list(seasonDict.keys())
    #
    # win loss mattrix
    wlRow = []
    wlCol = []
    wlData = []

    #
    # point difference matrix
    pdRow = []
    pdCol = []
    pdData = []

    #
    # points for/against matrix
    pfaRow = []
    pfaCol = []
    pfaData = []

    #
    # close game matrix
    cgRow = []
    cgCol = []
    cgData = []

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
        cgRow.clear()
        cgCol.clear()
        cgData.clear()

        #
        # load data to season summary objects
        # this is used to find teams that did not
        # play in the current season

        results = seasonDict[season]

        results = seasonDict[season]
        for game in results:
            wTeamID = int(game[2])
            lTeamID = int(game[4])
            wTeam = teamDict[wTeamID].get_index()
            wScore = int(game[3])
            lTeam = teamDict[lTeamID].get_index()
            lScore = int(game[5])

            #
            # add game info to team obects

            teamDict[wTeamID].add_season_game(season,wScore,lScore,lTeamID)
            teamDict[lTeamID].add_season_game(season,lScore,wScore,wTeamID)

        #
        # now loop thru teams and set matrix index
        index = 0
        for team in teamDict.keys():
            if teamDict[team].get_tot_season_games(season) > 0:
                teamDict[team].set_season_index(season,index)
                index = index + 1

        numSeasonTeams = index

        for game in results:
            wTeamID = int(game[2])
            lTeamID = int(game[4])
            wTeam = teamDict[wTeamID].get_season_index(season)
            wScore = int(game[3])
            lTeam = teamDict[lTeamID].get_season_index(season)
            lScore = int(game[5])

            #
            # add game info to team obects

            teamDict[wTeamID].add_season_game(season,wScore,lScore,lTeamID)
            teamDict[lTeamID].add_season_game(season,lScore,wScore,wTeamID)

            #
            # append 1 to (lTeam,wteam)
            wlRow.append(lTeam)
            wlCol.append(wTeam)
            wlData.append(1.0)

            #
            # append point difference for at (lTeam,wTeam) 
            pdRow.append(lTeam)
            pdCol.append(wTeam)
            pdData.append(float(wScore -lScore))

            if wScore - lScore < 5:
                cgRow.append(lTeam)
                cgCol.append(wTeam)
                cgData.append(1.0)

            #
            # append points scored on lTeam at (lTeam,wTeam) and points score on wTeam at (wTeam,lTeam)
            pfaRow.append(lTeam)
            pfaCol.append(wTeam)
            pfaData.append(float(wScore))

            pfaRow.append(wTeam)
            pfaCol.append(lTeam)
            pfaData.append(float(lScore))

        #
        # now get the last n gmae trend for the teams
        
        #
        # close game matrix
        trendRow = []
        trendCol = []
        trendData = []
        trendList = []
        for team in teamDict:
            trendList = teamDict[team].get_last_n_games(season, ntrend)
            
            for gameTuple in trendList:
                (wl, oppID) = gameTuple
                if wl == 0:
                    trendRow.append(teamDict[team].get_season_index(season))
                    trendCol.append(teamDict[oppID].get_season_index(season))
                    trendData.append(1.0)

        wlMatrix = coo_matrix((wlData, (wlRow, wlCol)),shape=(numSeasonTeams,numSeasonTeams))
        wlMatrix_csr = wlMatrix.tocsr()
        wlMatrix_norm = normalize_matrix(wlMatrix_csr)
        wlMatrix_norm = check_zero_rows(wlMatrix_norm)
               
        pdMatrix = coo_matrix((pdData, (pdRow, pdCol)),shape=(numSeasonTeams,numSeasonTeams))
        pdMatrix_csr = pdMatrix.tocsr()
        pdMatrix_norm = normalize_matrix(pdMatrix_csr)
        pdMatrix_norm = check_zero_rows(pdMatrix_norm)

        pfaMatrix = coo_matrix((pfaData, (pfaRow, pfaCol)),shape=(numSeasonTeams,numSeasonTeams))
        pfaMatrix_csr = pfaMatrix.tocsr()
        pfaMatrix_norm = normalize_matrix(pfaMatrix_csr)
        pfaMatrix_norm = check_zero_rows(pfaMatrix_norm)

        cgMatrix = coo_matrix((cgData, (cgRow, cgCol)),shape=(numSeasonTeams,numSeasonTeams))
        cgMatrix_csr = cgMatrix.tocsr()
        cgMatrix_norm = normalize_matrix(cgMatrix_csr)
        cgMatrix_norm = check_zero_rows(cgMatrix_norm)

        trendMatrix = coo_matrix((trendData, (trendRow, trendCol)),shape=(numSeasonTeams,numSeasonTeams))
        trendMatrix_csr = trendMatrix.tocsr()
        trendMatrix_norm = normalize_matrix(trendMatrix_csr)
        trendMatrix_norm = check_zero_rows(trendMatrix_norm)    



        finalMatrix_csr = alphas[0] * wlMatrix_norm + alphas[1] * pdMatrix_norm \
            + alphas[2] * pfaMatrix_norm + alphas[3] * cgMatrix_norm \
            + alphas[4] * trendMatrix_norm

        sMatrixDict[season] = finalMatrix_csr

    return sMatrixDict


def normalize_matrix(matrix):
    """
    normalize_matrix accepts a csr sparse matrix and normalizes the
    rows

    Input:
        sparse.csr_matrix   matrix

    Return:
        sparse.csr_matrix   row normalized matrix

    """

    (numRows, numCols) = matrix.shape

    for i in range(0,numRows):
        row = matrix.getrow(i)
        rowSum = 0
        for k in range(len(row.data)):
            rowSum = rowSum + row.data[k]

        if rowSum != 0:
            for j in range(matrix.indptr[i],matrix.indptr[i+1]):
                value = matrix.data[j]
                value = value / rowSum
                matrix.data[j] = value

    return matrix


def  check_zero_rows(csrMatrix):
    """
    check_zero_row will check if there is a zero row and 
    if so add 1/rows to each element in that row
    """

    (rows,cols) = csrMatrix.shape

    for i in range(rows):
        if csrMatrix.indptr[i] == csrMatrix.indptr[i+1]:
            rowData = []
            colData = []
            mData = []
            for k in range(rows):
                rowData.append(i)
                colData.append(k)
                mData.append(1.0/float(rows))

            cooMatrix = coo_matrix((mData, (rowData, colData)),shape=(rows,cols))
            csrMatrix = csrMatrix + cooMatrix.tocsr()

    return csrMatrix

def get_dominant_eigen(eigvals, eigvec):

    numEigVals = len(eigvals.real)
    domIndex = 0
    for i in range(numEigVals):
        if math.fabs(1.0 - eigvals.real[i]) < 1e-3:
            domIndex = i

    (rows,cols) = eigvec.shape
    domEig = []
    sum = 0.0
    for i in range(rows):
        sum = sum + eigvec.real[i][domIndex]
        domEig.append(eigvec.real[i][domIndex])

    for i in range(rows):
        domEig[i] = math.fabs(domEig[i] / sum)


    return domEig

def compare_ratings(tourneyresults, teamDict, skiplist):

    seasonPredictions = {}
    sum = 0.0
    count = 0
    for season in tourneyresults.keys():
        if season not in (skiplist):
            results = tourneyresults[season]
            totGames = 0
            numRight = 0
            for game in results:
                wTeamID = int(game[2])
                lTeamID = int(game[4])
                wTeam = teamDict[wTeamID].get_season_index(season)
                lTeam = teamDict[lTeamID].get_season_index(season)
                if teamDict[wTeamID].get_SI(season) > teamDict[lTeamID].get_SI(season):
                    numRight = numRight + 1
                totGames = totGames + 1
            print ('Season: ' + str(season) + ' Correct %: ' + str(100.0 * numRight / totGames))
            sum = sum + (numRight / totGames)
            count = count + 1

    return sum / count


def main():
    """
    
    main is the main function for the kmm program.  

    arguments:
        -a [list of alphas]     :   list of alphas to use for calculations
        -b [list of seasons]    :   list of seasons to calculate ratings only and bypass results comparison
        -e [filename]           :   tourney seeds               default is tourney_seeds.csv
        -f [alphaSteps]         :   number of alpha steps for simulation
        -h                      :   help on running the code
        -l [filename]           :   tourney slots               default is tourney_slots.csv
        -o [filename]           :   tourney results             default is tourney_results.csv
        -r [filename]           :   regular season results      default is regular_season_results.csv
        -s [filename]           :   seasons                     default is seasons.csv
        -t [filename]           :   team names/ids              default is teams.csv
  
    """
    teamsFile = ''
    regularSeasonResultsFile = ''
    seasonsFile = ''
    tourneySlotsFile = ''
    tourneySeedsFile = ''
    tourneyResultsFile = ''
    alphaList = []
    numAlphas = 1
    alphaSteps = 1
    delAlpha = 0.0
    skipList = []
    writeAlphaData = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:b:e:f:hl:o:r:st:y:",["help","filename="])
    except getopt.error as msg:
        print (msg)
        print ("for help use --help")
        sys.exit(2)

    for o, arg in opts:
#        print (o, arg)
        if o == "-a":
            tokens = arg.split(',')
            for alpha in tokens:
                alphaList.append(float(alpha))
            #
            # check for sum to 1.0
            sum = 0.0
            for alpha in alphaList:
                sum = alpha + sum

            if math.fabs(1.0 - sum) > 1e-4:
                print ('alpha list does not sum to 1.0, please try again')
                sys.exit(2)
        if o == '-b':
            tokens = arg.split(',')
            for skip in tokens:
                skipList.append(skip)

        if o == "-e":
            tourneySeedsFile = arg
        if o == "-f":
            alphaSteps = int(arg)
            if alphaSteps > 2:
                delAlpha = 1.0 / (alphaSteps - 1)
                numAlphas = 5
                alphaFile = open('alphadata.txt',mode='w')
                writeAlphaData = True
            else:
                print('Need more alpha steps')
                sys.exit(2)

        if o == "-h":
            print ("python kmm.py")
        if o == "-l":
            tourneySlotsFile = arg
        if o == "-o":
            tourneyResultsFile = arg
        if o == "-r":
            regularSeasonResultsFile = arg
        if o == "-s":
            seasonsFile = arg
        if o == "-t":
            teamsFile = arg




    if len(alphaList) == 0:
        alphaList = [0.75,0.125,0.125,0.0,0.0]
    teamDict = {}
    seasonDict = {}
    sMatrixDict = {}
    ratingsDict = {}
    standingsDict = {}
    tourneyDict = {}

    
    if teamsFile == '':
        teamDict = read_team_list()
    else:
        teamDict = read_team_list(teamsFile)
    if regularSeasonResultsFile == '':
        seasonDict = read_season_results()
    else:
        seasonDict = read_season_results(regularSeasonResultsFile)

    

    for i in range(numAlphas):
        if numAlphas > 1:
            alphaList[i] = 0.0
        for j in range(alphaSteps):
            if numAlphas > 1:
                sum = 1.0 - alphaList[i]
                for k in range(numAlphas):
                    if k != i:
                        alphaList[k] = sum / (numAlphas - 1.0)
            sMatrixDict = make_matrix(teamDict, seasonDict, alphaList)
            for key in sMatrixDict.keys():
                #dense_Matrix = sMatrixDict[key].todense()
                (rows,cols) = sMatrixDict[key].shape
                if rows <= 6:
                    rank=rows-2
                else:
                    rank=6
                evalsp, evecsp = eigs(sMatrixDict[key].transpose(),k=rank)
                #evals, levecs, revecs = sp.linalg.eig(dense_Matrix,left=True)
                ratingsDict[key] = get_dominant_eigen(evalsp, evecsp)
                standingsList = []
                for team in teamDict.keys():
                    teamIndex = teamDict[team].get_season_index(key)
                    if teamIndex >= 0:
                        standingsList.append((teamDict[team].get_name(),1000*ratingsDict[key][teamIndex]))
                        teamDict[team].set_SI(key,1000*ratingsDict[key][teamIndex])

                standingsList = sorted(standingsList, key=lambda listitem: listitem[1],reverse=True)
                standingsDict[key] = standingsList
            tourneyDict = read_season_results('tourney_results.csv')
            for k in range(numAlphas):
                print('alpha[' + str(k) + '] = ' + str(alphaList[k]) + '  ')
            print ('\n')
            overallScore = compare_ratings(tourneyDict, teamDict, skipList)
            if writeAlphaData == True:
                for k in range(numAlphas):
                    alphaFile.write('{0: >6.5e} '.format(alphaList[k]))
                alphaFile.write('{0: >6.5e}\n'.format(overallScore))
            alphaList[i] = alphaList[i] + delAlpha
    print ('Done!')



if __name__ == "__main__":
    main()
 