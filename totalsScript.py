# player() Object
class player:
   def __init__(self):
      self.total = 0
      self.seasons = {}
      
   def addGameToSeason(self, season, date, goals):
      if season not in self.seasons:
         self.seasons[season] = {}
      currentSeason = self.seasons[season]
      if date not in currentSeason:
         self.total = self.total + int(goals)
         currentSeason[date] = goals
         self.seasons[season] = currentSeason
      else:
         print "There's already a date listed for this player."

   def getTotal(self):
      return self.total

   def getSeasons(self):
      return self.seasons.keys()
      
   def getSeasonGoalsTotal(self, season):
      total = 0
      if season in self.seasons:
         goalsForSeason = self.seasons[season].values()
         for amt in goalsForSeason: total = total + int(amt)
      return total
   
   def getSeasonGamesTotal(self, season):
      if season in self.seasons:
         return len(self.seasons[season].keys())
      else:
         return 0

# readFile()
# Reads the scorers.txt file      
def readFile():
   scorers = open("scorers.txt", "r")
   season = ""
   date = ""
   data = []
   
   while True:
      line = scorers.readline()
      if not line: break
      if line.split()[0] == "--":
         data.append(line.split()[1] + " " + line.split()[2])
      elif len(line.split()) == 1:
         data.append(line.split()[0])
      else:
         data.append([line.split()[0], line.split()[1] + " " + line.split()[2]])
         
   return data
   
def processData(data):
   results = {}
   season = ""
   date = ""
   for line in data:
      if "/" in line:
         date = line
      elif len(line) == 2:
         results = processScorer(line[0], line[1], results, season, date)
      else:
         season = line

   return results

def processScorer(goals, scorer, results, season, date):
   if scorer not in results:
      results[scorer] = player()
   indiv = results[scorer]
   indiv.addGameToSeason(season, date, goals)
   results[scorer] = indiv
   return results

if __name__ == "__main__":
   data = readFile()
   results = processData(data)