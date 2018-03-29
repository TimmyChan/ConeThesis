
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




NUMOFTRIALS = 10
NUMOFTESTS = 100

#dim = input("Dimension: ")
dim = args.dimension

TOPDOWNtrial(dim,verbose=True)
