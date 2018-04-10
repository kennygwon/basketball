# Basketball Neural Network
## Overview
### neural_net.py
Creates a feedforward neural network that uses mini-batch gradient descent to predict the winner of basketball games.  For each game that is predicted, the statistics for the games leading up to that game are used as inputs for the neural network and the winner of the game (home or away team) is used as the output.
The user can specify the seasons from which games are picked, the statistics that are used
as input, and the number of games prior to the predicted game that are used as input.
The user is also prompted for information used to structure the neural network such as the
training data size, batch size, mini-batch size, number of epochs, learning rate, number of
layers, and nodes per layer.
The average cost per epoch for the training set and validation set are graphed so the user can see at what epoch the network begins to overtrain.
Finally the percentage of games that were correctly guessed is shown to assess the accuracy of the statistics selected and hyperparameters in choosing the winner of the basketball game.
### boxscore_scraper.py
Given a start date and end date, this program searches for any NBA games played between these dates.  Using basketballreference.com, the boxscores from each of these games are stored as JSON files and then as txt files to be used as input and output for training the neural network.  Aside from the team statistics and scores necessary for training the neural network, other information obtained from the boxscore scraper includes individual player statistics, and records.
## Results
By selecting the inputs as offensive rating and defensive rating for the two games prior to the game being predicted, I was able to create a neural network that was able to predict the winner of a basketball game with about 62% accuracy.  In the graph below, it can be seen that learning takes place as the average cost per training example decreases until about epoch 120 where learning stalls.

![300_epoch_graph](https://user-images.githubusercontent.com/23203851/38541682-d852508c-3c6d-11e8-8acc-b6b24eb40931.png)

Using stalled progress on the validation set as an indication that the network begins to overtrain around epoch 120, the neural network was then trained for 120 epochs before training was stopped.  The test set data was then used and it was found that the neural network was able to correctly predict the winner of the game for around 62% of the games which is certainly better than the expected 50% had it randomly chosen a winner.
