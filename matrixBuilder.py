from os import listdir
import random
from operator import itemgetter
import numpy as np;
import matplotlib.pyplot as plt

players = [f for f in listdir("./players/")]

idToIndex = {};
count = 0;
for player in players:
	idToIndex[int(player)] = count;
	count = count+1;
idToIndex[-1] = count+1;

l = len(players)

numberOfWins = np.zeros(l+1);
numberOfLosses = np.zeros(l+1);

matrix = np.zeros((l+1, l+1)); #last one represents all unlisted players
matrix.astype('float')
count = np.zeros((l+1, l+1));

def getIndexOfId(sid):
	global idToIndex
	try:
		return idToIndex[sid]
	except:
		return -1

for p in players:
	f = open('./players/'+p, 'r');
	for line in f:
		x = line.strip().split();
		self = getIndexOfId(int(p));
		numberOfWins[self] = numberOfWins[self]+1;
		for others in x[1:]:
			o_index = getIndexOfId(int(others))
			numberOfLosses[o_index] = numberOfLosses[o_index]+1; #will divide by 5 later since
			matrix[o_index][self] = matrix[o_index][self]+int(x[0]);


"""
Normalize the matrix. Calculate the probability of moving from
one node to another based on grades. If the grade is lower,
we gave a bigger
"""

for i in range(l+1):
	#row sum = 1; 
	total = 0
	for j in range(l+1):
		value = matrix[i][j]
		total = total+value;
	for j in range(l+1):
		if(total == 0):
			matrix[i][j] = 1/float(l)
			continue;
		if(matrix[i][j] <= 0):
			matrix[i][j] = 0
		else:
			matrix[i][j] = (matrix[i][j])/float(total);


# x = np.zeros(l+1);
# starting = 0;
# for i in range(30000):
# 	x[starting] = x[starting]+1;
# 	r = random.random();
# 	for j in range(len(matrix[starting])):
# 		if(r-matrix[starting][j] < 0):
# 			starting = j;
# 		else:
# 			r = r-matrix[starting][j];
# 			continue;
# 	if(i%1000 == 0):
# 		print(np.round(x, 4))



# 
x = np.linalg.matrix_power(matrix, 200)[0]
y = range(len(x));
for _ in range(len(x)):
	if(numberOfWins[_] == 0):
		numberOfWins[_] = float(1);
	else:
		numberOfWins[_] = float(numberOfWins[_])

	if(numberOfWins[_]<3):
		numberOfWins[_] = float(100)

x = x/numberOfWins

so = [];
for i in y:
	z = (y[i],x[i])
	so.append(z);

z = sorted(so, key = itemgetter(1));
print(z);

temp2 = [list(z) for z in zip(*sorted(zip(x, y), key=itemgetter(0)))]

print(temp2)
max_index = 5

for i in temp2[1]:
	max_index = i;
	s_id = 0;
	for _ in idToIndex.keys():
		if(idToIndex[_] == max_index):
			s_id = _;

	print(s_id)



# max_index = 0;
# second_max = 0;
# third_max = 0;
# fourth_max = 0;
# max_occurence = 0;
# for _ in range(len(x)):
# 	if(max_occurence<x[_]):
# 		# five_max = fourth_max
# 		# fourth_max = third_max
# 		# third_max = second_max;
# 		# second_max = max_index;
# 		max_index = _;
# 		max_occurence = x[_];

# print(max_index)

# s_id = 0;
# for _ in idToIndex.keys():
# 	if(idToIndex[_] == max_index):
# 		s_id = _;
# 	# if(idToIndex[_] == second_max):
# 	# 	s_id2 = _;
# 	# if(idToIndex[_] == third_max):
# 	# 	s_id3 = _;
# 	# if(idToIndex[_] == fourth_max):
# 	# 	s_id4 = _;
# 	# if(idToIndex[_] == five_max):
# 	# 	s_id5 = _;
# print(s_id);
# # print(s_id2);
# # print(s_id3)
# # print(s_id4)
# # print(s_id5)


# temp2 = [list(z) for z in zip(*sorted(zip(x, y), key=itemgetter(0)))]

# print(temp2)


