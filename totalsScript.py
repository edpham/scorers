import sys

# ============
# player Class
# ============
class player:
   def __init__(self, name):
      self.total = 0
      self.seasons = {}
      self.name = name
      
   # addGame()
   # Adds the game and their goal amount under the player. Also updates their total.
   def addGame(self, season, date, goals):
      if season not in self.seasons:
         self.seasons[season] = {}
      currentSeason = self.seasons[season]
      if date not in currentSeason:
         self.total = self.total + int(goals)
         currentSeason[date] = goals
         self.seasons[season] = currentSeason
      else:
         print "There's already a date " + date + " listed for " + self.name

   # getSeasonGoalsTotal()
   # Gets the amount of goals the individual scored for that season.
   def getSeasonGoalsTotal(self, season):
      total = 0
      if season in self.seasons:
         goalsForSeason = self.seasons[season].values()
         for amt in goalsForSeason: total = total + int(amt)
      return total
   
   # getSeasonGamesTotal()
   # Gets the number of games that they scored in a particular season.
   def getSeasonGamesTotal(self, season):
      if season in self.seasons:
         return len(self.seasons[season].keys())
      else:
         return 0
   
   # getMostGoalsInGame()
   # Gets the most goals that they've ever scored in a game.
   def getMostGoalsInGame(self):
      high = 0
      for season in self.seasons:
         for game in self.seasons[season]:
            if self.seasons[season][game] > high:
               high = self.seasons[season][game]
      return high

   # getTotal()
   # Returns the total number of goals the individual has scored.
   def getTotal(self):
      return self.total

   # getSeasons()
   # Returns the seasons that they've scored goals.
   def getSeasons(self):
      return self.seasons.keys()

   # getName()
   # Returns the name of the individual.
   def getName(self):
      return self.name
      

# ===============      
# opponent Class
# ================ 
class opponent:
   def __init__(self, name):
      self.name = name
      self.games = {}
   
   # addGame()
   # Adds the game that the team has played that opponent and the result.
   def addGame(self, date, result, season):
      if season not in self.games:
         self.games[season] = {}
      current = self.games[season]
      if date not in current:
         score = result[0].split("-")
         score.append(result[1])
         current[date] = score
         self.games[season] = current
      else:
         print "There is already a game against " + self.name + " for " + date
   
   # getGames()
   # Get the of seasons that they've played (in dict form)
   def getGames(self):
      return self.games
   
   def getSeasons(self):
      return self.games.keys()

   def getSeasonRecord(self, season):
      if season in self.games:
         record = [0, 0, 0]
         currentSeason = self.games[season]
         for game in currentSeason:
            result = currentSeason[game][2].lower()
            if result == "win":
               record[0] = record[0] + 1
            elif result == "loss":
               record[1] = record[1] + 1
            else:
               record[2] = record[2] + 1
         return record
      else:
         return None

   # calculateRecord()
   def calculateRecord(self):
      games = self.getGames()
      record = [0, 0, 0]
      for season in games:
         currentSeason = games[season]
         for game in currentSeason:
            current = currentSeason[game]
            if current[2].lower() == "win":
               record[0] = record[0] + 1
            elif current[2].lower() == "loss":
               record[1] = record[1] + 1
            else:
               record[2] = record[2] + 1
      
      return record
   
   # calculateGD()
   def calculateGD(self):
      games = self.getGames()
      gd = [0, 0, 0]
      for season in games:
         currentSeason = games[season]
         for game in currentSeason:
            score = currentSeason[game]
            gd[0] = gd[0] + int(score[0])
            gd[1] = gd[1] + int(score[1])
      gd[2] = gd[0] - gd[1]
      return gd
      
# =========
# Methods
# =========

def main(argv):
   scorers, games = readFile(argv)
   allScorers, allSeasons = processPlayers(scorers)
   allOpponents = processOpponents(games)
   
   allTimeScorers(allScorers)
   goalsPerSeason(allScorers, allSeasons)
   goalsInAGame(allScorers)
   allTimeRecords(allOpponents)
   recordPerSeason(allOpponents, allSeasons)
   totalRecord(allOpponents)
   totalGoals(allOpponents)

# readFile()
# Reads the scorers.txt file      
def readFile(argv):
   txt = open(argv[1], "r")
   season = ""
   date = ""
   scorers = []
   games = []
   
   while True:
      line = txt.readline()
      if not line: break
      if "--" in line:
         season = line.split()[1] + " " + line.split()[2]
         scorers.append(season)
      elif "/" in line:
         date = line.split()[0]
         scorers.append(date)
      elif "Result" in line:
         result = [season]
         result.append(date)
         result.append(line.split()[1:])
         games.append(result)
      elif len(line.split()) > 1:
         scorers.append([line.split()[0], " ".join(line.split()[1:])])
      else:
         None
         
   return scorers, games

