#!/usr/bin/env sage
""" Contains methods required to generate cones randomly."""

import sys
import sage.all


def gcd_of_list(args):
	"""Greatest Common Divisor of a list of integers
	Intended for use to scale a lattice vector
	Args:
		args (list of int)
	Returns:
		int: Greatest Common Divisor of args.
	"""
	return reduce(sage.all.gcd, args)


def cone_containment(C,D):
	"""Verifies if cone C is contained in (or equals to) of D
	Args:
		C (SAGE.geometry.Polyhedron): Cone with Normaliz Backend
		D (SAGE.geometry.Polyhedron): Cone with Normaliz Backend
	Returns: 
		sofar (boolean): True for C contained in D, False otherwise.
	"""
	sofar = True
	for ray in C.rays():
		# loop through every extremal generators of C. 
		# If they're all in D then C is in D.
		sofar = (sofar and D.contains(ray))
	return sofar


def shortest_vector(vectorlist):
	"""Given a list of SAGE vectors, return shortest WRT Euclidean norm.
	Args:
		vectorlist (list of SAGE vectors): vectors, 
	Returns:
		min(vectorlist,key=lambda:x.norm()) (SAGE vector): one with shortest norm.
		if the list is empty or there's some other error, return None
	"""
	try:
		return min(vectorlist, key = lambda x: x.norm())
	except:
		return None 


def longest_vector(vectorlist):
	"""Given a list of SAGE vectors, return longest WRT Euclidean norm.
	Args:
		vectorlist (list of SAGE vectors): vectors, 
	Returns:
		min(vectorlist,key=lambda:x.norm()) (SAGE vector): one with longest norm.
		if the list is empty or there's some other error, return None
	"""
	try:
		return max(vectorlist, key = lambda x: x.norm()) 
	except:
		return None

	  
def make_primitive(vectlist):
	"""Given some vector v in Z^d, return primitive of v
	Args:
		vectlist (list of integers): list of length d representing some vector in Z^d
	Returns:
		vector(primvectlist) (SAGE vector): v * 1/GCD(entries of v). 
	"""
	gcd = gcd_of_list(vectlist)
	primvectlist = [(i / gcd) for i in vectlist] 
	return sage.all.vector(primvectlist)


def generate_random_vector(dim, rmax=10):
	""" Generate a random vector in Z^d
	Args:
		dim (int): ambient dimension
		rmax (int): upperbound for random number generator
	Returns:
		vect (SAGE vector): random vector of the form (x_1,...,x_(n-1),x_n)
		where -rmax < x_1,...,x_(n-1) < rmax
		and 1 < x_n < rmax.
		This guarentees that the cones generated with this vector lie within
		the halfspace x_n > 0, so forces all cones generated this way to be pointed.
	"""
	vectlist  = [sage.all.randint(-rmax,rmax) for i in range(dim-1)]
	# make the first n-1 entries
	vectlist.append(sage.all.randint(1,rmax))
	# append the last entry  
	vect = make_primitive(vectlist) 
	# make a primative vector and return it.
	return vect
 

def generate_cone(dim, rmax=10, numgen=10):
	""" Generates a random SAGE polyhedral cone C with Normaliz backend
	where C is pointed, proper,full dimensional and lies strictly in 
	the halfspace x_d > 0.
	Args:
		dim (int): dimension of the ambient space, number of entries in vector
		rmax (int): max number for random number generator
		numgen (int): number of generators. (Default = 10)
	Returns:
		Temp (SAGE.geometry.Polyhedron): SAGE cone object with Normaliz backend. 
	"""
	if numgen < dim: 			# catch: if numgen < dim, guarenteed not full dimensional. 
		numgen = int(dim) + 1 	# force numgen to have at least one more than the dimension.

	vects = [generate_random_vector(dim,rmax) for i in range(numgen)] # Empty list of vectors
	temp = sage.all.Polyhedron(rays=[sage.all.vector(v) for v in vects],backend='normaliz')
	# conical hull of vectors in list vects.
		
	while (not temp.is_full_dimensional()): 
		#keep looping until we have a full dimensional cone. 
		vects.append(generate_random_vector(dim,rmax))
		temp = sage.all.Polyhedron(rays=[sage.all.vector(v) for v in vects],
						  backend='normaliz')
		# keep tacking on random vectors, eventually 
		# the convex hull will be full dimensional
	return temp

