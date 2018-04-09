from sage.all import *
import PyNormaliz as PyN
from Output import *

'''
Checks that given C_1, C_2:
	- C_1 is contained in C_2
	- L(C_2) = L(C_2) + Z_+ v for some v in C_2 but not in C_1
		* Achieve this by first listing out the inequalities of C_2
		* Negate each one so that we have the parts of C_1 compliment
		* Take the intersection of each of the inequalities from the step above with C_2
			- if the poset condition is met, the intersections will be a list of support hyperplanes except 1
			- that last 1 should be full dimension, but the hilbert basis should be some extremal generators of C with one v
		*Once we have v, we can verify that the monoid formed by L(C) and v is integrally closed
'''
def TestPosetConditions(Innerstep,Outerstep,verbose=False):
	if verbose:
		def verboseprint(*args):
			for arg in args:
				print arg,
			print
	else:
		verboseprint = lambda *a: None 

	''' Check that they're not equal '''
	if Outerstep == Innerstep:
		print("Same cone!")
		return False

	''' Check containment before running the test '''
	Innerstep_rays = Innerstep.rays_list()
	for ray in Innerstep_rays:
		if not Outerstep.contains(ray):
			print("Inner cone not a strict subset of Outer cone...")
			return False
	verboseprint("Innerstep contained in Outerstep... OK")

	''' 
	Verify that Innerstep and Outerstep
		- ambient dimensions match
		- Innerstep is full dimensional
		- Outerstep is full dimensional
	'''
	if not Innerstep.ambient_dim() == Outerstep.ambient_dim():
		print("Ambient dimensions mismatch! Inner lives in Z^{}, Outer lives in Z^{}.".format(Innerstep.ambient_dim(),Outerstep.ambient_dim()))
		return False
	if not Innerstep.is_full_dimensional():
		print("Inner cone not full dimensional!")
		return False
	if not Outerstep.is_full_dimensional():
		print("Outer cone not full dimensional!")
		return False
	verboseprint("Dimension checks... OK")
	dim = Innerstep.dim()


	# Go through the cone and name all the halfspaces by inequalities
	Inner_ieqs = Innerstep.inequalities_list()
	verboseprint(Inner_ieqs)
	verboseprint("The above list describes:")
	for i in range(len(Innerstep.inequalities())):
		verboseprint(Innerstep.inequalities()[i])

	# negate each one, so that the intersection of these new halfspaces forms the compliment of Innercone
	compliment_Ieqs = [[-1*x for x in ieqs] for ieqs in Inner_ieqs]
	verboseprint(compliment_Ieqs)

	# take each compliment_Ieqs and make a halfspace using Polyhedron() constructor:
	compliment_HS = [Polyhedron(ieqs=[ieq],backend='normaliz') for ieq in compliment_Ieqs]
	verboseprint(compliment_HS)

	# interesect each halfspace with Outerstep, then store in list intersections
	intersections = [Outerstep.intersection(HS) for HS in compliment_HS]
	for i in range(len(intersections)):
		verboseprint("Intersection {} is the conical hull of {}".format(i,intersections[i].rays_list()))

	# store all dimensions and verify that there should be just one of full dimension
	# all the others should be support hyperplanes of the inner cone.

	intersections_dimension = [intersection.dim() for intersection in intersections]
	verboseprint(intersections_dimension)

	# all but one intersections should have codimension 1
	if not intersections_dimension.count(dim-1) == len(intersections_dimension)-1:
		print("Not enough of the intersections resulted in support hyperplanes.")
		return False
	# only one should be full dimension.
	if not intersections_dimension.count(dim) == 1:
		print(" ")
		return False


	coneofinterest = max(intersections, key = lambda x: x.dim())
	rays_ConeofInterest = coneofinterest.rays_list()

	# get the hilbert basis of the cone of interest, and put it as list of list instead of vectors
	generators_ConeofInterest = [[x for x in point] for point in coneofinterest.integral_points_generators()[1]]
	verboseprint("Extremal generators of Outerstep\\Innerstep: \n\t{}".format(rays_ConeofInterest))
	verboseprint("Hilbert basis of Outerste\\Innerstep: \n\t{}".format(generators_ConeofInterest))

	if rays_ConeofInterest <> generators_ConeofInterest:
		print("We need more than one vector outside of inner cone to make the lattice of the difference!")
		return False

	for v in rays_ConeofInterest:
		if not Innerstep.contains(v):
			vectorofinterset = v


	Inner_HB = [[x for x in point] for point in Innerstep.integral_points_generators()[1]]
	Inner_HB_shifted = [[point[i] + vectorofinterset[i] for i in point] for point in Inner_HB] 
	TestList = Inner_HB + Inner_HB_shifted

	Testing = PyN.Cone(cone=TestList)
	verboseprint("At the end now testing to see if Cone(Hilb(C) union (Hilb(C)+v) is integrally closed")
	return Testing.IsIntegrallyClosed()

'''
#first try cones that work
C = Polyhedron(rays=[[0,0,1],[1,0,1],[0,1,1]],backend='normaliz')
D = C.convex_hull(Polyhedron(rays=[[1,1,1]]))

P = C.plot() + D.plot()
P.show()
printseparator()
print TestPosetConditions(C,D)



#try a pair of cones that DOESN'T work:
C = Polyhedron(rays=[[0,0,1],[1,0,1],[0,1,1]],backend='normaliz')
D = C.convex_hull(Polyhedron(rays=[[2,2,1]]))
printseparator()
print TestPosetConditions(C,D)
'''