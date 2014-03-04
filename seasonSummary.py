class seasonSummary(object):

    def __init__(self):
        """
        This function will initialize the seasonSummary object

        dict    opponents   - dictionary key = oppID, value = list of wins or losses ['w','l', etc]
        int     wins        - total wins
        int     losses      - total losses
        int     tpf         - total points for
        int     tpa         - total points against
        int     tpd         - total point difference
        float   si          - team strength index
        float   oldSI       - old strength index (used for iteration convergence)
        float   winPercent  - team winning percentage
        """

        self.opponents = {}
        self.wins = 0
        self.losses = 0 
        self.tpf = 0
        self.tpa = 0
        self.tpd = 0
        self.si = 0.0
        self.winPercent = 0.0
        self.recordList = []
        self.pdList = []
        self.oppList = []
        return

    def addGame(self, pf, pa, oppID):
        """
        function addGame will add the game info to the object

        Input:
            pf      - points scored by the team
            pa      - points scored against the team
            oppID   - opponent team ID

        Return:
            null
        """

        self.oppList.append(oppID)
        self.pdList.append(pf-pa)

        #
        # update team record
        if pf > pa:
            self.wins = self.wins + 1
            game = 'w'
            self.recordList.append(1)
        else:
            self.losses = self.losses + 1
            game = 'l'
            self.recordList.append(0)

        #
        # update si based on winning percentage
        if (self.wins + self.losses) > 0:
            self.winPercent = self.wins / (self.wins + self.losses)
            self.si = self.winPercent
        
        keyList = list(self.opponents.keys())
        if oppid in keyList:
            self.opponents[oppID].append(game)
        else:
            self.opponents[oppID] = []
            self.opponents[oppID].append(game)

        return

    def getWins(self):
        return self.wins

    def getLosses(self):
        return self.losses

    def getPF(self):
        return self.tpf

    def getPA(self):
        return self.tpa

    def getPD(self):
        return self.pd

    def getSI(self):
        return self.si

    def setSI(self, si):
        """
        function setSI will set the value for the 
        strength index based on the user supplied value si

        input:
            float   si

        return:
            null
        """
        self.si = si

        return
