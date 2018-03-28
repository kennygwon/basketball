import json

def main():
	
	season = input("season: ")
	team = input("team: ")
	year = input("year: ")
	month = input("month: ")
	day = input("day: ")
	date = year + "-" + month + "-" + day
	season = "2017-18"
	seasonTextFile = season + ".txt"
	with open(seasonTextFile) as seasonJSONfile:
		currentDictionary = json.load(seasonJSONfile)


	for game in currentDictionary.get(team):
		if game.get("date") == date:
			print(game)

main()