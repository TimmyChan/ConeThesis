
from sage.all import *
from PyNormaliz import *
from Init import *
from TopDown import *
import numpy as np
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("dimension", type=int,help="Dimension of ambient space for this experiment.")

args = parser.parse_args()
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
dim = args.dimension
# Initialize conditions 
# C is the inner cone
# D is the conical hull of the union of the extremal generators of C and v
#C, D, v = generateInitialConditions(dim,NUMGEN, RMIN, RMAX, verbose)
# for now Testing:
C = sage.geometry.cone.Cone([[-3,-1,1],[-3,0,1],[-2,-2,1],[2,0,1],[-2,2,1],[2,-1,1],[1,-3,1]])
v = vector([3,1,1])
D = sage.geometry.cone.Cone([[-3,-1,1],[-3,0,1],[-2,-2,1],[2,0,1],[-2,2,1],[2,-1,1],[1,-3,1],[3,1,1]])

print("C proper?: {}".format(C.is_proper()))
print("D contains C?:{}\nD contains v?:{}\nC contains v?:{}\n".format(D.intersection(C).is_equivalent(C) ,D.contains(v),C.contains(v)))

TOPDOWNtrial(C,D,v,verbose=True)
