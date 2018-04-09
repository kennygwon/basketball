import numpy as np
import numpy.random as r
import json
import random
import matplotlib.pyplot as plt
from datetime import date
from datetime import timedelta


def getSeasons():
	invalidSeason = True
	while invalidSeason:
		print()
		firstSeason = str(input("Please enter the first season: "))
		try:
			seasonTextFile = firstSeason + ".txt"
			file = open(seasonTextFile, "r")
			file.close()
			invalidSeason = False
		except:
			print("please enter a season with the following format: '1997-98'")

	invalidSeason = True
	while invalidSeason:
			lastSeason = str(input("Please enter the second season: "))
			try:
				seasonTextFile = lastSeason + ".txt"
				file = open(seasonTextFile, "r")
				file.close()
				if lastSeason.split("-")[0] >= firstSeason.split("-")[0]:
					invalidSeason = False
				else:
					print("The second season must come after the first season")
			except:
				print("please enter a season with the following format: '1997-98'")
	seasons = [firstSeason]
	season = firstSeason
	while season != lastSeason:
		firstDate = date(year = int(season.split("-")[0]), month = 1, day = 1)
		firstDate = firstDate.replace(year = (firstDate.year+1))
		secondDate = firstDate.replace(year = (firstDate.year+1))
		firstYear = str(firstDate.year)
		secondYear = str(secondDate.year)
		season = str(firstYear) + "-" + secondYear[2:4]
		seasons.append(season)
	seasonTextFiles = []
	for season in seasons:
		seasonTextFile = season + ".txt"
		seasonTextFiles.append(seasonTextFile)
	return seasonTextFiles

def getStats(season):
	#prompts the user for statistics and checks to see that are valid stats
	with open(season) as seasonJSONfile:
		currentDictionary = json.load(seasonJSONfile)
	invalidNum = True
	print()
	while invalidNum:
		numOfStats = input("How many statistics to be used as input? ")
		if numOfStats.isdigit():
			if int(numOfStats) < 10:
				numOfStats = int(numOfStats)
				invalidNum = False
			else:
				print("Too many inputs")
	listOfStats = []
	validStats = list(currentDictionary[random.choice(list(currentDictionary.keys()))][0]["home stats"].keys())
	for stat in range(numOfStats):
		invalidStatistic = True
		while invalidStatistic:
			statistic = input("Enter a stat category: ")
			if statistic in validStats:
				if statistic not in listOfStats:
					listOfStats.append(statistic)
					invalidStatistic = False
				else:
					print("You have already entered that statistic")
			else:
				print("Valid statistics include:")
				print(", ".join(validStats))
	return listOfStats

def getAverageStats(seasons, stats):
	# finds the average, min, and max of the specified stats for the specified seasons
	# outputs a list of the same size of stats but each item contains [average, min, max]
	# this information is used to normalize the data to range from 0 to 1
	statList = []
	for stat in stats:
		# contains a list of all the stat past the 10th games in specified seasons
		occurencesOfStat = []
		for season in seasons:
			with open(season) as seasonJSONfile:
				currentDictionary = json.load(seasonJSONfile)
				teams = list(currentDictionary.keys())
				teams = sorted(teams)
				for team in teams:
					for game in range(len(currentDictionary[team])):
						homeTeam = currentDictionary[team][game]["teams"]["home"]
						awayTeam = currentDictionary[team][game]["teams"]["away"]
						if team == homeTeam:
							otherTeam = awayTeam
						else:
							otherTeam = homeTeam
						if team < otherTeam:
							records = currentDictionary[team][game]["records"]
							homeGP = records["home losses"] + records["home wins"]
							awayGP = records["away losses"] + records["away wins"]
							if (homeGP > 10) and (awayGP > 10):
								occurencesOfStat.append(currentDictionary[team][game]["home stats"][stat])
								occurencesOfStat.append(currentDictionary[team][game]["away stats"][stat])
		statAvg = np.mean(occurencesOfStat)
		statMin = min(occurencesOfStat)
		statMax = max(occurencesOfStat)
		statList.append([statAvg, statMin, statMax])
	return statList






