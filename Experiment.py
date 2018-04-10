#!/usr/bin/env sage -python

from sage.all import *
#import PyNormaliz 
from Init import *
from TopDown import *
from Output import * 
import numpy as np
import argparse
import datetime


#parser = argparse.ArgumentParser()
#parser.add_argument("dimension", type=int,help="Dimension of ambient space for this experiment.")

#args = parser.parse_args()
# FILE = open('RawDataTopDown3D','a')

# Please note that to make a default cone in SAGE, one must now use 
# sage.geometry.cone.Cone(list), where list is a list of vectors.

#==================#
# GLOBAL VARIABLES #
#==================# 


#dim = input("Dimension: ")
#dim = args.dimension
while True:
	try:
		dim = int(input("dimension = "))
		if dim > 1: 
			break
		else: 
			print("Please enter a positive integer greater than 1.")
	except:
		print("Please enter a positive integer greater than 1.")

defaultsettings = query_yes_no("Keep Deafult Settings? (Number of generators for inner cone = 10 and \n\tRandom numbers bounded at (+/-) 10", default="yes"):
			
# The number of generators used for the cone (useful for 3d and up)
if defaultsettings:
	NUMGEN = 10
	RMAX = 10
else:
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


RMIN = -RMAX

fulltest = query_yes_no("Full Experiment?")
if fulltest:
	NUMOFTRIALS = 10
	NUMOFTESTS = 100
else:
	NUMOFTRIALS = 1
	NUMOFTESTS = 1


filename = "./DATA/{}d experiment - ".format(dim) + str(datetime.datetime.now()) + ".txt"
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
C, D, v = generateInitialConditions(dim, RMIN, RMAX, NUMGEN, FILE,verbose=True)
TOPDOWNtrial(C,D,v,FILE,verbose=True)

print("\n\n")
print("Number of Tests: {} \nVector Coordinate Bound: (+/-){}".format((NUMOFTESTS*NUMOFTRIALS), RMAX))
FILE.write("\n\n")
FILE.write("Number of Tests: {} \nVector Coordinate Bound: (+/-){}".format((NUMOFTESTS*NUMOFTRIALS), RMAX))

printseparator(FILE)

DATA = [None]*(NUMOFTESTS)
for trial in range(NUMOFTRIALS):
	for t in range(NUMOFTESTS):
		C, D, v = generateInitialConditions(dim, RMIN, RMAX, NUMGEN, FILE)
		DATA[t] = TOPDOWNtrial(C,D,v,FILE)
	print("TRIAL {}/{}: test # {} - {}".format(trial+1,NUMOFTRIALS, totalcounter+1, totalcounter+NUMOFTESTS))
	FILE.write("\nTRIAL {}/{}: test # {} - {}".format(trial+1,NUMOFTRIALS, totalcounter+1, totalcounter+NUMOFTESTS))
	printStats(DATA,FILE)
	for i in range(NUMOFTESTS):
		AllDATA[i+totalcounter] = DATA[i]
	totalcounter = totalcounter + NUMOFTESTS
	printseparator(FILE)
	
#print AllDATA
printStats(AllDATA,FILE,Final=True)