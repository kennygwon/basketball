import numpy.random as r
import numpy as np
import matplotlib.pyplot as plt
import json


def main():

	# x = np.array([[0,1],[3,4,5],[6,7,8]])
	# print(x.shape)

	# print(type(x[1, :]))
	# print(type(x[1]))

	# print(r.random_sample((5,3)))

	# print((np.array([3,4]) + np.array([[3],[4]])))

	# lst1 = r.random_sample((3,4))
	# lst2 = r.random_sample((4,2))
	# print(np.dot(lst1,lst2))
	# print(lst1.dot(lst2))

	# for i in range(5,0,-1):
	# 	print(i)
	lst = [4,5,8,15,2,7]
	print(min(lst)) 

	# lst = [4,5,6]
	# plt.plot(lst)
	# plt.show()


	# lst = np.array([[2],[3],[4],[5]])
	# print(lst.shape)
	# print((np.exp(lst)).shape)

	# with open("2012-13.txt") as seasonJSONfile:
	# 	currentDictionary = json.load(seasonJSONfile)
	# 	print(currentDictionary["Boston Celtics"][0]["home stats"]["fg"])



main()
