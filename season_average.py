import json

def main():
	#prompts user for a season
	invalidSeason = True
	while invalidSeason:
		season = str(input("Enter a season: "))
		try:
			seasonTextFile = season + ".txt"
			with open(seasonTextFile) as seasonJSONfile:
				currentDictionary = json.load(seasonJSONfile)
			invalidSeason = False
		except:
			print("Please enter a season with the following format: '1997-98'")
	
	#prompts user for a team
	invalidTeam = True
	while invalidTeam:
		team = input("Enter a team: ")
		if team in currentDictionary:
			invalidTeam = False

	#asks user sfor team average or player average
	invalidType = True
	while invalidType:
		averageType = (input("Press 't' for team average or 'p' for player average: ")).lower()
		if averageType == "t" or averageType == "p":
			invalidType = False

	numOfGames = 0
	if averageType == "t":
		invalidStat = True
		while invalidStat:
			statistic = input("Enter type of statistic: ")
			try:
				currentDictionary[team][0]["home stats"][statistic]
				invalidStat = False
			except:
				print("Invalid statistic type")
				print("Valid statistic types include:")
				print("", " ".join(currentDictionary[team][0]["home stats"].keys()))
		#adds the statistics which can be accumulated
		if statistic in ["fg3", "pts", "tov", "pf", "blk", "fta", "ft", "ast", "fg", "orb", "fga", "stl", "trb", "mp", "drb"]:
			statAccumulator = 0
			for game in range(len(currentDictionary[team])):
				if currentDictionary[team][game]["teams"]["home"] == team:
					statAccumulator += currentDictionary[team][game]["home stats"][statistic]
				else:
					statAccumulator += currentDictionary[team][game]["away stats"][statistic]
			print("%f" % (statAccumulator / len(currentDictionary[team])))
		#TODO: statistics requiring percentages
	if averageType == "p":
		player = input("Player name: ")
		invalidStat = True
		while invalidStat:
			statistic = input("Enter type of statistic: ")
			try:
				currentDictionary[team][0]["home stats"][statistic]
				invalidStat = False
			except:
				print("Invalid statistic type")
				print("Valid statistic types include:")
				print("", " ".join(currentDictionary[team][0]["home stats"].keys()))
		statAccumulator = 0
		for game in range(len(currentDictionary[team])):
			if currentDictionary[team][game]["teams"]["home"] == team:
				try:
					statAccumulator += currentDictionary[team][game]["home players"][player][statistic]
				except:
					pass
			else:
				# print(currentDictionary[team][game]["away players"].keys())
				try:
					statAccumulator += currentDictionary[team][game]["away players"][player][statistic]
				except:
					pass
		print("%f" % (statAccumulator / len(currentDictionary[team])))

main()



