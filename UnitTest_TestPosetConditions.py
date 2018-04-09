import unittest
from Init import *
from Output import *
from TestPosetConditions import *

FILE = open("UnitTest Output Dump.txt","w+")

''' 
verify TestPosetConditions(C,D)
	- Returns False if C,D not full dimension
	- Returns False if C == D
	- Returns False if C interesect D^c not empty
	- Returns True if L(D) = L(C)+ Z_+ v for some v outside of C
	- Returns False otherwise
	- Returns False if cone(Hilb(C) union Hilb(C)+v) is not integrally closed
'''
class Test_TestPosetConditions(unittest.TestCase):
	def test_ConesThatWork_2D(self):
		C = Polyhedron(rays=[[0,1],[1,0]],backend='normaliz')
		D = C.convex_hull(Polyhedron(rays=[[-1,1]],backend='normaliz'))
		self.assertTrue(TestPosetConditions(C,D))
	def test_ConesThatWork_3D(self):
		C = Polyhedron(rays=[[0,0,1],[1,0,1],[1,1,1]],backend='normaliz')
		D = C.convex_hull(Polyhedron(rays=[[0,1,1]],backend='normaliz'))
		self.assertTrue(TestPosetConditions(C,D))
	'''
	def test_ConesThatWork_4D(self):
		C = Polyhedron(rays=[[0,0,0,1],[1,0,0,1],[0,1,0,1],[0,0,1,1]],backend='normaliz')
		D = C.convex_hull(Polyhedron(rays=[[2,1,1,1]],backend='normaliz'))
		self.assertTrue(TestPosetConditions(C,D))
	'''
	def test_notfulldimensionInner_2D(self):
		C = Polyhedron(rays=[[-1,1]],backend='normaliz')
		D = generateCone(2,-10,10)
		self.assertFalse(TestPosetConditions(C,D))
	def test_notfulldimensionInner_3D(self):
		C = Polyhedron(rays=[[-1,1]],backend='normaliz')
		D = generateCone(3,-10,10)
		self.assertFalse(TestPosetConditions(C,D))
	def test_notfulldimensionInner_4D(self):
		C = Polyhedron(rays=[[-1,1]],backend='normaliz')
		D = generateCone(4,-10,10)
		self.assertFalse(TestPosetConditions(C,D))
	def test_notfulldimensionInner_3D(self):
		C = Polyhedron(rays=[[-1,1]],backend='normaliz')
		D = generateCone(5,-10,10)
		self.assertFalse(TestPosetConditions(C,D))

	def test_ConesEqual_2D(self):
		C = Polyhedron(rays=[[-1,1],[1,1]],backend='normaliz')
		D = C
		self.assertFalse(TestPosetConditions(C,D))


TestPosetConditionsTestNames = [Test_TestPosetConditions]
boxprint("TESTING TestPosetConditions.py")

for i in range(len(TestPosetConditionsTestNames)):
	printseparator()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestPosetConditionsTestNames[i])
	unittest.TextTestRunner(verbosity=2).run(suite)

