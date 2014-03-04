import seasonSummary

class team(object):
    """
    class team will hold all the team information about a specific 
    team including the team ID, team name, season summary dicitonary and
    team including the team ID, team name, index for matrix addressing, season summary dicitonary and
    tournament summary dictionary
    """

    def __init__(self):
        self.id = 0
        self.name = ""


        self.index = -1
        self.seasonSummaryDict = {}
        self.tournamentSummaryDict = {}
        return

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __init__(self, id, name, index):
        self.id = id
        self.name = name
        self.index = index
        self.seasonSummaryDict = {}
        self.tournamentSummaryDict = {}
        return

    def setID(self):
        self.id = id
        return

    def getID(self):
        return self.id

    def setName(self, name):
        self.name = name
        return

    def getName(self):
        return self.name

    def set_Index(self, index):
        self.index = index
        return

    def getIndex(self):
        return self.index

    def addSeasonGame(self, season, pf, pa, oppID):
        """
        add information about a season game
       
        Input:
            str     season  Season ID
            int     pf      points scored by team
            int     pa      points scored by opponent
            int     oppID   opponent ID
        
        Return:
            Null
         """
            
        seasonList = list(self.seasonSummaryDict.keys())

        if season in seasonList:
            #
            # already have a seasonSummary object in the list
            # append game info to this object
            self.seasonSummaryDict[season].addGame(pf,pa,oppID)
        else:
            seaSum = seasonSummary()
            seaSum.addGame(pf,pa,oppID)
            seasonSummaryDict[season] = seaSum
        return

    def getSI(self, season):
        return self.seasonSummaryDict[season].getSI()

    def setSI(self, season, si):
        self.seasonSummaryDict[season].setSI(si)
        return

    def getWins(self, season):
        return self.seasonSummaryDict[season].getWins()

    def getLosses(self, season):
        return self.seasonSummaryDict[season].getLosses()

    def getPF(self, season):
        return self.seasonSummaryDict[season].getPF()

    def getPA(self, season):
        return self.seasonSummaryDict[season].getPA()

    def getPD(self, season):
        return self.seasonSummaryDict[season].getPD()



        