# for i in reversed(temp2[1]):
# 	print(i)
# 	hottest_choice = temp2[1][i];
# 	if(numberOfWins[i]<3):
# 		continue;
# 	s_id = 0;
# 	for _ in idToIndex.keys():
# 		if(idToIndex[_] == hottest_choice):
# 			s_id = _;

# 	print(s_id);

"""
New Methods
"""


# starting_node = 0;
# counter = float(1);
# x = np.zeros(l+1);
# for i in range(100000):
# 	outBound = sum([1 for k in matrix[starting_node] if k>0]);
# 	inBound = sum([1 for j in matrix.T[starting_node] if j>0]);
# 	if outBound == 0:
# 		#randomly travel to a node
# 		#reset counter
# 		counter = float(1);
# 		starting_node = random.randint(0, l);
# 		x[starting_node] = x[starting_node]+counter;
# 		continue;

# 	if inBound == 0:
# 		ratio = float(1);
# 	else:
# 		ratio = outBound/float(inBound)
# 	counter = counter*ratio;
# 	r = random.random();
# 	for j in range(len(matrix[starting_node])):
# 		if(r - matrix[starting_node][j] < 0):
# 			starting_node = j;
# 		else:
# 			r = r-matrix[starting_node][j]

# 	x[starting_node] = x[starting_node]+counter;

# y = range(len(x));

# temp2 = [list(z) for z in zip(*sorted(zip(x, y), key=itemgetter(0)))]


# for i in range(len(temp2[1])):
# 	hottest_choice = temp2[1][i];
# 	if(numberOfWins[i]<2):
# 		continue;
# 	s_id = 0;
# 	for _ in idToIndex.keys():
# 		if(idToIndex[_] == hottest_choice):
# 			s_id = _;

# 	print(s_id);

"""
New Methods
"""


# np.round(x, 4)

# max_index = 0;
# max_occurence = 0;
# for _ in range(len(x)):
# 	if(numberOfWins[_]+numberOfLosses[_]/float(5) < 5):
# 		continue;
# 	if(max_occurence<x[_]):
# 		max_index = _;
# 		max_occurence = x[_];

# print(max_index)

# s_id = 0;
# for _ in idToIndex.keys():
# 	if(idToIndex[_] == max_index):
# 		s_id = _;

# print(s_id);






# plt.matshow(matrix);
# plt.colorbar();
# plt.show();



# """
# Simulate markov chaining
# """

# x = np.round(np.linalg.matrix_power(matrix, 100), 4)[0].T;

# max_in = -1
# max_p = -1
# for _ in range(len(x)):

# 	tempp = x[_]/(numberOfWins[_]+numberOfLosses[_]/5)
# 	if((numberOfWins[_]+numberOfLosses[_]/5)<5):
# 		tempp = 0;
# 	if(max_p<tempp):
# 		max_in = _;
# 		max_p = tempp;

# print(max_in)

# for _ in idToIndex.keys():
# 	if(idToIndex[_] == max_in):
# 		s_id = _;

# print(s_id);

# x = np.zeros(l+1);
# point = random.randint(0, l)
# for _ in range(10000):
# 	r = random.random();
# 	futureIndex = -1;
# 	for i in range(len(matrix[point])):
# 		if(r-matrix[point][i]<0):
# 			futureIndex = i;
# 			break;
# 		r = r-matrix[point][i];

# 	x[futureIndex] = x[futureIndex]+1;
# 	point = futureIndex


# 	if(_%100 == 0):
# 		print(x);

# totalGames = numberOfWins+numberOfLosses/5

# x.astype('float');
# for i in range(len(x)):
# 	#Make people who have played less than 4 games ineligble
# 	if(totalGames[i]<3):
# 		x[i] = 0;


# x = x/totalGames;

# max_index = 0;
# max_occurence = 0;
# for _ in range(len(x)):
# 	if(max_occurence<x[_]):
# 		max_index = _;
# 		max_occurence = x[_];

# print(max_index)
# s_id = 0;
# for _ in idToIndex.keys():
# 	if(idToIndex[_] == max_index):
# 		s_id = _;

# print(s_id);