#!/usr/bin/python

# ----------------------------------------------------------------
# drawtree: a tree-drawing program 
# It reads an S-expression from stdin then draws a tree to a
# specified picture file
#
# Example usage:
# 	cat sexp | ./drawtree.py output.png
#
# If you end up with a big image you can use programs like
# "Eye of GNOME" to scroll and zoom around them.
#
# project started by blockeduser, october 2013
# ----------------------------------------------------------------

# TODO: maybe latex or troff output would be nice if that's
#       not too hard

import pygame

import sys
import copy
import time
import math
import sexp_reader

from pygame.locals import *

####################################################################

# "t" is the tree
# encoding: child 0 is node, child 1 is left child,
#           child 2 is right child; recursively

# test tree 
t = [1, [2, 3, 4, 5], 3, [4, 5, 6, 7], [5, 1, [2, 123], 3, [4, [5, 6, 7], 8]]]

###################################################################

# =============== Tree routines ===============

# is it a tree node ?
def check(tn):
	return (type(tn) == list and len(tn)) or type(tn) == int

# get the headvalue
def head(tn):
	if type(tn) == list:
		return tn[0]
	else:
		return tn

# figure out height
def height(tn):
	l = [0]
	if type(tn) == list:
		for i in range(len(tn) - 1):
			l.append(height(tn[i + 1]))
	return 1 + max(l)

# get all the stuff that's at a given depth
def listd(tn, d):
	def listd_iter(tn, c, d, l):
		if c == d:
			l.append(tn)
		if c < d:
			for i in range(len(tn) - 1):
				listd_iter(tn[i+1], c + 1, d, l)
	l = []
	listd_iter(tn, 0, d, l)
	return l

# estimate required height in pixels
def est_height(tn):
	return height(tn) * 20

# estimate required width in pixels
def est_width(tn):
	l = []
	# for each depth-level,
	for d in range(height(tn)):
		# estimate reasonable width at this depth
		tot_text_pixels = 0
		stuff = listd(tn, d)
		for k in stuff:
			if type(k[0]) == str:
				tot_text_pixels += 15 * len(k[0])
		tot_text_pixels += 20 * len(stuff)
		w = max(tot_text_pixels, 40 * len(stuff))
		l.append(w)
	# choose the largest depth-width
	return max(l)

###################################################################

# deal with cli args
make_square = False
if "--square" in sys.argv:
	make_square = True
	sys.argv.remove("--square")

# get output file
if len(sys.argv) < 2:
	print "use: %s output.{png,bmp,tga,jpg}" % (sys.argv[0])
	print "N.B.: Input is an s-expression that goes into stdin"
	sys.exit(1)
outf = sys.argv[1]

# read input S-expression from one line of stdin
t = sexp_reader.sexp2list(raw_input())

# default video dimensions
w = 640
h = 480

# make the dimensions bigger if necessary
w = max(w, est_width(t))
h = max(h, est_height(t))

# make it square ?
if make_square:
	w = max(w, h)
	h = w

# pygame.init() initializes all the SDL modules and
# makes the quit routine super slow (like 1 full second to exit !!)
# apparently it's the audio module's fault
pygame.display.init()
pygame.font.init()

# get a window
win = pygame.Surface((w, h))
font = pygame.font.Font(pygame.font.match_font(pygame.font.get_fonts()[0]), 15)
pygame.display.set_caption('tree')

# setup some colors for further use
black = pygame.Color(0, 0, 0)
blue = pygame.Color(0, 0, 255)
red = pygame.Color(255, 0, 0)
white = pygame.Color(255, 255, 255)

# routine that automatizes pygame text-rendering ugliness
def write_text(txt, x, y):
	text = font.render(txt, False, black)
	rect = text.get_rect()
	rect.topleft = (x, y)
	win.blit(text, rect)

# white background
pygame.draw.rect(win, white, (0,0, w, h))	

# Split the vertical axis into 'h' equal-sized chunks,
# where h is the height
ychunk = h / height(t)

# Set up list of nodes at height 0
# This gets recursed into the list of nodes
# at heights 1, 2, ..., h
nl = [t]
pcl = [None]
pid = [0]

prev = -1

for i in range(height(t)):
	for j in range(len(nl)):
		if type(nl[j]) != list or (type(nl[j])==list and len(nl[j])==1):
			if (type(nl[j])==list and len(nl[j])==1):
				nl[j] = [nl[j][0], 0]
			else:
				nl[j] = [nl[j], 0]

	# Split horizontal axis into equal-sized chunk
	xlen = (len(nl) + 1)

	if prev > 0 and prev > xlen:
		xlen = prev

	prev = xlen

	xchunk = w / xlen

	# Draw all the (non-empty) nodes that occur at this height
	cl = []
	xc = xchunk
	yc = ychunk * i
	idx = 0
	for node in nl:
		if node != None:
			null_node = head(node) == 0
			cl.append([xc, yc+40])
			if i > 0:
				# draw line to parent
				pc = pcl[pid[idx]]
				if not null_node:
					pygame.draw.line(win, black, (xc, yc), tuple(pc)) 
				pass
			# draw the node
			if not null_node:
				pygame.draw.circle(win, black, (xc, yc+20), 20, 1)		
				write_text(str(head(node)), xc, yc+20)
		else:
			cl.append(None)
		xc += xchunk
		idx += 1

	pcl = cl

	# Prepare new nodelist
	nnl = []
	pid = []
	for k in range(len(nl)):
		#print "nl, ", nl[k]
		if type(nl[k]) == list:
			for l in range(len(nl[k]) - 1):
				pid.append(k)
				nnl.append(nl[k][l + 1])
	nl = nnl

# save result to imagefile and leave happily
pygame.image.save(win, outf)

sys.exit(0)


