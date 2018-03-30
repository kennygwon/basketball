import json

def main():
	
	season = str(input("season: "))

	seasonTextFile = season + ".txt"
	with open(seasonTextFile) as seasonJSONfile:
		currentDictionary = json.load(seasonJSONfile)
	running = True
	while running:
		print("'Quit' to quit; 'team' for )
		team = input("team: ")
	# keys = currentDictionary.keys()
	# for key in keys:

		# playoffGames = len(currentDictionary.get(key))
		# print("%s played %d playoff games" % (key, playoffGames))

		print("Print 'g' to look up stats for a single game")
		if input("'Quit' to quit") == "quit":
			break
		elif :
			year = input("year: ")
			month = input("month: ")
			day = input("day: ")
			date = year + "-" + month + "-" + day
			
			team = input("team: ")



			for game in currentDictionary.get(team):
				if game.get("date") == date:
					print(game)

main()