# processPlayers()
# Processes the data that was extracted from the scorers.txt file
def processPlayers(data):
   results = {}
   seasons = []
   season = ""
   date = ""
   
   for line in data:
      if "/" in line and type(line) is str:
         date = line
      elif type(line) is str:
         season = line
         seasons.append(line)
      else:
         results = processScorer(line[0], line[1], results, season, date)
         
   return results, seasons

# processScorer()
# Processes the data that comes with the scorer (goals, season, date)
def processScorer(goals, scorer, results, season, date):
   if scorer not in results:
      results[scorer] = player(scorer)
   indiv = results[scorer]
   indiv.addGame(season, date, goals)
   results[scorer] = indiv
   return results

# processOpponents()
def processOpponents(data):
   opponents = {}
   for line in data:
      opp = " ".join(line[2][3:])
      if opp not in opponents:
         opponents[opp] = opponent(opp)
      team = opponents[opp]
      team.addGame(line[1], line[2][0:2], line[0])
      opponents[opp] = team
         
   return opponents

# goalsPerSeason()   
def goalsPerSeason(scorers, seasons):
   for season in seasons:
      currentSeason = []
      for scorer in scorers:
         total = scorers[scorer].getSeasonGoalsTotal(season)
         if total > 0: currentSeason.append((total, scorer))
      currentSeason = sorted(currentSeason, key = lambda x: (-x[0], x[1]))
      print season, "\n================="
      for player in currentSeason: print str(player[0]) + "\t" + player[1]
      print

# goalsInAGame()
def goalsInAGame(scorers):
   totals = []
   for scorer in scorers:
      goals = scorers[scorer].getMostGoalsInGame()
      totals.append((goals, scorer))
   
   totals = sorted(totals, key = lambda x: (-int(x[0]), x[1]))
   print "Most Goals in a Single Game"
   print "==========================="
   for total in totals: print total[0], "\t", total[1]
      

# allTimeScorers()
# Processes and outputs the all time scorers for the team.
def allTimeScorers(scorers):
   allTime = []
   for scorer in scorers:
      allTime.append((scorers[scorer].getTotal(), scorer))
   allTime = sorted(allTime, key = lambda x: (-x[0], x[1]))
   
   print "All Time Scorers"
   print "================"
   for player in allTime: 
      if player[0] > 100:
         print player[0], '\t', player[1]
      else:
         print player[0], '\t\t', player[1]
   print

# allTimeRecords()
# Processes the all-time records against each opponent   
def allTimeRecords(opponents):
   allTime = []
   for opp in opponents:
      record = opponents[opp].calculateRecord()
      gd = opponents[opp].calculateGD()
      allTime.append((opp, record[0] * 3 + record[2], record[0], record[1], record[2], gd))

   print "\nAll Time Records"
   print "================"
   allTime = sorted(allTime, key = lambda x: (-x[1], -x[2], -x[4], x[3], x[0]))
   for opp in allTime: print "-".join([str(x) for x in opp[2:5]]), '\t', opp[5], '\t', opp[0]

# recordPerSeason()
def recordPerSeason(opponents, seasons):
   allSeasons = []
   for season in seasons:
      record = [0, 0, 0]
      for opp in opponents:
         currentSeason = opponents[opp].getSeasonRecord(season)
         if currentSeason != None:
            for x in range(len(record)): record[x] = currentSeason[x] + record[x]
      allSeasons.append((season, "-".join([str(x) for x in record])))
   
   print "\nRecords For Each Season"
   print "========================="
   for season in allSeasons:
      print season[1] + "\t" + season[0]

# totalRecord()   
def totalRecord(opponents):
   total = [0, 0, 0]
   for opp in opponents:
      record = opponents[opp].calculateRecord()
      for x in range(len(total)):
         total[x] = total[x] + record[x]
   print "\nOverall record:", "-".join([str(x) for x in total])

# totalGoals()   
def totalGoals(opponents):
   total = [0, 0, 0]
   for opp in opponents:
      goals = opponents[opp].calculateGD()
      for x in range(3):
         total[x] = total[x] + goals[x]
   print "Overall goal differential:", "-".join([str(x) for x in total]) + "\n"

# ============ 
# Main method
# ============
if __name__ == "__main__":
   main(sys.argv)