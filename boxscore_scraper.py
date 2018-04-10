import certifi
import urllib3
import json
import requests
import lxml.html
import time
from bs4 import BeautifulSoup
import datetime

"""
This file is used to scrape box scores and statistics from basketball refernce.
The statistics and written to txt files which are named after the season.
Each season and playoff txt file contains a dictionary containing the teams that played in that season.
Each team consists of a list containing information for each game it played.
Each game consists of a dictionary with information such as the teams who played, the scores, the records
of the teams, the team statistics for both teams, and the individual statistics for players on both teams.

The start and end dates for which this program will search for basketball games can be specified at the
beginning of the main function.
"""

def get_dates_between(startDate, endDate):
	#given a start date and end date it ouputs a list of all dates between them
	#includes the start date and end date
	allDates = []
	while abs(endDate - startDate).days > 0:
		allDates.append(startDate)
		startDate = startDate + datetime.timedelta(days = 1)
	allDates.append(endDate)
	return allDates

def url_to_stats(url):
	# returns a dictionary containing the information about a single game
	gameInfo = {}
	homeStats = {}
	awayStats = {}
	homePlayers = {}
	awayPlayers = {}

	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")

	#finds the home and away teams
	title = soup.find_all("title")[0].get_text().split(" Box Score, ")
	teamsPlaying = title[0]
	date = title[1].split(" |")[0]
	awayTeam = teamsPlaying.split(" at ")[0]
	homeTeam = teamsPlaying.split(" at ")[1]
	teamsList = {"away" : awayTeam, "home" : homeTeam}
	gameInfo["teams"] = teamsList


	# find scores and records
	scores = soup.find_all("div", class_="score")
	awayRecord = (scores[0].findNext("div").get_text().split("-"))
	awayWins = int(awayRecord[0])
	awayLosses = int(awayRecord[1])
	homeRecord =(scores[1].findNext("div").get_text().split("-"))
	homeWins = int(homeRecord[0])
	homeLosses = int(homeRecord[1])

	awayScore = int(scores[0].get_text())
	homeScore = int(scores[1].get_text())

	records = {"away losses" : awayLosses, "away wins" : awayWins, "home losses" : homeLosses, "home wins" : homeWins}
	gameInfo["records"] = records
	scoresList = {"away" : awayScore, "home" : homeScore}
	gameInfo["scores"] = scoresList
	
	#creates teams which is a list of all the tables on the webpage
	#the try/except prevents tables with only pictures of the boxscore from being added
	teams = []
	tables = soup.find_all("table")
	for table in tables:
		try:
			tableBody = table.find("tbody")
			tableBody.find_all("tr")
			teams.append(table)
		except:
			pass

	# determines which team each player plays for
	for i in range(len(teams)):
		if i < len(teams)/2:
			memberTeam = awayTeam
		else:
			memberTeam = homeTeam
		# print()
		# print(memberTeam)
		body = teams[i].find("tbody")
		allRows = body.find_all("tr")
		for row in allRows:
			allData = row.find_all("td")
			if len(allData) == 1:
				continue
			
			#eliminates starters and reserves heading
			if len(allData) > 0:
				playerName = row.find("th").get_text()
				# print()
				# print(playerName)
			
			playerDict = {}
			# iterate through each row of data in the box score
			for data in allData:
				# if the statistic is empty because the player did not play
				# could also be empty beacause that statistic was not recorded that year
				# if it is empty, it is recorded as a 0
				if data.get_text() == "":
					stat = 0
					statCategory = data.get("data-stat")
				else:
					# nested try/except ensures the data is stored as the correct type
					try:
						stat = int(data.get_text())
					except:
						try:
							stat = float(data.get_text())
						# the : in the minutes played category means it is originally stored as a string
						except:
							timePlayed = data.get_text()
							minutes = int(timePlayed.split(":")[0])
							seconds = int(timePlayed.split(":")[1])/60
							stat = minutes + seconds
					statCategory = data.get("data-stat")
					# # prints the stat category and stat
					# if type(stat) == int:
					# 	print("%s: %d" % (statCategory, stat))
					# elif type(stat) == float:
					# 	print ("%s: %f" % (statCategory, stat))
					# else:
					# 	print ("%s: %s" % (statCategory, stat))
				if memberTeam == homeTeam:
					try:
						homePlayers[playerName][statCategory] = stat
					except:
						homePlayers[playerName] = {}
						homePlayers[playerName][statCategory] = stat
				else:
					try:
						awayPlayers[playerName][statCategory] = stat
					except:
						awayPlayers[playerName] = {}
						awayPlayers[playerName][statCategory] = stat					

		# at the foot of each table is the team statistics
		foot = teams[i].find("tfoot")
		allRows = foot.find_all("tr")
		# print()
		# print("Team Totals")
		teamDict = {}
		for row in allRows:
			allData = row.find_all("td")
			for data in allData:
				try:
					stat = int(data.get_text())
				except:
					try:
						stat = float(data.get_text())
					except:
						if memberTeam == awayTeam:
							stat = awayScore - homeScore
						else:
							stat = homeScore - awayScore
				statCategory = data.get("data-stat")
				teamDict[statCategory] = stat
				# # prints the stat category and the stat
				# if type(stat) == int:
				# 	print ("%s: %d" % (statCategory, stat))
				# else:
				# 	print ("%s: %.3f" % (statCategory, stat))
		if memberTeam == homeTeam:
			homeStats.update(teamDict)
		else:
			awayStats.update(teamDict)
	
	homeStats["win pct"] = homeWins / (homeWins + homeLosses)
	awayStats["win pct"] = awayWins / (awayWins + awayLosses)

	gameInfo["home stats"] = homeStats
	gameInfo["away stats"] = awayStats
	gameInfo["home players"] = homePlayers
	gameInfo["away players"] = awayPlayers

	return gameInfo

