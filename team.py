import seasonSummary

class team(object):
    """
    class team will hold all the team information about a specific 
<<<<<<< HEAD
    team including the team ID, team name, season summary dicitonary and
=======
    team including the team ID, team name, index for matrix addressing, season summary dicitonary and
>>>>>>> Minor update to check home sync
    tournament summary dictionary
    """

    def __init__(self):
        self.id = 0
        self.name = ""
<<<<<<< HEAD
=======
        self.index = -1
>>>>>>> Minor update to check home sync
        self.seasonSummaryDict = {}
        self.tournamentSummaryDict = {}
        return

<<<<<<< HEAD
    def __init__(self, id, name):
        self.id = id
        self.name = name
=======
    def __init__(self, id, name, index):
        self.id = id
        self.name = name
        self.index = index
>>>>>>> Minor update to check home sync
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

<<<<<<< HEAD
=======
    def set_Index(self, index):
        self.index = index
        return

    def getIndex(self):
        retun self.index


>>>>>>> Minor update to check home sync
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

    def getSIError(self):
        return self.seasonSummaryDict[season].getSIError()

    def updateSI(self, season, si):
        """
        function updateSI is used during iteration
        on si.  The difference between the setSI 
        function and theupdateSI function is that 
        update will also update the oldSI value before
        setting the new one.

        input:
            str     season
            float   si
        return:
            null
        """

        self.seasonSummaryDict[season].updateSI(si)
        return

        

