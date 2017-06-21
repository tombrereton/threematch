import sys
import random
from time import time
from itertools import product
from collections import Counter

class Super:
	def __init__(self, a):
		self.a = a

	def match_check(self):
		for i in range(len(self.a)):
			for j in range(len(self.a[0])):
					if self.get_gem(i, j) is self.get_gem(i + 1, j) is self.get_gem(i + 2, j) is not None:
						return True
					if self.get_gem(i, j) is self.get_gem(i, j + 1) is self.get_gem(i, j + 2) is not None:
						return True
		return False

class Alternate(Super):
	def __init__(self, a, y, x, d):
		super().__init__(a)
		self.y = y
		self.x = x
		self.d = d
		self.swapped = [[y, x], [j + 1 if i == d else j for i, j in enumerate([y, x])]]
	
	def good(self):
		return self.swapped[1][0] < len(self.a) and self.swapped[1][1] < len(self.a[0])
	
	def get_gem(self, i, j):
		if len(self.a) <= i or len(self.a[0]) <= j:
			return None
		if [i, j] in self.swapped:
			k = self.swapped.index([i, j])
			return self.a[self.swapped[1 - k][0]][self.swapped[1 - k][1]]
		else:
			return self.a[i][j]

class Normal(Super):
	def __init__(self, a):
		super().__init__(a)
	
	def get_gem(self, i, j):
		if len(self.a) <= i or len(self.a[0]) <= j:
			return None
		else:
			return self.a[i][j]

def moves_one(a):
	m = []
	for i in range(len(a)):
		for j in range(len(a[0])):
			for k in range(2):
				alt = Alternate(a, i, j, k)
				if alt.good() and alt.match_check():
					m.append([i, j, k])
	return m

def moves_two(a):
	norm = Normal(a)
	m = []
	oneOffPatterns = (((0, 1), (1, 0), (2, 0)),
					  ((0, 1), (1, 1), (2, 0)),
					  ((0, 0), (1, 1), (2, 0)),
					  ((0, 1), (1, 0), (2, 1)),
					  ((0, 0), (1, 0), (2, 1)),
					  ((0, 0), (1, 1), (2, 1)),
					  ((0, 0), (0, 2), (0, 3)),
					  ((0, 0), (0, 1), (0, 3)))
	for i in range(len(a)):
		for j in range(len(a[0])):
			for pat in oneOffPatterns:
				if (norm.get_gem(i + pat[0][0], j + pat[0][1]) is \
					norm.get_gem(i + pat[1][0], j + pat[1][1]) is \
					norm.get_gem(i + pat[2][0], j + pat[2][1]) is not None) or \
					(norm.get_gem(i + pat[0][1], j + pat[0][0]) is \
					norm.get_gem(i + pat[1][1], j + pat[1][0]) is \
					norm.get_gem(i + pat[2][1], j + pat[2][0]) is not None):
					m.append([i, j])
	return m

def moves_three(a):
	moves = []
	rows = len(a)
	columns = len(a[0])
	for i, j, k in product(range(rows), range(columns), range(2)):
		if (i < rows - 2 and k == 0) or (j < columns - 2 and k == 1):
			to_check = [(i + c, j) if k == 0 else (i, j + c) for c in range(3)]
			types = [a[i][j] for i, j in to_check]
			c = Counter(types).most_common()
			if len(c) == 2:
				major_type = c[0][0]
				minor_type = c[1][0]
				y1, x1 = to_check[types.index(minor_type)]
				surround = [(y1, x1 + offset) for offset in range(-1, 2, 2)] + [(y1 + offset, x1) for offset in range(-1, 2, 2)]
				surround = [(y2, x2) for y2, x2 in surround if 0 <= y2 < rows and 0 <= x2 < columns and (y2, x2) not in to_check]
				for y2, x2 in surround:
					if a[y2][x2] == major_type:
						moves.append(((y1, x1), (y2, x2)))
	return moves
				

def p(a):
	print('\n'.join([''.join([str(el) for el in row]) for row in a]))

while True:
	a = [[random.randrange(6) for i in range(5)] for i in range(5)]
	w = Normal(a)
	if not w.match_check():
		p(a)
		break

def time_test(a):
	n = int(sys.argv[1])
	t = []
	t.append(time())
	for i in range(n): m1 = moves_one(a)
	t.append(time())
	for i in range(n): m2 = moves_two(a)
	t.append(time())
	for i in range(n): m3 = moves_three(a)
	t.append(time())
	print(m1, m2, m3, sep='\n\n')
	print('\t'.join([str(t[i] - t[i - 1]) for i in range(1, len(t))]))

time_test(a)