def getSeason(url):
	# given a link to a boxscore, parses the html doc and returns the season
	# season has the format "2012-13"
	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")
	season = soup.find_all("ul")[4].find_all("li")[2].get_text().split(" NBA")[0]
	return season

def day_to_boxscore_url(date):
	#this function takes in a date and outputs the links of all the games on that day
	boxscoreLinks = []
	
	day = date.strftime("%d")
	month = date.strftime("%m")
	year = date.strftime("%Y")
	url = "https://www.basketball-reference.com/boxscores/?month=%s&day=%s&year=%s" % (month,day,year)

	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")
	games = soup.find_all("p", class_="links")
	for game in games:
		links = game.find_all("a")
		for link in links:
			if link.get_text() == "Box Score":
				gameLink = "https://www.basketball-reference.com" + link.get("href")
				boxscoreLinks.append(gameLink)
	
	return boxscoreLinks


def main():
	
	# specifies the start and end date for scraping stats
	firstDate = datetime.date(1975, 7, 16)
	lastDate = datetime.date(1976, 7, 15)

	# gets dates between specified dates
	dates = get_dates_between(firstDate, lastDate)
	for day in dates:
		print(day)
		# converts days to boxscore urls
		boxscoreLinks = day_to_boxscore_url(day)
		# scrapes the data for each box score url
		for url in boxscoreLinks:
			game = url_to_stats(url)
			
			# if connection to website fails, tries again
			gettingSeason = True
			while gettingSeason:
				try:
					season = getSeason(url)
					gettingSeason = False
				except:
					pass

			seasonTextFile = season + ".txt"
			#checks to see if a txt file for the season exists
			try:	
				file = open(seasonTextFile, "r")
				file.close()
				with open(seasonTextFile) as seasonJSONfile:
					currentDictionary = json.load(seasonJSONfile)
			except:
				file = open(seasonTextFile, "w")
				file.close()
				currentDictionary = {}

			gameDictionary = url_to_stats(url)
			gameDictionary["date"] = str(day)

			#checks to see if a team's record is equal to the number of games they've played + 1
			homeTeam = gameDictionary.get("teams").get("home")
			textOutfile = seasonTextFile

			try:
				if (len(currentDictionary.get(homeTeam)) + 1) != gameDictionary.get("records").get("home wins") + gameDictionary.get("records").get("home losses"):
					textOutfile = season +"_playoffs" + ".txt"
			except:
				pass

			# prints the scores for the game
			print("%s (%d) vs %s (%d) in %s" % (gameDictionary.get("teams").get("home"), gameDictionary.get("scores").get("home"), gameDictionary.get("teams").get("away"), gameDictionary.get("scores").get("away"), textOutfile))
			if textOutfile != seasonTextFile:
				# tries to load the playoff text file as the current dictionary
				try:	
					file = open(textOutfile, "r")
					file.close()
					with open(textOutfile) as playoffJSONfile:
						currentDictionary = json.load(playoffJSONfile)
				# if the playoff text file does not exists, creates a new one
				# and creates an empty dictionary
				except:
					file = open(textOutfile, "w")
					file.close()
					currentDictionary = {}


			# checks to see if the list of games for a team is empty
			# creates a new list of games if there is none
			if currentDictionary.get(gameDictionary.get("teams").get("home")) == None:
				currentDictionary[gameDictionary.get("teams").get("home")] = [gameDictionary]
			else:
				currentDictionary.get(gameDictionary.get("teams").get("home")).append(gameDictionary)
			if currentDictionary.get(gameDictionary.get("teams").get("away")) == None:
				currentDictionary[gameDictionary.get("teams").get("away")] = [gameDictionary]
			else:
				currentDictionary.get(gameDictionary.get("teams").get("away")).append(gameDictionary)
			
			# writes to textOutfile
			with open(textOutfile, "w") as outfile:
				json.dump(currentDictionary, outfile)
main()