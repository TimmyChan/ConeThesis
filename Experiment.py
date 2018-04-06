#!/usr/bin/env sage -python

from sage.all import *
import PyNormaliz 
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
# The number of generators used for the cone (useful for 3d and up)
NUMGEN = 5


# RESTRICTIONS ON RANDOM NUMBER GENERATOR. 
RMAX = 10
RMIN = -RMAX



NUMOFTRIALS = 10
NUMOFTESTS = 100

#dim = input("Dimension: ")
#dim = args.dimension
dim = input("dimension = ")


filename = str(datetime.datetime.now())
filename = "./DATA/{}d experiment - ".format(dim) + filename + ".txt"
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
FILE.write("Verbose Run for Accuracy Verification:")
C, D, v = generateInitialConditions(dim,NUMGEN, RMIN, RMAX, verbose=True)
TOPDOWNtrial(C,D,v,verbose=True)

print("\n\n")
print("Number of Tests: {} \nVector Coordinate Bound: (+/-){}".format((NUMOFTESTS*NUMOFTRIALS), RMAX))
FILE.write("\n\n")
FILE.write("Number of Tests: {} \nVector Coordinate Bound: (+/-){}".format((NUMOFTESTS*NUMOFTRIALS), RMAX))

printseparator(FILE)

DATA = [None]*(NUMOFTESTS)
for trial in range(NUMOFTRIALS):
	for t in range(NUMOFTESTS):
		C, D, v = generateInitialConditions(dim,NUMGEN, RMIN, RMAX)
		DATA[t] = TOPDOWNtrial(C,D,v)
	print("TRIAL {}/{}: test # {} - {}".format(trial+1,NUMOFTRIALS, totalcounter+1, totalcounter+NUMOFTESTS))
	FILE.write("TRIAL {}/{}: test # {} - {}".format(trial+1,NUMOFTRIALS, totalcounter+1, totalcounter+NUMOFTESTS))
	printStats(DATA,FILE)
	for i in range(NUMOFTESTS):
		AllDATA[i+totalcounter] = DATA[i]
	totalcounter = totalcounter + NUMOFTESTS
	printseparator(FILE)
	
#print AllDATA
printStats(AllDATA,FILE,Final=True)