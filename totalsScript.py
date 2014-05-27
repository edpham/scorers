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
   def addGame(self, date, result):
      if date not in self.games:
         score = result[0].split("-")
         score.append(result[1])
         self.games[date] = score
      else:
         print "There is already a game against " + self.name + " for " + date
   
   # getGames()
   # Get the list of games that they've played (in dict form)
   def getGames(self):
      return self.games
      
   # calculateRecord()
   def calculateRecord(self):
      games = self.getGames()
      record = [0, 0, 0]
      for game in games:
         current = games[game]
         if current[2].lower() == "win":
            record[0] = record[0] + 1
         elif current[2].lower() == "loss":
            record[1] = record[1] + 1
         else:
            record[2] = record[2] + 1
      return "-".join([str(x) for x in record])
   
   # calculateGD()
   def calculateGD(self):
      games = self.getGames()
      gd = [0, 0, 0]
      for game in games:
         current = games[game]
         gd[0] = gd[0] + int(current[0])
         gd[1] = gd[1] + int(current[1])
      gd[2] = gd[0] - gd[1]
      return gd
      
# =========
# Methods
# =========

# readFile()
# Reads the scorers.txt file      
def readFile():
   txt = open("scorers.txt", "r")
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
      else:
         scorers.append([line.split()[0], " ".join(line.split()[1:])])
         
   return scorers, games

# processPlayers()
# Processes the data that was extracted from the scorers.txt file
def processPlayers(data):
   results = {}
   season = ""
   date = ""
   
   for line in data:
      if "/" in line and type(line) is str:
         date = line
      elif type(line) is str:
         season = line
      else:
         results = processScorer(line[0], line[1], results, season, date)
         
   return results

# processScorer()
# Processes the data that comes with the scorer (goals, season, date)
def processScorer(goals, scorer, results, season, date):
   if scorer not in results:
      results[scorer] = player(scorer)
   indiv = results[scorer]
   indiv.addGame(season, date, goals)
   results[scorer] = indiv
   return results
   
def processOpponents(data):
   opponents = {}
   for line in data:
      opp = " ".join(line[2][3:])
      if opp not in opponents:
         opponents[opp] = opponent(opp)
      team = opponents[opp]
      team.addGame(line[1], line[2][0:2])
      opponents[opp] = team
      
   return opponents
   
def allTimeScorers(scorers):
   allTime = []
   for scorer in scorers:
      allTime.append((scorers[scorer].getTotal(), scorer))
   allTime = sorted(allTime, key = lambda x: (-x[0], x[1]))
   
   for player in allTime:
      print player[0], '\t', player[1]

# ============
# Main method
# ============
if __name__ == "__main__":
   scorers, games = readFile()
   allScorers = processPlayers(scorers)
   allOpponents = processOpponents(games)
   
   allTimeScorers(allScorers)