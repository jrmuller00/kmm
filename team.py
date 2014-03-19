import seasonSummary

class team(object):
    """
    class team will hold all the team information about a specific 
    team including the team ID, team name, season summary dicitonary and
    team including the team ID, team name, index for matrix addressing, season summary dicitonary and
    tournament summary dictionary
    """

    def __init__(self,id=0,name="",index=-1):
        self.id = id
        self.name = name
        self.index = index
        self.seasonSummaryDict = {}
        self.tournamentSummaryDict = {}
        return

    def set_ID(self):
        self.id = id
        return

    def get_ID(self):
        return self.id

    def set_name(self, name):
        self.name = name
        return

    def get_name(self):
        return self.name

    def set_index(self, index):
        self.index = index
        return

    def get_index(self):
        return self.index

    def add_season_game(self, season, pf, pa, oppID):
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
            self.seasonSummaryDict[season].add_game(pf,pa,oppID)
        else:
            seaSum = seasonSummary.seasonSummary()
            seaSum.add_game(pf,pa,oppID)
            self.seasonSummaryDict[season] = seaSum
        return

    def get_SI(self, season):
        return self.seasonSummaryDict[season].get_SI()

    def set_SI(self, season, si):
        try:
            self.seasonSummaryDict[season].set_SI(si)
        except Exception:
            pass
            #print ('No season ' + str(season) + ' key for ' + self.name)
        return

    def get_wins(self, season):
        return self.seasonSummaryDict[season].get_wins()

    def get_losses(self, season):
        return self.seasonSummaryDict[season].get_losses()

    def get_PF(self, season):
        return self.seasonSummaryDict[season].get_PF()

    def get_PA(self, season):
        return self.seasonSummaryDict[season].get_PA()

    def get_PD(self, season):
        return self.seasonSummaryDict[season].get_PD()

    def get_last_n_games(self,season,n):
        try:
            return self.seasonSummaryDict[season].get_last_n_games(n)
        except Exception:
            return []

    def set_season_index(self, season, index):
        self.seasonSummaryDict[season].set_index(index)
        return

    def get_season_index(self, season):
        try:
            return self.seasonSummaryDict[season].get_index()
        except Exception:
            return -1

    def get_tot_season_games(self,season):
        try:
            return self.seasonSummaryDict[season].get_tot_games()
        except Exception:
            return 0

    def get_opponent_list(self, season):
        try:
            return self.seasonSummaryDict[season].get_opponent_list()
        except Exception:
            return []




        

