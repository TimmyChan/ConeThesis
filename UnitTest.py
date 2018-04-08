import unittest
from Init import *
from TopDown import *
import datetime


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
class Test_generateCone(unittest.TestCase):
	# 2D tests
	def test_C_fulldim_in_2D(self):
		C = generateCone(2,1,-10,10, FILE) #what if we have fewer generators than dimension? (fixed)
		self.assertTrue(C.is_full_dimensional())
	def test_C_proper_in_2D(self):
		C = generateCone(2,10,-10,10, FILE)
		self.assertTrue(C.lines_list() == [])
	# 3D tests
	def test_C_fulldim_in_3D(self):
		C = generateCone(3,1,-10,10, FILE)
		self.assertTrue(C.is_full_dimensional())
	def test_C_proper_in_3D(self):
		C = generateCone(3,10,-10,10, FILE)
		self.assertTrue(C.lines_list() == [])
	# 4D tests
	def test_C_fulldim_in_4D(self):
		C = generateCone(4,1,-10,10, FILE) 
		self.assertTrue(C.is_full_dimensional())
	def test_C_proper_in_4D(self):
		C = generateCone(4,10,-10,10, FILE)
		self.assertTrue(C.lines_list() == [])
	# 5D tests
	def test_C_fulldim_in_5D(self):
		C = generateCone(5,1,-10,10, FILE) 
		self.assertTrue(C.is_full_dimensional())
	def test_C_proper_in_5D(self):
		C = generateCone(5,10,-10,10, FILE)
		self.assertTrue(C.lines_list() == [])




class Test_GCD_List(unittest.TestCase):
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
	


class Test_generateRandomVector(unittest.TestCase):
	def test_v_primitive(self):
		v = generateRandomVector(5,-10,10)
		self.assertEqual(GCD_List(list([i for i in v])),1)
	def test_v_above_halfspace(self):
		v = generateRandomVector(3,-10,10)
		halfspace = Polyhedron(rays=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,-1]],backend='normaliz') 
		self.assertFalse(halfspace.contains(v))



class Test_generateOutsideVector(unittest.TestCase):
	def test_v_outside_C(self):
		C = generateCone(5,10,-10,10,FILE)
		v = generateOutsideVector(5, C, -10,10, FILE)
		self.assertFalse(C.contains(v))
	def test_v_primitive(self):
		v = generateRandomVector(5,-10,10)
		self.assertEqual(GCD_List(list([i for i in v])),1)


 


#Function that takes a SAGE cone and generates a random vector outside of the cone such that
#v not in C and -v not in C
#generateOutsideVector(dim, SAGECone, RMIN, RMAX,verbose=False):

# This function returns two SAGE cones, C & D, and a vector v, where
# D is the conical hull of the extremal generators of C union v 
# input: dim - ambient dimension
#        gencount - number of extremal generators 
#C, D, v = generateInitialConditions(dim, gencount, RMIN, RMAX, FILE, verbose=False):
class Test_generateInitialConditions(unittest.TestCase):
	def test_D_contains_C_and_v(self):
		C,D,v = generateInitialConditions(5, 10, -10, 10,FILE)
		self.assertTrue(D.contains(C))
		self.assertTrue(D.contains(v))
	def test_D_proper(self):
		C,D,v = generateInitialConditions(5, 10, -10, 10,FILE)
		self.assertEqual(D.lines_list,[])
	def test_D_full_dimensional(self):
		C,D,v = generateInitialConditions(5, 10, -10, 10,FILE)
		self.assertTrue(D.is_full_dimensional())












suite = unittest.TestLoader().loadTestsFromTestCase(Test_GCD_List)
unittest.TextTestRunner(verbosity=2).run(suite)


suite = unittest.TestLoader().loadTestsFromTestCase(Test_generateRandomVector)
unittest.TextTestRunner(verbosity=2).run(suite)


suite = unittest.TestLoader().loadTestsFromTestCase(Test_generateCone)
unittest.TextTestRunner(verbosity=2).run(suite)
