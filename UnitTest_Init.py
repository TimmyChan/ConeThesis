import unittest
from Init import *
from TopDown import *
from Output import *

FILE = open("UnitTest Output Dump.txt","w+")

''' 
verify that generateCone(dim,RMIN,RMAX,FILE,numgen=10,verbose=False) yields
	- full dimensional cone
	- cone that contains no lines.
'''
class Test_generateCone(unittest.TestCase):
	# 2D tests
	def test_C_fulldim_in_2D(self):
		C = generateCone(2,-10,10, 1) #what if we have fewer generators than dimension? (fixed)
		self.assertTrue(C.is_full_dimensional())
	def test_C_proper_in_2D(self):
		C = generateCone(2,-10,10, 10)
		self.assertTrue(C.lines_list() == [])
	# 3D tests
	def test_C_fulldim_in_3D(self):
		C = generateCone(3,-10,10, 1)
		self.assertTrue(C.is_full_dimensional())
	def test_C_proper_in_3D(self):
		C = generateCone(3,-10,10,10)
		self.assertTrue(C.lines_list() == [])
	# 4D tests
	def test_C_fulldim_in_4D(self):
		C = generateCone(4,-10,10, 1) 
		self.assertTrue(C.is_full_dimensional())
	def test_C_proper_in_4D(self):
		C = generateCone(4,-10,10,10)
		self.assertTrue(C.lines_list() == [])
	# 5D tests
	def test_C_fulldim_in_5D(self):
		C = generateCone(5,-10,10, 1) 
		self.assertTrue(C.is_full_dimensional())
	def test_C_proper_in_5D(self):
		C = generateCone(5,-10,10,10)
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
	- always yields vector outside of cone
	- always yields vector such that the conical hull of the rays of C and v 
		forms a proper cone.
'''
class Test_generateOutsideVector(unittest.TestCase):
	def test_v_outside_C_2D(self):
		C = generateCone(2,-10,10,10,FILE)
		v = generateOutsideVector( C, -10,10)
		self.assertFalse(C.contains(v))
	def test_v_outside_C_3D(self):
		C = generateCone(3,-10,10,10,FILE)
		v = generateOutsideVector( C, -10,10)
		self.assertFalse(C.contains(v))
	def test_v_outside_C_4D(self):
		C = generateCone(4,-10,10,10,FILE)
		v = generateOutsideVector( C, -10,10)
		self.assertFalse(C.contains(v))
	def test_v_outside_C_5D(self):
		C = generateCone(5,-10,10,10,FILE)
		v = generateOutsideVector( C, -10,10)
		self.assertFalse(C.contains(v))
	def test_ConicalHull_v_and_C_is_proper_2D(self):
		C = generateCone(2,-10,10,10,FILE)
		v = generateOutsideVector(C,-10,10)
		Drays = C.rays_list().append(v)
		D = Polyhedron(rays=Drays,backend='normaliz')
		self.assertEqual(D.rays_list(), [])
	def test_ConicalHull_v_and_C_is_proper_3D(self):
		C = generateCone(3,-10,10,10,FILE)
		v = generateOutsideVector(C,-10,10)
		Drays = C.rays_list().append(v)
		D = Polyhedron(rays=Drays,backend='normaliz')
		self.assertEqual(D.rays_list(), [])
	def test_ConicalHull_v_and_C_is_proper_4D(self):
		C = generateCone(4,-10,10,10,FILE)
		v = generateOutsideVector(C,-10,10)
		Drays = C.rays_list().append(v)
		D = Polyhedron(rays=Drays,backend='normaliz')
		self.assertEqual(D.rays_list(), [])
	def test_ConicalHull_v_and_C_is_proper_5D(self):
		C = generateCone(5,-10,10,10)
		v = generateOutsideVector(C,-10,10)
		Drays = C.rays_list().append(v) # Take the list of rays and append v, then take conical hull
		D = Polyhedron(rays=Drays,backend='normaliz')
		self.assertEqual(D.rays_list(), [])

'''
verify that gernateInitialConditions()
	- D contains C and v (check by listing rays of C and verifying each one)
	- D contains no lines
	- D is full dimensional
'''
class Test_generateInitialConditions(unittest.TestCase):
	def test_D_contains_C_and_v_2D(self):
		C,D,v = generateInitialConditions(2, 10, -10, 10)
		Crays = C.rays_list()
		for r in Crays:
			self.assertTrue(D.contains(r))
		self.assertTrue(D.contains(v))
	def test_D_contains_C_and_v_3D(self):
		C,D,v = generateInitialConditions(3, 10, -10, 10)
		Crays = C.rays_list()
		for r in Crays:
			self.assertTrue(D.contains(r))
		self.assertTrue(D.contains(v))
	def test_D_contains_C_and_v_4D(self):
		C,D,v = generateInitialConditions(4, 10, -10, 10)
		Crays = C.rays_list()
		for r in Crays:
			self.assertTrue(D.contains(r))
		self.assertTrue(D.contains(v))
	def test_D_contains_C_and_v_5D(self):
		C,D,v = generateInitialConditions(5, 10, -10, 10)
		Crays = C.rays_list()
		for r in Crays:
			self.assertTrue(D.contains(r))
		self.assertTrue(D.contains(v))
	def test_D_proper_2D(self):
		C,D,v = generateInitialConditions(2, 10, -10, 10)
		self.assertEqual(D.lines_list(),[])	
	def test_D_proper_3D(self):
		C,D,v = generateInitialConditions(3, 10, -10, 10)
		self.assertEqual(D.lines_list(),[])	
	def test_D_proper_4D(self):
		C,D,v = generateInitialConditions(4, 10, -10, 10)
		self.assertEqual(D.lines_list(),[])
	def test_D_proper_5D(self):
		C,D,v = generateInitialConditions(5, 10, -10, 10)
		self.assertEqual(D.lines_list(),[])
	def test_D_full_dimensional_2D(self):
		C,D,v = generateInitialConditions(2, 10, -10, 10)
		self.assertTrue(D.is_full_dimensional())
	def test_D_full_dimensional_3D(self):
		C,D,v = generateInitialConditions(3, 10, -10, 10)
		self.assertTrue(D.is_full_dimensional())
	def test_D_full_dimensional_4D(self):
		C,D,v = generateInitialConditions(4, 10, -10, 10)
		self.assertTrue(D.is_full_dimensional())
	def test_D_full_dimensional_5D(self):
		C,D,v = generateInitialConditions(5, 10, -10, 10)
		self.assertTrue(D.is_full_dimensional())

InitTestNames = [Test_generateCone,Test_GCD_List,Test_generateRandomVector,Test_generateOutsideVector, Test_generateInitialConditions]
boxprint("TESTING Init.py")

for i in range(len(InitTestNames)):
	print("\n----------------------------------------------------------------------\n")
	suite = unittest.TestLoader().loadTestsFromTestCase(InitTestNames[i])
	unittest.TextTestRunner(verbosity=2).run(suite)
