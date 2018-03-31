import json

def main():
	
	running = True
	invalidSeason = True
	while running:

		while invalidSeason:
			season = str(input("season: "))
			try:
				seasonTextFile = season + ".txt"
				with open(seasonTextFile) as seasonJSONfile:
					currentDictionary = json.load(seasonJSONfile)
				invalidSeason = False
			except:
				print("please enter a season with the following format: '1997-98'")
		# quitBool = input("press any key to continue or type 'quit' to quit\n")
		# if quitBool.lower() == "quit":
			# break
		team = input("team: ")
	# keys = currentDictionary.keys()
	# for key in keys:

		# playoffGames = len(currentDictionary.get(key))
		# print("%s played %d playoff games" % (key, playoffGames))

		month = input("month: ")
		
		for game in currentDictionary.get(team):
			if game.get("date").split("-")[1] == month:
				print(game.get("date"))

		if int(month) > 7:
			if season[2:3] == 99:
				year = "20" + season.split("-")[1]
			else:
				year = season.split("-")[0]
		else:
			year = season[0:2] + season.split("-")[1]
		
		day = input("day: ")
		date = year + "-" + month + "-" + day

		userInput = ""
		while True:
			userInput = input("'roster' for team rosters; 'scores' for scores; 'team' to start another team in the same season; restart' to choose another date and team; 'quit' to quit\n")
			if userInput.lower() == "roster":
				for game in currentDictionary.get(team):
					if game.get("date") == date:
						print()
						print(game.get("teams").get("home"))
						homePlayers = (game.get("home players"))
						for homePlayer in homePlayers:
							print(homePlayer)
						print()
						print(game.get("teams").get("away"))
						awayPlayers = (game.get("away players"))
						for awayPlayer in awayPlayers:
							print(awayPlayer)
						print()
			if userInput.lower() == "scores":
				print(game.get("teams").get("away") + " (" + str(game.get("scores").get("away")) + ") "+ "@ " + game.get("teams").get("home") + " ("+ str(game.get("scores").get("home")) + ")")
			if userInput.lower() == "restart" or userInput.lower() == "quit" or userInput.lower() == "team":
				break


		if userInput.lower() == "restart":
			invalidSeason = True


		if userInput.lower() == "quit":
			break



		# for game in currentDictionary.get(team):
		# 	if game.get("date") == date:
		# 		print(game)

main()
