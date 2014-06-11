import sys

# Player class
class Player:
   def __init__(self, name):  # Initialize the object (name of player)
      self.name = name
      self.total = 0
      self.most = 0
      self.opponents = {}
      self.seasons = {}
      self.dates = {}
   
   def __str__(self):         # Print out the player object
      return self.name + "\nTotal Goals: " + str(self.total) + \
                        "\nOpponents: " + str(self.opponents) + \
                        "\nSeasons: " + str(self.seasons) + \
                        "\nGames: " + str(self.dates)
   
   
   def addGoalsVsOpp(self, opp, goals):   # Add the number of goals scored against that opponent.
      if opp not in self.opponents: self.opponents[opp] = 0
      self.opponents[opp] = self.opponents[opp] + goals
   
   def addGoalsForSeason(self, season, goals):  # Add the number of goals scored for that season
      if season not in self.seasons: self.seasons[season] = 0
      self.seasons[season] = self.seasons[season] + goals
   
   def addGoalsForGame(self, date, goals):      # Add the number of goals scored for that game and increase total, max
      self.dates[date] = goals
      self.total = self.total + goals
      if self.most < goals: self.most = goals
   
   
   def getPlayerName(self):            # Recall player name
      return self.name
   
   def getPlayerTotal(self):           # Recall player total
      return self.total
   
   def getMostInGame(self):            # Recall the most goals player scored in a game
      return self.most
   
   def getOpponentTotal(self, opp):    # Recall player's goal total against opponent
      return self.opponents[opp]
   
   def getSeasonTotal(self, season):   # Recall player's goal total for a season
      return self.seasons[season]
   
   def getSeasonsPlayed(self):
      return self.seasons.keys()
   
   def getGameTotal(self, date):      # Recall player's game total for a specific date
      return self.dates[date]
   

class Opponent:
   def __init__(self, name):  # Initialize the object
      self.name = name
      self.record = [0, 0, 0]
      self.games = {}
      self.GF = 0
      self.GA = 0
   
   def __str__(self):         # Print out the opponent object
      return self.name + "\nRecord: " + str(self.record) + \
                        "\nGF: " + str(self.GF) + " GA: " + str(self.GA) + \
                        "\n" + str(self.games)
   
   
   def addWin(self):
      self.record[0] = self.record[0] + 1
   
   def addLoss(self):
      self.record[1] = self.record[1] + 1
   
   def addDraw(self):
      self.record[2] = self.record[2] + 1
   
   def addGF(self, goals):
      self.GF = self.GF + goals
   
   def addGA(self, goals):
      self.GA = self.GA + goals
   
   def addGame(self, date, gf, ga, result):
      self.games[date] = [gf, ga, result]
   
   
   def getGoalDiff(self):
      return self.GF - self.GA
   
   def getRecord(self):
      return self.record
   
   def getTeamName(self):
      return self.name
   
   def getGameResult(self, date):
      result = self.games[date]
      return date + ": " + str(result[0]) + "-" + str(result[1]) + " " + str(result[2])
   
   def getGoalsFor(self):
      return self.GF
   
   def getGoalsAgainst(self):
      return self.GA
   

def processData(data, players, opponents):
   season = ""
   date = ""
   opponent = ""
   
   text = open(data, "r")
   
   while True:
      line = text.readline()
      if not line: break
      
      if "--" in line:
         season = " ".join(line.split()[1:])
      elif "/" in line:
         date = line.split()[0]
      elif "Result" in line:
         result = line.split()[1:]
         opponent = " ".join(result[3:])
         GF = int(result[0].split("-")[0])
         GA = int(result[0].split("-")[1])
         outcome = result[1]
         
         if opponent not in opponents: opponents[opponent] = Opponent(opponent) 
         if outcome.lower() == "win":
            opponents[opponent].addWin()
         elif outcome.lower() == "loss":
            opponents[opponent].addLoss()
         else:
            opponents[opponent].addDraw()
         opponents[opponent].addGF(GF)
         opponents[opponent].addGA(GA)
         opponents[opponent].addGame(date, GF, GA, outcome)
      elif len(line) > 2:
         goals = int(line.split()[0])
         name = " ".join(line.split()[1:])
         if name not in players: players[name] = Player(name)
         players[name].addGoalsVsOpp(opponent, goals)
         players[name].addGoalsForSeason(season, goals)
         players[name].addGoalsForGame(date, goals)
   
   text.close()
   return None


