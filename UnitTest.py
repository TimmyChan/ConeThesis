import unittest
from Init import *
from TopDown import *
import datetime


filename = "./Unit_Test_Results/" + str(datetime.datetime.now()) + ".txt"
print("Saving Data to file \"{}\"".format(filename))
FILE = open(filename,"w+")
"""
CNFR0593@umn.edu
Hzei5274
"""


"""
generateCone(dim, numgen, RMIN, RMAX, FILE, verbose=False)

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
class TestConeGeneration(unittest.TestCase):
	# 2D tests
	def test_is_C_fulldim_in_2D(self):
		C = generateCone(2,1,-10,10, FILE, verbose=True) #what if we have fewer generators than dimension? (fixed)
		self.assertTrue(C.is_full_dimensional())

	
	def test_is_C_proper_in_2D(self):
		C = generateCone(2,10,-10,10, FILE, verbose=True)
		self.assertTrue(C.lines_list() == [])

	# 3D tests
	def test_is_C_fulldim_in_3D(self):
		C = generateCone(3,1,-10,10, FILE, verbose=True)
		self.assertTrue(C.is_full_dimensional())

	
	def test_is_C_proper_in_3D(self):
		C = generateCone(3,10,-10,10, FILE, verbose=True)
		self.assertTrue(C.lines_list() == [])
	# 4D tests
	def test_is_C_fulldim_in_4D(self):
		C = generateCone(4,1,-10,10, FILE, verbose=True) 
		self.assertTrue(C.is_full_dimensional())

	
	def test_is_C_proper_in_4D(self):
		C = generateCone(4,10,-10,10, FILE, verbose=True)
		self.assertTrue(C.lines_list() == [])
	# 5D tests
	def test_is_C_fulldim_in_5D(self):
		C = generateCone(5,1,-10,10, FILE, verbose=True) 
		self.assertTrue(C.is_full_dimensional())

	
	def test_is_C_proper_in_5D(self):
		C = generateCone(5,10,-10,10, FILE, verbose=True)
		self.assertTrue(C.lines_list() == [])

class TestVectorGeneration(unittest.TestCase):
	# is v inside C?
	def test_GCD_of_zeros(self):
		gcd = GCD_List([0,0,0,0,1])
		self.assertEqual(gcd,1)
	def test_GCD_posneg(self):
		gcd = GCD_List([-5,10])
		self.assertEqual(gcd,5)
	def test_GCD_coprime(self):
		gcd = GCD_List([7,8])
		self.assertEqual(gcd,1)
	def test_is_v_primitive(self):
		v = generateRandomVector(5,-10,10,verbose=True)
		self.assertEqual(GCD_List(list([i for i in v])),1)
	def test_is_v_outside_C(self):
		C = generateCone(5,10,-10,10,FILE, verbose=True)
		v = generateOutsideVector(5, C, -10,10, FILE, verbose=True)
		self.assertFalse(C.contains(v))

"""

Find the GCD of a list of numbers

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
#GCD_List(args):
   
"""

"""
#generateRandomVector(dim, RMIN,RMAX,verbose=False):
   
    


#Function that takes a SAGE cone and generates a random vector outside of the cone such that
#v not in C and -v not in C
#generateOutsideVector(dim, SAGECone, RMIN, RMAX,verbose=False):

# This function returns two SAGE cones, C & D, and a vector v, where
# D is the conical hull of the extremal generators of C union v 
# input: dim - ambient dimension
#        gencount - number of extremal generators 
#C, D, v = generateInitialConditions(dim, gencount, RMIN, RMAX, verbose=False):



















suite = unittest.TestLoader().loadTestsFromTestCase(TestConeGeneration)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestVectorGeneration)
unittest.TextTestRunner(verbosity=2).run(suite)