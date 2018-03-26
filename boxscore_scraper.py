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


	url = "https://www.basketball-reference.com/boxscores/201711070POR.html"


	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")


	print(soup.prettify())

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
	awayScore = int(scores[0].get_text())
	homeScore = int(scores[1].get_text())

	scoresList = {"away" : awayScore, "home" : homeScore}
	gameInfo["scores"] = scoresList

	print()
	print("home team: %s %d" % (homeTeam, homeScore))
	print("away team: %s %d" % (awayTeam, awayScore))
	
	teams = soup.find_all("table")
	for i in range(len(teams)):
		if i < len(teams)/2:
			memberTeam = awayTeam
		else:
			memberTeam = homeTeam
		print()
		print(memberTeam)
		body = teams[i].find("tbody")
		allRows = body.find_all("tr")
		for row in allRows:
			allData = row.find_all("td")
			if len(allData) == 1:
				continue
			
			#eliminates starters and reserves heading
			if len(allData) > 0:
				playerName = row.find("th").get_text()
				print()
				print(playerName)
			
			playerDict = {}
			for data in allData:
				if data.get_text() == "":
					stat = 0
				else:
					try:
						stat = int(data.get_text())
					except:
						try:
							stat = float(data.get_text())
						except:
							timePlayed = datetime.datetime.strptime(data.get_text(), "%M:%S")
							minutes = timePlayed.minute
							seconds = timePlayed.second/60
							stat = minutes + seconds
					statCategory = data.get("data-stat")
					if type(stat) == int:
						print("%s: %d" % (statCategory, stat))
					elif type(stat) == float:
						print ("%s: %f" % (statCategory, stat))
					else:
						print ("%s: %s" % (statCategory, stat))
				playerDict[statCategory] = stat
			if memberTeam == homeTeam:
				homePlayers[playerName] = playerDict
			else:
				awayPlayers[playerName] = playerDict
		foot = teams[i].find("tfoot")
		allRows = foot.find_all("tr")
		print()
		print("Team Totals")
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
				if type(stat) == int:
					print ("%s: %d" % (statCategory, stat))
				else:
					print ("%s: %.3f" % (statCategory, stat))
		if memberTeam == homeTeam:
			homeStats.update(teamDict)
		else:
			awayStats.update(teamDict)
	gameInfo["home stats"] = homeStats
	gameInfo["away stats"] = awayStats
	gameInfo["home players"] = homePlayers
	gameInfo["away players"] = awayPlayers

	return gameInfo


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
	lastDate = datetime.date(today.year, 3, 20)
	firstDate = datetime.date(2018, 3, 20)


	# dates = get_dates_between(firstDate, lastDate)
	# for day in dates:
	# 	boxscoreLinks = day_to_boxscore_url(day)
	# 	for url in boxscoreLinks:
	# 		game = url_to_stats(url)


	url = "https://www.basketball-reference.com/boxscores/201711070POR.html"
	print(url_to_stats(url).get("home players").get("C.J. McCollum").get("off_rtg"))


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