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
   
   def addGoalsForGame(self, date, goals):      # Add the number of goals scored for that game and 
                                                # increase total, max
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
   
   def getOpponents(self):
      return self.opponents.keys()
   
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
      self.seasons = {}
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
   
   def addSeasonRecord(self, season, result, GF, GA):
      if season not in self.seasons: self.seasons[season] = [0, 0, 0, 0, 0]
      record = self.seasons[season]
      if result.lower() == "win":
         record[0] = record[0] + 1
      elif result.lower() == "loss":
         record[1] = record[1] + 1
      else:
         record[2] = record[2] + 1
      record[3] = GF + record[3]
      record[4] = GA + record[4]
      self.seasons[season] = record
   
   
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
   
   def getSeasons(self):
      return self.seasons.keys()
      
   def getSeasonRecord(self, season):
      return self.seasons[season]

   def getAllGames(self):
      return self.games
   

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
         opponents[opponent].addSeasonRecord(season, outcome, GF, GA)
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
   allScorers = sorted([(players[player].getPlayerTotal(), player) for player in players], key=
                        lambda x : (-x[0], x[1]))

   rank = 0

   print "All-Time Scorers"
   print "-------------------------------"
   for scorer in allScorers: print "{:3} - {}".format(scorer[0], scorer[1])
   return None


def processMostGoalsInGame(players):
   allScorers = sorted([(players[player].getMostInGame(), player) for player in players], key=
                           lambda x : (-x[0], x[1]))
   print "\nMost Goals in a Game"
   print "--------------------"
   for scorer in allScorers: print "{:3} - {}".format(scorer[0], scorer[1])
   print
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
   
   print "\nGoals In Each Season"
   print "--------------------\n"
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
   return allTime


def processTeamGoals(opp):
   goalsFor = 0
   goalsAga = 0
   for team in opp:
      GF = opp[team].getGoalsFor()
      GA = opp[team].getGoalsAgainst()
      goalsFor = GF + goalsFor
      goalsAga = GA + goalsAga
   return goalsFor, goalsAga


def processFinalStats(opp):
   record = processAllTimeRecord(opp)
   GF, GA = processTeamGoals(opp)
   print '--------------------------------------------------------'
   print '{:>3} - {:>3} - {:>3}  |  ({:>+4}) {:>4} {:>4}  | {:.2f} | {:.2f} | Overall'.format(record[0], record[1],
            record[2], GF-GA, GF, GA, GF/float(sum(record[0:2])), GA/float(sum(record[0:2])))


def processRecordsVsTeams(opp):
   allTeams = sorted([(opp[team].getRecord(), team) for team in opp], key=lambda x : (-x[0][0], 
                                                                        -x[0][2], x[0][1], x[1]))
   print "All-Time Records vs. Teams"
   print "------------------------"
   print '{:>3} - {:>3} - {:>3}  |  ({:^4}) {:>4} {:>4}  | {:>4} | {:>4} | {}'.format("W", "L", "D", "GD", "GF",
                   "GA", "GFA", "GAA", "Team")
   print "-------------------------------------------------------------"
   for team in allTeams:
      w = team[0][0]
      l = team[0][1]
      d = team[0][2]
      print '{:>3} - {:>3} - {:>3}  |  ({:>+#4}) {:>4} {:>4}  | {:.2f} | {:.2f} | {}'.format(w, l, d, 
         opp[team[1]].getGoalDiff(), opp[team[1]].getGoalsFor(), 
         opp[team[1]].getGoalsAgainst(), opp[team[1]].getGoalsFor()/float(sum(team[0][0:2])),
         opp[team[1]].getGoalsAgainst()/float(sum(team[0][0:2])), team[1])
   return None