def processAllTimeScorers(players):
   allScorers = sorted([(players[player].getPlayerTotal(), player) for player in players], key=lambda x : (-x[0], x[1]))
   print "All-Time Scorers"
   print "----------------"
   for scorer in allScorers: print "{:3} - {}".format(scorer[0], scorer[1])
   return None


def processMostGoalsInGame(players):
   allScorers = sorted([(players[player].getMostInGame(), player) for player in players], key=lambda x : (-x[0], x[1]))
   print "\nMost Goals in a Game"
   print "--------------------"
   for scorer in allScorers: print "{:3} - {}".format(scorer[0], scorer[1])
   return None


def processScorersPerSeason(players):
   seasons = {}
   for player in players:
      for season in players[player].getSeasonsPlayed():
         if season not in seasons:
            seasons[season] = []
         current = seasons[season]
         current.append((players[player].getSeasonTotal(season), player))
         seasons[season] = current
   
   orderedSeasons = sortSeasons(seasons.keys())
   
   for season in orderedSeasons:
      sortedSeason = sorted(seasons[season], key=lambda x : (-x[0], x[1]))
      print season
      print "----------------"
      for player in sortedSeason: print "{:3} - {}".format(player[0], player[1])
      print
   
   return None


def processAllTimeRecord(opp):
   allTime = [0, 0, 0]
   for team in opp:
      record = opp[team].getRecord()
      allTime[0] = allTime[0] + record[0]
      allTime[1] = allTime[1] + record[1]
      allTime[2] = allTime[2] + record[2]
   print "Overall Record: ", "-".join(str(num) for num in allTime), "(" + str(allTime[0] + allTime[1] + allTime[2]) + ")"
   return None


def processTeamGoals(opp):
   goalsFor = 0
   goalsAga = 0
   for team in opp:
      GF = opp[team].getGoalsFor()
      GA = opp[team].getGoalsAgainst()
      goalsFor = GF + goalsFor
      goalsAga = GA + goalsAga
   print "GF:", "{:>4}".format(goalsFor)
   print "GA:", "{:>4}".format(goalsAga)
   print "GD:", "{:>+4}".format(goalsFor - goalsAga)
   print
   return None


def processRecordsVsTeams(opp):
   allTeams = sorted([(opp[team].getRecord(), team) for team in opp], key=lambda x : (-x[0][0], -x[0][2], x[0][1], x[1]))
   print "All-Time Records vs. Teams"
   print "--------------------------"
   for team in allTeams:
      w = team[0][0]
      l = team[0][1]
      d = team[0][2]
      print '{:>2} - {:>2} - {:>2}  ({:>+#4}) -- {team}'.format(w, l, d, opp[team[1]].getGoalDiff(), team=team[1])
   return None


def sortSeasons(seasons):
   orderedSeasons = seasons
   orderedSeasons = [[x.split()[1], x.split()[0]] for x in orderedSeasons]
   for item in orderedSeasons:
      if item[1] == "Winter": 
         item[1] = 1
      elif item[1] == "Spring":
         item[1] = 2
      elif item[1] == "Summer":
         item[1] = 3
      elif item[1] == "Fall":
         item[1] = 4
   
   orderedSeasons = sorted(orderedSeasons, key=lambda x : [x[0], x[1]])
   
   for item in orderedSeasons:
      if item[1] == 1:
         item[1] = "Winter"
      elif item[1] == 2:
         item[1] = "Spring"
      elif item[1] == 3:
         item[1] = "Summer"
      elif item[1] == 4:
         item[1] = "Fall"
   
   orderedSeasons = [" ".join(item[::-1]) for item in orderedSeasons]
   return orderedSeasons


# Main method
def main(args):
   players = {}
   opponents = {}
   
   processData(args[1], players, opponents)
   
   print "****** Individual Records ******\n"
   processAllTimeScorers(players)
   processMostGoalsInGame(players)
   print
   processScorersPerSeason(players)
   
   print "****** Team Records ******\n"
   processAllTimeRecord(opponents)
   processTeamGoals(opponents)
   processRecordsVsTeams(opponents)


if __name__ == "__main__":
   main(sys.argv)