def getInputsOutputs(seasons, stats, averageStats, prevGames):
	x = []
	y = []
	for season in seasons:
		with open(season) as seasonJSONfile:
			currentDictionary = json.load(seasonJSONfile)
			teams = list(currentDictionary.keys())
			teams = sorted(teams)
			# adds data for each team in the season
			for team in teams:
				for game in range(len(currentDictionary[team])):
					homeTeam = currentDictionary[team][game]["teams"]["home"]
					awayTeam = currentDictionary[team][game]["teams"]["away"]
					if team == homeTeam:
						otherTeam = awayTeam
					else:
						otherTeam = homeTeam
					# since we check the teams in order
					# if the team we are checking is greater than the other team for that game,
					# we have already done that game
					if team < otherTeam:
						records = currentDictionary[team][game]["records"]
						homeGP = records["home losses"] + records["home wins"]
						awayGP = records["away losses"] + records["away wins"]
						if (homeGP > 10) and (awayGP > 10):
							scores = currentDictionary[team][game]["scores"]
							# # difference in the score is the output
							# # y is the difference between the home score and the away score
							# y.append(np.array([[scores["home"] - scores["away"]]]))
							
							# who won the game is the output
							# 1 for home team, 0 for away team
							if scores["home"] > scores["away"]:
								y.append(np.array([[1]]))
							else:
								y.append(np.array([[0]]))							


							gameInput = []
							# statistics from the previous ten games are used for the input layer
							for trainingGame in range(homeGP - prevGames, homeGP):
								# checks to see if the home team was home or away in the previous games
								if currentDictionary[homeTeam][trainingGame]["teams"]["home"] == homeTeam:
									#for stat in stats
									for statIndex in range(len(stats)):
										stat = currentDictionary[homeTeam][trainingGame]["home stats"][stats[statIndex]]
										normalizedStat = (stat - averageStats[statIndex][1]) / (averageStats[statIndex][2] - averageStats[statIndex][1])
										gameInput.append([normalizedStat])
										# gameInput.append([currentDictionary[homeTeam][trainingGame]["home stats"][stat]])
										# print(gameInput)
								else:
									for statIndex in range(len(stats)):
										stat = currentDictionary[homeTeam][trainingGame]["away stats"][stats[statIndex]]
										normalizedStat = (stat - averageStats[statIndex][1]) / (averageStats[statIndex][2] - averageStats[statIndex][1])
										gameInput.append([normalizedStat])
										# print(gameInput)
							for trainingGame in range(awayGP - prevGames, awayGP):
								# checks to see if the home team was home or away in the previous 10 games
								if currentDictionary[homeTeam][trainingGame]["teams"]["home"] == awayTeam:
									for statIndex in range(len(stats)):
										stat = currentDictionary[homeTeam][trainingGame]["home stats"][stats[statIndex]]
										normalizedStat = (stat - averageStats[statIndex][1]) / (averageStats[statIndex][2] - averageStats[statIndex][1])
										gameInput.append([normalizedStat])
								else:
									for statIndex in range(len(stats)):
										stat = currentDictionary[homeTeam][trainingGame]["away stats"][stats[statIndex]]
										normalizedStat = (stat - averageStats[statIndex][1]) / (averageStats[statIndex][2] - averageStats[statIndex][1])
										gameInput.append([normalizedStat])
							x.append(np.array(gameInput))
	return (x,y)

def validationSetError(w, b, x, y)


def sigmoid(x):
	#takes in an np.array and applies the sigmoid function to each element of the array
	#outputs an np.array of the same size
	return 1 / (1 + np.exp(-x))
def sigmoidDerivative(x):
	return sigmoid(x) * (1 - sigmoid(x))

def initializeWeightsBiases(nnStructure):
	#creates weights and biases stored in np.arrays equal to the number of nodes in each layer
	#randomly initializes weights and biases to be between 0 and 1
	w = {}
	b = {}
	#for weights, creates a np.array with size l x l-1 where l is the number of nodes in the layer
	#and l-1 is the nodes in the last layer
	#for biases, creates a l x 1 np.array for each layer
	for layer in range(1,len(nnStructure)):
		w[layer] = r.random_sample((nnStructure[layer], nnStructure[layer-1]))
		b[layer] = r.random_sample((nnStructure[layer], 1))
	return (w,b)

def initializeMeanWeightsBiases(nnStructure):
	#initializes mean weights and biases to be 0's
	meanW = {}
	meanB = {}
	for layer in range(1,len(nnStructure)):
		meanW[layer] = np.zeros((nnStructure[layer], nnStructure[layer-1]))
		meanB[layer] = np.zeros((nnStructure[layer], 1))
	return (meanW, meanB)

def feedForward(x,w,b):
	# h is output
	# so the output for the first layer is just the input layer
	h = {1:x}
	z = {}
	# len(w) + 1 because we start from layer 1 since there is no layer 0 for weights
	for layer in range(1, len(w) + 1):
		# input for the first layer or weights is x, the input layer
		if layer == 1:
			sigmoidInput = x
		else:
			sigmoidInput = h[layer]
		# z is the input to the sigmoid function
		# z = (w * l) + b
		z[layer+1] = w[layer].dot(sigmoidInput) + b[layer]
		h[layer+1] = sigmoid(z[layer+1])
	return(h,z)

def lastLayerDelta(y, h, z):
	# calculates delta for the last layer
	# takes in the h and z as the inputs
	# J is the cost function
	# delJ / delw = delta * h
	# delJ / delb = delta
	delta = -(y-h) * sigmoidDerivative(z)
	return delta

def hiddenLayerDelta(nextDelta, w, z):
	delta = ((np.transpose(w)).dot(nextDelta)) * sigmoidDerivative(z)
	return delta

