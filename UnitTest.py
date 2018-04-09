import unittest
from Init import *
from TopDown import *
import datetime


FILE = open("UnitTest Output Dump.txt","w+")

''' 
verify that generateCone(dim,numgen,RMIN,RMAX,FILE,verbose=False) yields
	- full dimensional cone
	- cone that contains no lines.
'''
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
'''
verify that GCD_List(args) yields
	- GCD of a list with a zero is automatically 1
	- Always return the positive gcd
	- one prime should already give gcd 1
	- coprimes should have gcd 1 
	* Maybe eventually be careful and throw exceptions for type errors?
'''
class Test_GCD_List(unittest.TestCase):
	# is v inside C?
	def test_GCD_of_zeros(self):
		gcd = GCD_List([0,0,0,0,1])
		self.assertEqual(gcd,1)
	def test_GCD_posneg(self):
		gcd = GCD_List([-5,10])
		self.assertEqual(gcd,5)
	def test_GCD_oneprime(self):
		gcd = GCD_List([7,8,10])
		self.assertEqual(gcd,1)
	def test_GCD_coprime(self):
		gcd = GCD_List([8,27,125])
		self.assertEqual(gcd,1)	

'''
verify that generateRandomVector() yields
	- primitive vector in dimensions 2,3,4,5
'''
class Test_generateRandomVector(unittest.TestCase):
	def test_v_primitive_2D(self):
		v = generateRandomVector(2,-10,10)
		entriesofv = list([i for i in v])
		self.assertEqual(GCD_List(entriesofv),1)
	def test_v_primitive_3D(self):
		v = generateRandomVector(3,-10,10)
		entriesofv = list([i for i in v])
		self.assertEqual(GCD_List(entriesofv),1)
	def test_v_primitive_4D(self):
		v = generateRandomVector(4,-10,10)
		entriesofv = list([i for i in v])
		self.assertEqual(GCD_List(entriesofv),1)
	def test_v_primitive_5D(self):
		v = generateRandomVector(5,-10,10)
		entriesofv = list([i for i in v])
		self.assertEqual(GCD_List(entriesofv),1)


'''
verify that generateOutsideVector()
	- always yields vector outside of cone, in 
'''
class Test_generateOutsideVector(unittest.TestCase):
	def test_v_outside_C(self):
		C = generateCone(5,10,-10,10,FILE)
		v = generateOutsideVector( C, -10,10, FILE)
		self.assertFalse(C.contains(v))
	
class Test_generateInitialConditions(unittest.TestCase):
	def test_D_contains_C_and_v(self):
		C,D,v = generateInitialConditions(5, 10, -10, 10,FILE)
		Crays = C.rays_list()
		for r in Crays:
			self.assertTrue(D.contains(r))
		self.assertTrue(D.contains(v))
	def test_D_proper(self):
		C,D,v = generateInitialConditions(5, 10, -10, 10,FILE)
		self.assertEqual(D.lines_list(),[])
	def test_D_full_dimensional(self):
		C,D,v = generateInitialConditions(5, 10, -10, 10,FILE)
		self.assertTrue(D.is_full_dimensional())




InitTestNames = [Test_generateCone,Test_GCD_List,Test_generateRandomVector,Test_generateOutsideVector, Test_generateInitialConditions]

print("Testing Init.py:\n")

for i in range(len(InitTestNames)):
	suite = unittest.TestLoader().loadTestsFromTestCase(TestNames[i])
	unittest.TextTestRunner(verbosity=2).run(suite)
