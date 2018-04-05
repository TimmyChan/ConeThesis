import unittest
from Init import *
from TopDown import *


"""
CNFR0593@umn.edu
Hzei5274
"""


"""
generateCone(dim, numgen, RMIN, RMAX, verbose=False)

Description:	Generates a full dimensional proper rational cone 

Input: 			Number of extremeal generators (numgen) in the cone
Method: 		Generates (numgen) many vectors in the halfspace z>0
        		and takes conical hull
Returns: 		SAGE Cone
Tests: 			- C is full dimensional even if numgen < dim (simply force use dim)
				- C is proper
				- C is convex
				- verbose version works
"""
class InitTestCase(unittest.TestCase):
	""" Tests for Init.py"""
	def test_is_C_SAGEcone(self):
		C = generateCone(2, 10, -10, 10)
		self.assertIsInstance(C, sage.geometry.cone)

	def test_is_C_proper(self):
		C = generateCone()
"""
Functions used to generate a primitive rational vector

Input:		List of integers
Method:		Recursion
Returns:	GCD of integers
Tests:		- GCD_List(2,3,5) = 1
			- GCD_List(5,10) = 10
			- GCD_List(3,7) = 1
			- GCD_List(0,0,) = 1
			- GCD_List(0,5) = 5
			- GCD_List(0,2,3) = 1
"""
GCD_List(args):
   
"""

"""
generateRandomVector(dim, RMIN,RMAX,verbose=False):
   
    


#Function that takes a SAGE cone and generates a random vector outside of the cone such that
#v not in C and -v not in C
generateOutsideVector(dim, SAGECone, RMIN, RMAX,verbose=False):

# This function returns two SAGE cones, C & D, and a vector v, where
# D is the conical hull of the extremal generators of C union v 
# input: dim - ambient dimension
#        gencount - number of extremal generators 
C, D, v = generateInitialConditions(dim, gencount, RMIN, RMAX, verbose=False):

