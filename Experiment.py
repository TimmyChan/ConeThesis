#!/usr/bin/env sage -python

from sage.all import *
#import PyNormaliz 
from Init import *
from TopDown import *
from Output import * 
import numpy as np
import argparse
import datetime
import os, sys



#==================#
# GLOBAL VARIABLES #
#==================# 

RMAX = 10
NUMGEN = 10
NUMOFTRIALS = 10
NUMOFTESTS = 100
fulltest = True

# Ask the user, first, dimension of the experiment?
# Then ask if user wants to hard code input.
while True:
		try:
			dim = int(input("dimension = "))
			if dim > 1: 
				break
			else: 
				print("Please enter a positive integer greater than 1.")
		except:
			print("Please enter a positive integer greater than 1.")

	
# Ask the user, second, are we randomly generating cones or testing a specific case.
generaterandomly = query_yes_no("Generate random cones?")


# If we are generating the cones randomly...
if generaterandomly:	
	# Do we want to keep the default settings?
	defaultsettings = query_yes_no("Keep Deafult Settings?\n\t - Number of generators for inner cone = 10 \n\t - Random numbers bounded at (+/-) 10", default="yes")


	# If we're not keeping the default settings...
	if not defaultsettings:
		# WHAT IS NUMGEN? (How many generators?)
		while True:
			try:
				NUMGEN = int(input("Number of vectors for random cones = "))
				if NUMGEN >= dim: 
					break 
				else: 
					print("Please enter a positive integer greater than {}.".format(dim))
			except:
				print("Please enter a positive integer greater than {}.".format(dim))



		# RESTRICTIONS ON RANDOM NUMBER GENERATOR. 
		while True:
			try:
				RMAX = int(input("Bound on random generator (greater than or equal to 2) = "))
				if RMAX >= 2:
					break 
				else: 
					print("Using default of (+/-)10")
					RMAX = 10
					break
			except:
				print("Please enter a positive integer greater than or equal to 2.")
		
		# Run full experiment?
		fulltest = query_yes_no("Full Experiment?")
else:
	fulltest = False
	continueinput = True
	while continueinput:
		outerGenerator = []
	
		while True:
			try:
				printseparator()
				print("Current list of extremal generators for the outer cone: {}".format(outerGenerator))
				printseparator()
				handle = raw_input("Please enter an extremal generator \"x_1,...,x_d\" of the outer cone without quotes, \nor type \"finish\" when done: ")
				if str(handle).lower() == "finish":
					if len(outerGenerator) +1 < dim:
						print("Not enough generators for a full dimensional cone!")
					else:
						break
				else:
					handlelist = [ int(i) for i in handle.split(",")]						
					if len(handlelist) <> dim:
						print("Incorrect dimension.")
					else:
						outerGenerator.append(handlelist)		
			except Exception as inputerror:
				print("Input error detected: {}".format(inputerror))
			
		D = Polyhedron(rays=outerGenerator,backend='normaliz')
		
		innerGenerator = []
		while True:
			try:
				printseparator()
				print("Current list of extremal generators for the inner cone: {}".format(innerGenerator))
				printseparator()
				handle = raw_input("Please enter an extremal generator \"x_1,...,x_d\" of the inner cone without quotes, \nor type \"finish\" when done: ")
				if handle.lower() == "finish":
					if len(innerGenerator) < dim:
						print("Not enough generators for a full dimensional cone!")
					else:
						break
				else:
					handlelist = [int(i) for i in handle.split(",")]						
					if len(handlelist) <> dim:
						print("Incorrect dimension.")
					elif D.contains(handlelist):
						innerGenerator.append(handlelist)
					else:
						print("{} is not contained in outer cone!".format(handlelist))				
			except Exception as inputerror:
				print("Input error detected: {}".format(inputerror))
			os.system('clear')
		C = Polyhedron(rays=innerGenerator,backend='normaliz')
		continueinput = not sanitycheck(C,D)


if not fulltest:
	NUMOFTRIALS = 1
	NUMOFTESTS = 1

RMIN = -RMAX


DIRECTORY = "DATA/{}d-experiment/".format(dim) + str(datetime.datetime.now()) + "/"

os.makedirs(DIRECTORY, 0755) 

filename = DIRECTORY + str(datetime.datetime.now()) + ".txt"
print("Saving Data to file \"{}\"".format(filename))
FILE = open(filename,"w+")
# Initialize conditions 
# C is the inner cone
# D is the conical hull of the union of the extremal generators of C and v


#==============#
# COLLECT DATA #
#==============#
AllDATA = [None]*(NUMOFTRIALS*NUMOFTESTS)
totalcounter = 0
print("Verbose Run for Accuracy Verification:")
FILE.write("\nVerbose Run for Accuracy Verification:")
if generaterandomly:
	C, D = generateInitialConditions(dim, RMIN, RMAX, NUMGEN, FILE,verbose=True)
TOPDOWNtrial(C,D,FILE,verbose=True)

print("\n\n")
print("Number of Tests: {} \nVector Coordinate Bound: (+/-){}".format((NUMOFTESTS*NUMOFTRIALS), RMAX))
FILE.write("\n\n")
FILE.write("Number of Tests: {} \nVector Coordinate Bound: (+/-){}".format((NUMOFTESTS*NUMOFTRIALS), RMAX))

printseparator(FILE)

if fulltest:
	DATA = [None]*(NUMOFTESTS)
	for trial in range(NUMOFTRIALS):
		for t in range(NUMOFTESTS):
			C, D = generateInitialConditions(dim, RMIN, RMAX, NUMGEN, FILE)
			DATA[t] = TOPDOWNtrial(C,D,FILE)
		print("TRIAL {}/{}: test # {} - {}".format(trial+1,NUMOFTRIALS, totalcounter+1, totalcounter+NUMOFTESTS))
		FILE.write("\nTRIAL {}/{}: test # {} - {}".format(trial+1,NUMOFTRIALS, totalcounter+1, totalcounter+NUMOFTESTS))
		printStats(DATA,FILE)
		for i in range(NUMOFTESTS):
			AllDATA[i+totalcounter] = DATA[i]
		totalcounter = totalcounter + NUMOFTESTS
		printseparator(FILE)
		
	#print AllDATA
	printStats(AllDATA,FILE,Final=True)