def convertToMiniBatch(x, y, miniBatchSize):
	allMiniBatchesX = []
	allMiniBatchesY = []
	while len(x) >= (2 * miniBatchSize):
		miniBatchX = []
		miniBatchY = []
		for i in range(miniBatchSize):
			randomNum = random.randrange(0, len(x))
			miniBatchX.append(x.pop(randomNum))
			miniBatchY.append(y.pop(randomNum))
		allMiniBatchesX.append(miniBatchX)
		allMiniBatchesY.append(miniBatchY)
	allMiniBatchesX.append(x)
	allMiniBatchesY.append(y)
	return(allMiniBatchesX, allMiniBatchesY)
		

def trainMiniBatch(x, y, w, b, nnStructure, learningRate):
	
	(deltaW, deltaB) = initializeMeanWeightsBiases(nnStructure)
	totalError = 0
	for iterationNum in range(len(x)):
		delta = {}
		(h, z) = feedForward(x[iterationNum], w, b)
		for layerNum in range(len(nnStructure), 0 ,-1):
			if layerNum == len(nnStructure):
				delta[layerNum] = lastLayerDelta(y[iterationNum], h[layerNum], z[layerNum])
				totalError += abs(y[iterationNum].item(0) - h[layerNum].item(0))
				# print("y")
				# print(y[iterationNum])
				# print("h")
				# print(h[layerNum])
				# print("total error")
				# print(totalError)



			else:
				if layerNum > 1:
					delta[layerNum] = hiddenLayerDelta(delta[layerNum + 1], w[layerNum], z[layerNum])
				deltaW[layerNum] += delta[layerNum + 1].dot(np.transpose(h[layerNum]))
				deltaB[layerNum] += delta[layerNum + 1]
		for layerNum in range(len(nnStructure) - 1, 0, -1):
			# print(type(-learningRate * ((1/(len(x))) * deltaW[layerNum])))
			# print(deltaW[layerNum])
			w[layerNum] += -learningRate * ((1/(len(x))) * deltaW[layerNum])
			b[layerNum] += -learningRate * ((1/(len(x))) * deltaB[layerNum])
	return (w, b, totalError)


def main():
	print()
	print("Creates a neural network that grab statistics from specified seasons for the specified statistics")
	print("Uses statistics from the previous games as input and the difference in score as output")

	seasons = getSeasons()
	stats = getStats(seasons[0])
	averageStats = getAverageStats(seasons, stats)
	print(averageStats)

	prevGames = int(input("Stats froms how many previous games? "))

	inputsOutputs = getInputsOutputs(seasons, stats, averageStats, prevGames)
	inputs = inputsOutputs[0]
	outputs = inputsOutputs[1]

	
	numOfGames = len(inputs)
	print()
	print("The total number of games played during those seasons is %d" % (numOfGames))
	batchSize = int(input("How many of those games would you like to use as training data? "))
	# plucks training data from all games that between the specified seasons
	# the rest of the data is used to test the results of the neural net after it's been trained
	
	trainingDataX = []
	trainingDataY = []
	for i in range(batchSize):
		randomNum = random.randrange(0, len(inputs))
		trainingDataX.append(inputs.pop(randomNum))
		trainingDataY.append(outputs.pop(randomNum))


	miniBatchSize = int(input("Enter mini-batch size: "))

	epochs = int(input("Enter number of epochs: "))

	learningRate = float(input("Enter learning rate: "))


	firstLayerSize = len(inputs[0])
	nnStructure = [firstLayerSize]
	numLayers = int(input("Enter number of layers: "))
	print("The number of nodes in the first layer is %d" % (firstLayerSize))
	for layer in range(numLayers - 2):
		nnStructure.append(int(input("Enter number of nodes in layer: ")))
	# the output layer is a single node
	nnStructure.append(1)

	errorFunction = []
	(w, b) = initializeWeightsBiases(nnStructure)
	for epoch in range(epochs):
		# print("weights")
		# print(w)
		# print("biases")
		# print(b)
		# print("Epoch %d" % (epoch))
		batchX = list(trainingDataX)
		batchY = list(trainingDataY)
		(miniBatchesX, miniBatchesY) = convertToMiniBatch(batchX, batchY, miniBatchSize)
		totalError = 0
		for miniBatchNum in range(len(miniBatchesX)):
			# if miniBatchNum == 0:
				# (w, b) = initializeWeightsBiases(nnStructure)
			(w,b,error) = trainMiniBatch(miniBatchesX[miniBatchNum], miniBatchesY[miniBatchNum], w, b, nnStructure, learningRate)
			totalError += error
		errorFunction.append(totalError/len(trainingDataX))
		if epoch % 50 == 0:
			print("Epoch %d" % (epoch))
			print("weights")
			print(w)
			print("biases")
			print(b)
	plt.plot(errorFunction)
	plt.ylabel("Average Difference in Score")
	plt.xlabel("Number of Epochs")
	plt.title("Cost Function")
	plt.show()


main()