def processRecordPerSeason(opponents):
   seasons = {}
   for opp in opponents:
      ssns = opponents[opp].getSeasons()
      for season in ssns:
         if season not in seasons: seasons[season] = [0, 0, 0, 0, 0]
         total = seasons[season]
         record = opponents[opp].getSeasonRecord(season)
         total[0] = record[0] + total[0]
         total[1] = record[1] + total[1]
         total[2] = record[2] + total[2]
         total[3] = record[3] + total[3]
         total[4] = record[4] + total[4]
         seasons[season] = total
   
   listOfSeasons = sortSeasons(seasons.keys())
   
   print "\nRecord per Season"
   print "------------------------"
   print '{:>3} - {:>3} - {:>3}  |  ({:^4}) {:>4} {:>4}  | {:>4} | {:>4} | {}'.format("W", "L", "D", "GD", "GF", 
      "GA", "GFA", "GAA", "Season")
   print "--------------------------------------------------------"
   for season in listOfSeasons:
      record = seasons[season]
      print '{:>3} - {:>3} - {:>3}  |  ({:>+4}) {:>4} {:>4}  | {:.2f} | {:.2f} | {}'.format(record[0], record[1],
             record[2], record[3]-record[4], record[3], record[4], record[3]/float(sum(record[0:2])),
             record[4]/float(sum(record[0:2])), season)


def processScorersVsTeams(players):
   opponents = {}
   for player in players:
      teams = players[player].getOpponents()
      for opp in teams:
         goals = int(players[player].getOpponentTotal(opp))
         if opp not in opponents: opponents[opp] = []
         scorers = opponents[opp]
         scorers.append((goals, player))
         opponents[opp] = scorers
   
   print '*** Goals Against Each Opponent ***'
   for opp in opponents:
      print opp, "\n----------------"
      sortedScorers = sorted(opponents[opp], key=lambda x : [-x[0], x[1]])
      if len(sortedScorers) < 5:
         for player in sortedScorers: print "{:>3}  {}".format(player[0], player[1])
      else:
         for num in range(5): print "{:>3}  {}".format(sortedScorers[num][0], 
            sortedScorers[num][1])
      print


def processScoringGraphs(opponents):
   goalsFor = [0 for num in range(11)]
   goalsAga = [0 for num in range(11)]

   for opp in opponents:
      games = opponents[opp].getAllGames()
      for game in games:
         if games[game][0] >= 10:
            goalsFor[10] = goalsFor[10] + 1
         else:
            goalsFor[games[game][0]] = goalsFor[games[game][0]] + 1

         if games[game][1] >= 10:
            goalsAga[10] = goalsAga[10] + 1
         else:
            goalsAga[games[game][1]] = goalsAga[games[game][1]] + 1

   print "\nCounts of Goals Scored in a Game\n------------------------"
   printGraphs(goalsFor)

   print "\nCounts of Goals Conceded in a Game\n------------------------"
   printGraphs(goalsAga)

def printGraphs(goals):
   for num in range(11):
      print "{:>2} | {:>3}".format(num, goals[num])


def processBiggestWinsAndLosses(opponents):
   wins = []
   losses = []
   for opp in opponents:
      games = opponents[opp].getAllGames()
      for date in games:
         data = (opp, date, games[date][0], games[date][1], games[date][0] - games[date][1])
         if games[date][2] == "Win":
            wins.append(data)
         if games[date][2] == "Loss":
            losses.append(data)
   biggestWins = sorted(wins, key=lambda x : (-x[4], -x[2], x[3]))
   biggestLosses = sorted(losses, key=lambda x : (x[4], -x[3], x[2]))
   print "\nBiggest Wins\n---------------"
   for num in range(10):
      print "{:2} -{:2} on {:>10} vs. {}".format(biggestWins[num][2], biggestWins[num][3], 
                                                   biggestWins[num][1], biggestWins[num][0])
   print "\nBiggest Losses\n---------------"
   for num in range(10):
      print "{:2} -{:2} on {:>10} vs. {}".format(biggestLosses[num][2], biggestLosses[num][3], 
                                                   biggestLosses[num][1], biggestLosses[num][0])
   
      

# Other useful methods
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
   processScorersPerSeason(players)
   # processScorersVsTeams(players)
   
   print "****** Team Records ******\n"
   processRecordsVsTeams(opponents)
   processRecordPerSeason(opponents)
   processFinalStats(opponents)
   processScoringGraphs(opponents)
   processBiggestWinsAndLosses(opponents)

if __name__ == "__main__":
   main(sys.argv)