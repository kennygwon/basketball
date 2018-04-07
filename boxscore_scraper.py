import certifi
import urllib3
import json
import requests
import lxml.html
import time
from bs4 import BeautifulSoup
import datetime


def get_dates_between(startDate, endDate):
	#given a start date and end date it ouputs a list of all dates between them
	#includes the start date and end date
	allDates = []
	while abs(endDate - startDate).days > 0:
		allDates.append(startDate)
		startDate = startDate + datetime.timedelta(days = 1)
		# print("startDate: ")
		# print(startDate)
		# print("endDate: ")
		# print(endDate)
	allDates.append(endDate)
	return allDates

def url_to_stats(url):
	#returns a dictionary containing the information about a single game
	# allPlayers = {}
	# emptyPlayerStats = {}
	gameInfo = {}
	homeStats = {}
	awayStats = {}
	homePlayers = {}
	awayPlayers = {}

	#http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
	#r = http.request("GET", "https://www.basketball-reference.com/boxscores/201803120OKC.html")
	# url = "https://www.basketball-reference.com/boxscores/201803120OKC.html"
	# url = "https://www.basketball-reference.com/boxscores/201710210CLE.html"


	# url = "https://www.basketball-reference.com/boxscores/201711070POR.html"
	# url = "https://www.basketball-reference.com/boxscores/201704150CLE.html"
	# url = "https://www.basketball-reference.com/boxscores/201401150ORL.html"


	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")


	# print(soup.prettify())

	#finds the home and away teams
	#hard-coded
	title = soup.find_all("title")[0].get_text().split(" Box Score, ")
	teamsPlaying = title[0]
	date = title[1].split(" |")[0]
	awayTeam = teamsPlaying.split(" at ")[0]
	homeTeam = teamsPlaying.split(" at ")[1]
	teamsList = {"away" : awayTeam, "home" : homeTeam}
	gameInfo["teams"] = teamsList




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

	# print()
	# print("home team: %s %d" % (homeTeam, homeScore))
	# print("away team: %s %d" % (awayTeam, awayScore))
	
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
			for data in allData:
				if data.get_text() == "":
					stat = 0
					statCategory = data.get("data-stat")
				else:
					try:
						stat = int(data.get_text())
					except:
						try:
							stat = float(data.get_text())
						except:
							timePlayed = data.get_text()
							minutes = int(timePlayed.split(":")[0])
							seconds = int(timePlayed.split(":")[1])/60
							# timePlayed = datetime.datetime.strptime(data.get_text(), "%M:%S")
							# minutes = timePlayed.minute
							# seconds = timePlayed.second/60
							stat = minutes + seconds
					statCategory = data.get("data-stat")
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

				# playerDict[statCategory] = stat
			# if memberTeam == homeTeam:
				# homePlayers[playerName] = playerDict
			# else:
				# awayPlayers[playerName] = playerDict
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
	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")
	season =soup.find_all("ul")[4].find_all("li")[2].get_text().split(" NBA")[0]
	return season
	# print(soup.prettify())


