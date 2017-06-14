import random, functools

def rand(rows, columns):
	return [[random.randrange(6) for i in range(rows)] for i in range(columns)]

def find_row_matches(array):
	return [(i, j) for i in range(len(array)) for j in range(len(array[i]) - 2) if array[i][j] is array[i][j + 1] is array[i][j + 2]]

def find_column_matches(array):
	return [(i, j) for i in range(len(array) - 2) for j in range(len(array[i])) if array[i + 1][j] is array[i + 1][j] is array[i + 2][j]]

def row_op(ident, element):
	if len(ident) is not 0 and ident[-1][0] is element[0] and ident[-1][1] + 1 is element[1]:
		last = ident.pop()
		ident.append((*last[:-1], last[-1] + 1))
		# return [*ident[:-1], (*ident[-1][:-1], ident[-1][-1] + 1)]
	else:
		ident.append((*element, 3))
		# return [*ident, (*element, 3)]
	return ident

def column_op(ident, element):
	if len(ident) is not 0 and ident[-1][0] is element[0] and ident[-1][0] + 1 is element[0]:
		last = ident.pop()
		ident.append((*last[:-1], last[-1] + 1))
		# return [*ident[:-1], (*ident[-1][:-1], ident[-1][-1] + 1)]
	else:
		ident.append((*element, 3))
		# return [*ident, (*element, 3)]
	return ident

def remove_dups(op, list):
	return functools.reduce(op, list, [])

def gen():
	while True:
		r = rand(10, 10)
		mr = find_row_matches(r)
		mc = find_column_matches(r)
		dr = remove_dups(row_op, mr)
		dc = remove_dups(column_op, mc)
		if len(mr) is not len(dr) or len(mc) is not len(dc):
			return r, mr, mc, dr, dc

r, mr, mc, dr, dc = gen()
