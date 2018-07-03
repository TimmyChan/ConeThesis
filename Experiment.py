
'''
This file contains the definitions for the classes 
	Experiment	Trial	ConePair
Experiment will contain methods for input / output
Trial will contain Tests and composite data
Test will house data and methods for a pair of cones.
'''

from GenerateCone import *


class ConePair:
	''' 
	Initializes with dimension (Integer)
	Generating Inner and Outer Cone,
	Contains a list ConeSequence[], which 
	'''
	dimension = 0 
	''' 
	note that once dimension is set, it will not be changed again. 
	All pairs of cones in a particular experiment will share the same dimension.
	'''
	def __init__(self,dimension):
		self.InnerCone