def generate_inner_cone(outer, rmax=10, numgen=10):
	"""Generates a full dimensional cone that is contained by outer.
	Args:
		outer (SAGE.geometry.Polyhedron): Outer Cone
		rmax: upperbound for random number generator.
		numgen (int): number of generators
	Returns:
		inner (SAGE.geometry.Polyhedron): Inner Cone contained by outer cone
	"""
	dim = outer.dimension()
	# store the dimension of the outer cone
	vectlist = []
	# empty list to house the generator of cones
	while len(vectlist) < numgen:
		temp_vect = generate_random_vector(dim, rmax)
		if outer.contains(temp_vect):
			vectlist.append(temp_vect)
	inner = sage.all.Polyhedron(rays=[sage.all.vector(v) for v in vectlist],
					   backend='normaliz')		
	while not inner.is_full_dimensional():
		#keep looping until we have a full dimensional cone. 
		temp_vect = generate_random_vector(dim, rmax)
		if outer.contains(temp_vect):
			vectlist.append(temp_vect)
		inner = sage.all.Polyhedron(rays=[sage.all.vector(v) for v in vectlist],
						  backend='normaliz')
		# keep tacking on random vectors, eventually 
		# the convex hull will be full dimensional
	return inner


def extremal_generators_outside_inner_cone(inner, outer):
	""" Given inner, outer cone pair return extremal generators of outer cone
		not contained by inner cone
	Args:
		inner (SAGE.geometry.Polyhedron): cone of dimension d
		outer (SAGE.geometry.Polyhedron): contains inner cone of same ambient dimension
	Returns:
		ext_gens_final (List of SAGE vectors): list of extremal generators not in inner cone.
	"""
	# grab the outer cone's extremal generators and loop through each one:
	ext_gens = outer.rays_list()
	for r in outer.rays_list():
		# if r is inside of inner cone, discard it.
		if (inner.contains(r)):
			ext_gens.remove(r)
	# convert the lists into vectors			
	ext_gens_final = [sage.all.vector(i for i in v) for v in ext_gens]

	return ext_gens_final 


def poset_condition_checker(self, inner, outer):
	""" Verifies if the Poset condition is met by inner and outer
	Default behavior for same cone given is to return True.
	We do this by checking the hilbert basis of inner, then outer,
	and verify that:
		1) One or less extremal generator of outer is outside inner, call this v
		2) Hilbert basis of outer take away v should be a subset of
			the Hilbert basis of inner.
	Args: 
		inner (sage.all.Polyhedron): "inner" cone
		outer (sage.all.Polyhedron): "outer" cone (assume inner is contained)
	Returns: 
		poset_condition, hilbert_inner, hilbert_outer
		poset_condition (Boolean): 	True if C, D satisify the poset condition
										or if they're the same cone;
									False otherwise.
		hilbert_inner (list of lists): Hilbert Basis of inner cone
		hilbert_outer (list of lists): Hilbert Basis of outer cone.
	TODO:
		store hilbert basis calculated here into cone_dict -> key = inner / outer,
				value of first element of this list needs to change only.
	"""

	# Computing Hilbert basis of C and D:
	hilbert_inner = list(inner.integral_points_generators()[1])
	hilbert_outer = list(outer.integral_points_generators()[1])
	
	# TODO: store the hilbert basis into cone_dict 
	# 		ASK JUNE HOW

	# if they're the same cone just return true...
	if inner == outer:
		return True
	# Finding extremal generator of D not in C
	v = extremal_generators_outside_inner_cone(inner,outer)
	
	if len(v) > 1:
		# if there's more than one extremal generator outside of C, 
		# this cannot satisify the poset condition.
		return False
	# Removing the extremal generator (should be just one) from hilbert_working
	hilbert_outer.remove(v[0])

	# Assume that the poset condition is satisified at this point, then
	# loop through each vector in the Hilbert basis of D, 
	poset_condition = True
	for vect in hilbert_outer:
		# the poset condition will remain true as long as 
		# each vect in Hilbert basis of D is also
		# contained in the Hilbert basis of D
		poset_condition = poset_condition and (vect in hilbert_inner) 
	
	return poset_condition

##################
# Test Code Here #
##################

if __name__ == "__main__":
	for i in range(3):
		print("Generating Cone for dimension {}:".format(i+2))
		test_outer_cone = generate_cone(i+2, 10)
		test_inner_cone = generate_inner_cone(test_outer_cone)
		print("\tOuter cone has generators: \n\t{}".format(test_outer_cone.rays_list()))
		print("\tInner cone has generators: \n\t{}".format(test_inner_cone.rays_list()))

