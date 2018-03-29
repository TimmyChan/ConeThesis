
from sage.all import *
from PyNormaliz import *
from Init import *
from TopDown import *
import numpy as np
import argparse

from sage.all import *
from PyNormaliz import *



#=================================================#
# GENERATE INITIAL CONDITIONS FOR CONE EXPERIMENT #
#=================================================#
# Input: Number of extremeal generators (numgen) in the cone
# Description: Generates (numgen) many vectors in the halfspace z>0
#              and takes conical hull
# Returns: SAGE Cone
# Expecting Cone of full dimension, so numgen >= dim. 
generateCone(dim, 10, -, RMAX,verbose=False):


# Functions used to generate a primitive rational vector
GCD_List(args):
   

generateRandomVector(dim, RMIN,RMAX,verbose=False):
   
    


#Function that takes a SAGE cone and generates a random vector outside of the cone such that
#v not in C and -v not in C
generateOutsideVector(dim, SAGECone, RMIN, RMAX,verbose=False):

# This function returns two SAGE cones, C & D, and a vector v, where
# D is the conical hull of the extremal generators of C union v 
# input: dim - ambient dimension
#        gencount - number of extremal generators 
C, D, v = generateInitialConditions(dim, gencount, RMIN, RMAX, verbose=False):