def day_to_boxscore_url(date):
	#this function takes in a date and outputs the links of all the games on that day
	boxscoreLinks = []
	
	day = date.strftime("%d")
	month = date.strftime("%m")
	year = date.strftime("%Y")
	url = "https://www.basketball-reference.com/boxscores/?month=%s&day=%s&year=%s" % (month,day,year)

	# url = "https://www.basketball-reference.com/boxscores/?month=03&day=18&year=2018"
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
	# print(today())

	today = datetime.date.today()
	lastDate = datetime.date.today()
	
	firstDate = datetime.date(2001, 7, 16)
	lastDate = datetime.date(2016, 7, 15)

	# lastDate = datetime.date(today.year, 3, 20)
	# firstDate = datetime.date(2018, 3, 20)

	# url = "https://www.basketball-reference.com/boxscores/199303240PHI.html"
	# url_to_stats(url)

	dates = get_dates_between(firstDate, lastDate)
	for day in dates:
		print()
		print(day)
		boxscoreLinks = day_to_boxscore_url(day)
		for url in boxscoreLinks:
			game = url_to_stats(url)

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
					print(len(currentDictionary.get(homeTeam)))
					print(gameDictionary.get("records").get("home wins"))
					print(gameDictionary.get("records").get("home losses"))
			except:
				pass

			print("%s (%d) vs %s (%d) in %s" % (gameDictionary.get("teams").get("home"), gameDictionary.get("scores").get("home"), gameDictionary.get("teams").get("away"), gameDictionary.get("scores").get("away"), textOutfile))
			# print(textOutfile)
			if textOutfile != seasonTextFile:
				try:	
					file = open(textOutfile, "r")
					file.close()
					with open(textOutfile) as playoffJSONfile:
						currentDictionary = json.load(playoffJSONfile)
				except:
					file = open(textOutfile, "w")
					file.close()
					currentDictionary = {}


			#checks to see if the list of games for a team is empty
			if currentDictionary.get(gameDictionary.get("teams").get("home")) == None:
				currentDictionary[gameDictionary.get("teams").get("home")] = [gameDictionary]
			else:
				currentDictionary.get(gameDictionary.get("teams").get("home")).append(gameDictionary)
			if currentDictionary.get(gameDictionary.get("teams").get("away")) == None:
				currentDictionary[gameDictionary.get("teams").get("away")] = [gameDictionary]
			else:
				currentDictionary.get(gameDictionary.get("teams").get("away")).append(gameDictionary)
			
			
			with open(textOutfile, "w") as outfile:
				json.dump(currentDictionary, outfile)






	


	# oldDictionary = url_to_stats(url)
	# print(oldDictionary.get("home players").get("Jim Eakins"))
	# print(url_to_stats(url).get("home players").get("C.J. McCollum").get("off_rtg"))


	# allPlayers = {}
	# emptyPlayerStats = {}



	# #http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
	# #r = http.request("GET", "https://www.basketball-reference.com/boxscores/201803120OKC.html")
	# url = "https://www.basketball-reference.com/boxscores/201803120OKC.html"
	# # url = "https://www.basketball-reference.com/boxscores/201710210CLE.html"

	# response = requests.get(url)
	# soup = BeautifulSoup(response.content, "html.parser")

	# #print(soup.prettify())

	# #finds the home and away teams
	# #hard-coded
	# title = soup.find_all("title")[0].get_text().split(" Box Score, ")
	# teamsPlaying = title[0]
	# date = title[1].split(" |")[0]
	# awayTeam = teamsPlaying.split(" at ")[0]
	# homeTeam = teamsPlaying.split(" at ")[1]

	# scores = soup.find_all("div", class_="score")
	# awayScore = int(scores[0].get_text())
	# homeScore = int(scores[1].get_text())
	# # print("home team: %s %d" % (homeTeam, homeScore))
	# # print("away team: %s %d" % (awayTeam, awayScore))

	
	# teams = soup.find_all("tbody")
	# for i in range(len(teams)):
	# 	if i % 2 == 0:
	# 		memberTeam = awayTeam
	# 	else:
	# 		memberTeam = homeTeam
	# 	# print()
	# 	# print(memberTeam)
	# 	allRows = teams[i].find_all("tr")
	# 	for row in allRows:
	# 		allData = row.find_all("td")
	# 		#eliminates starters and reserves heading
	# 		if len(allData) > 0:
	# 			playerName = row.find("th").get_text()
	# 			# print()
	# 			# print(playerName)
			
	# 		if len(allData) == 1:
	# 			print("DNP")

	# 		for data in allData:
	# 			try:
	# 				stat = int(data.get_text())
	# 			except:
	# 				stat = data.get_text()
	# 			statCategory = data.get("data-stat")
	# 			# try:
	# 			# 	print ("%s: %d" % (statCategory, stat))
	# 			# except:
	# 			# 	print ("%s: %s" % (statCategory, stat))
main()