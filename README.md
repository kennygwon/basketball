# Basketball Neural Network

##Overview

###neural_net.py

Creates a feedforward neural network that uses mini-batch gradient descent to predict the winner of basketball games.  For each game that is predicted, the statistics for the games leading up to that game are used as inputs for the neural network and the winner of the game (home or away team) is used as the output.
The user can specify the seasons from which games are picked, the statistics that are used
as input, and the number of games prior to the predicted game that are used as input.
The user is also prompted for information used to structure the neural network such as the
training data size, batch size, mini-batch size, number of epochs, learning rate, number of
layers, and nodes per layer.
The average cost per epoch for the training set and validation set are graphed so the user can see at what epoch the network begins to overtrain.
Finally the percentage of games that were correctly guessed is shown to assess the accuracy of the statistics selected and hyperparameters in choosing the winner of the basketball game.

###boxscore_scraper.py

Given a start date and end date, this program searches for any NBA games played between these dates.  Using basketballreference.com, the boxscores from each of these games are stored as JSON files and then as txt files to be used as input and output for training the neural network.  Aside from the team statistics and scores necessary for training the neural network, other information obtained from the boxscore scraper includes individual player statistics, and records.
