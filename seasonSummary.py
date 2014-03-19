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

        self.index = -1
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

    def add_game(self, pf, pa, oppID):
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
        self.tpf = self.tpf + pf
        self.tpa = self.tpa + pa

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
        if oppID in keyList:
            self.opponents[oppID].append(game)
        else:
            self.opponents[oppID] = []
            self.opponents[oppID].append(game)

        return

    def get_wins(self):
        return self.wins

    def get_losses(self):
        return self.losses

    def get_PF(self):
        return self.tpf

    def get_PA(self):
        return self.tpa

    def get_PD(self):
        return self.pd

    def get_SI(self):
        return self.si

    def set_SI(self, si):
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

    def get_last_n_games(self, n):
        #
        # first check if n > # games
        # if yes return entire season,
        # otherwise retuurn games
        # as tuples ([ 0| 1], oppID)

        totGames = self.wins + self.losses
        gameList = []
        if n > totGames:
            n = totGames

        for i in range(totGames - n, totGames):
            gameList.append((self.recordList[i],self.oppList[i]))

        return gameList

    def set_index(self, index):
        self.index = index
        return

    def get_index(self):
        return self.index

    def get_tot_games(self):
        return self.wins + self.losses

    def get_opponent_list(self):
        return self.oppList






