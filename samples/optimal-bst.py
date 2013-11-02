#!/usr/bin/python

# emit an s-expression for an optimal BST for keys 1, ..., n
# by blockeduser,
# Tue Oct 29 00:18:45 EDT 2013

import math
import sys

try:
	n = int(sys.argv[1])
except:
	sys.stderr.write("optimal-bst: I need an integer as argument !\n")
	sys.exit(1)


# =============== Binary tree routines ===============

# does a tree node have a leftchild ?
def checklc(tn):
	return type(tn) == list and len(tn) > 1

# does a tree node have a rightchild ?
def checkrc(tn):
	return type(tn) == list and len(tn) > 2

# is it a tree node ?
def check(tn):
	return (type(tn) == list and len(tn)) or type(tn) == int

# get the leftchild
def lc(tn):
	return tn[1]

# get the rightchild
def rc(tn):
	return tn[2]

# get the headvalue
def head(tn):
	if type(tn) == list:
		return tn[0]
	else:
		return tn

# =============== BST routines ===============

def bst_insert(n, k):
	if type(n) == list and len(n) == 0:
		n.append(k)
		return n
	
	if checklc(n) and type(n[1]) == int:
		n[1] = [n[1]]
	if checkrc(n) and type(n[2]) == int:
		n[2] = [n[2]]

	if k <= head(n):
		if checklc(n):
			bst_insert(n[1], k)
		else:
			while len(n) < 2:
				n.append("X")
			n[1] = k
	else:
		if checkrc(n):
			bst_insert(n[2], k)
		else:
			while len(n) < 3:
				n.append("X")
			n[2] = k


# optimal BST insertion order
def insert_mh(io, arr):
	if len(arr) < 3:
		for k in arr:
			io.append(k)
	else:
		io.append(arr[int(math.ceil(len(arr)/2.0)) - 1])
		insert_mh(io, arr[:int(math.ceil(len(arr)/2.0)) - 1])
		insert_mh(io, arr[int(math.ceil(len(arr)/2.0)):])

# Run the optimal-order insertion

l = []
insert_mh(l, range(1, n + 1))
t = []
for e in l:
	bst_insert(t, e)

print str(t).replace(',', '').replace('[', '(').replace(']', ')').replace("'", '')

