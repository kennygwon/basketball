import json

def main():
	
	season = input("season: ")
	season = "2013-14"
	seasonTextFile = season + ".txt"
	with open(seasonTextFile) as seasonJSONfile:
		currentDictionary = json.load(seasonJSONfile)
	running = True
	while running:
		print("Print 'g' to look up stats for a single game")
		if input("'Quit' to quit") == "quit":
			break
		else:
			year = input("year: ")
			month = input("month: ")
			day = input("day: ")
			date = year + "-" + month + "-" + day
			
			team = input("team: ")



			for game in currentDictionary.get(team):
				if game.get("date") == date:
					print(game)

main()