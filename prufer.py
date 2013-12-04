#!/usr/bin/python

# Prufer code => S-expression
#
# Input: space-separated node list (assumed sorted with root first), newline,
#        space-separated code, newline.
#
# Example input :
#	0 1 2 3 4 5 6 7
#	0 0 7 7 3 7

# assume nodelist is sorted
nodelist = map(lambda u: int(u), raw_input().strip().split(" "))
botrow = map(lambda u: int(u), raw_input().strip().split(" "))
botrow += [nodelist[0]]

toprow = []
i = 0
while len(toprow) < len(botrow):
	for n in nodelist:
		if n not in botrow[i:] and n not in toprow:
			toprow += [n]
			break
	i += 1

def recurse(n):
	s = "(" + str(n)
	for i in range(len(botrow)):
		if botrow[i] == n:
			s += " "
			s += recurse(toprow[i])
	s += ")"
	return s

print recurse(nodelist[0])
