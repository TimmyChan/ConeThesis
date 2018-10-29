#!/usr/bin/env sage
""" Contains methods required to generate cones randomly."""

import sys
import sage.all
import experiment_io_tools


def rays_list_to_json_array(rays_list):
	return None if rays_list is None else [[int(i) for i in v] for v in rays_list] 

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

	  
#####################################
# TOOLS FOR GENERATING RANDOM CONES #
#####################################

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

def generate_cone(dim, rmax=10, numgen=5):
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
		numgen = int(dim)  		# force numgen to have at least be full dimensional.

	vects = [generate_random_vector(dim,rmax) for i in range(numgen)] # Empty list of vectors
	temp = sage.all.Polyhedron(rays=[sage.all.vector(v) for v in vects],backend='normaliz')
	# conical hull of vectors in list vects.
	# DEBUG: print("\t attempting to generate a cone with {}...".format(vects))
	
	if dim > 2:
		while len(temp.rays_list())<numgen: 
			#print("len(temp.rays()), numgen: {}, {}".format(len(temp.rays_list()),numgen))
			#keep looping until we have a full dimensional cone. 
			vects.append(generate_random_vector(dim,rmax))
			#print("\t attempting to generate a cone with {}...".format(vects))
			temp = sage.all.Polyhedron(rays=[sage.all.vector(v) for v in vects],
							  backend='normaliz')
			# keep tacking on random vectors, eventually 
			# the convex hull will be full dimensional
	return temp

def generate_inner_cone(outer, rmax=10, numgen=5):
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
	if numgen < dim:
		numgen = int(dim)
	vectlist = []

	# empty list to house the generator of cones
	while len(vectlist) < numgen:
		temp_vect = generate_random_vector(dim, rmax)
		if outer.contains(temp_vect):
			vectlist.append(temp_vect)
	inner = sage.all.Polyhedron(rays=[sage.all.vector(v) for v in vectlist],
					   backend='normaliz')	
	if dim > 2:	
		while len(inner.rays_list())<numgen:
			#keep looping until we have a full dimensional cone. 
			temp_vect = generate_random_vector(dim, rmax)
			if outer.contains(temp_vect):
				vectlist.append(temp_vect)
			del inner
			inner = sage.all.Polyhedron(rays=[sage.all.vector(v) for v in vectlist],
							  backend='normaliz')
			# keep tacking on random vectors, eventually 
			# the convex hull will be full dimensional
	return inner








#################################
# TOOLS FOR BOTTOM UP ALGORITHM #
#################################

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


def visible_facets(cone,vect):
	''' C is a full dimensional cone, v is external to C and returns 
			a list of facets [f1,f2,...,fn], where each f_i is visible WRT v 
		Args:
			cone (sage.all.Polyhedron): Some cone
			vect (sage vector): a vector outside of cone.
		Returns:
			visiblefacets (List of face): Returns a list of faces that are 
				visible to vect
	'''
	if cone.contains(vect):
		return None
	else:
		#print("v = {}\n C = \n{}".format(v,C.rays_list()))
		numfacets = len(cone.faces(cone.dim()-1)) # counts the number of facets of codimension 1

		facets = cone.faces(cone.dim()-1)
		visiblefacets = []
		for facet in facets:
			#print("Facet {}:".format(facets.index(facet)))
			facet_ineq = facet.ambient_Hrepresentation(0)
			#print("\tambient halfspace {}".format(facet_ineq))
			facet_visibile = (facet_ineq.eval(sage.all.vector(vect)) < 0)
			#print facet_ineq.eval(vector(v))
			#print("\trays = {}".format(facet.as_polyhedron().rays_list()))
			if facet_visibile:
				visiblefacets.append(facet)
		
		return visiblefacets



def facets_with_max_lambda(visiblefacets,v):
	''' given visible facets, find max lambda '''
	return max(visiblefacets, key = lambda x: abs(x.ambient_Hrepresentation(0).eval(sage.all.vector(v))))


def vector_sum(listofvectors):
	''' Returns vector sum of a given list of vectors  takes a list of vectors of the same dimension
	returns a vector that is the termwise sum of each vector in the list.
	'''
	length = len(listofvectors)
	dim = len(listofvectors[0])
	summand = [0 for i in range(dim)]
	for i in range(length):
		for d in range(dim):
			summand[d] = summand[d] + listofvectors[i][d]
	return summand


def zonotope_generators(vectlist):
	'''  Form a zonotope given v_1,...,v_n. Gives the vertices of said zonotope.
	Args:
		vectlist (list of vectors): assumes they're all same dimension.
	Returns:
		zonogens (list of vectors): vertices of a zonotope_generators generated
			by vectlist.
	'''

	# First create the powerset of the list	and remove the empty set.
	dimension = len(vectlist[0])
	combo = list(sage.all.powerset(vectlist))
	combo.remove([])
	combo.append([[0 for i in range(dimension)]])
	#print combo
	zonogens = [vector_sum(c) for c in combo]
	#print zonogens
	#return Polyhedron(vertices=zonogens,backend='normaliz')
	return zonogens

# SANITY CHECK

def sanity_check(C,D):
    if not C.is_full_dimensional():
        print("C is not full dimensional!")
        experiment_io_tools.printseparator()
        experiment_io_tools.printseparator()
        print("RESTARTING INPUT!")
    if not D.is_full_dimensional():
        print("D is not full dimensional!")
        experiment_io_tools.printseparator()
        experiment_io_tools.printseparator()
        print("RESTARTING INPUT!")
    if not C.lines_list() == []:
        print("C is not proper!")
        experiment_io_tools.printseparator()
        experiment_io_tools.printseparator()
        print("RESTARTING INPUT!")
    if not D.lines_list() == []:
        print("D is not proper!")
        experiment_io_tools.printseparator()
        experiment_io_tools.printseparator()        
        print("RESTARTING INPUT!")
    if not cone_containment(C,D):
        print("C is not in D!")
        experiment_io_tools.printseparator()
        experiment_io_tools.printseparator()
        print("RESTARTING INPUT!")
    return (C.is_full_dimensional() and D.is_full_dimensional() and C.lines_list() == [] and D.lines_list() == [] and cone_containment(C,D))



##################
# Test Code Here #
##################

if __name__ == "__main__":
	for i in range(3):
		for j in range(i+2,i+5):
			print("Generating Cone for dimension {} with {} vectors:".format(i+2,j))
			test_outer_cone = generate_cone(i+2, numgen=j)
			test_inner_cone = generate_inner_cone(test_outer_cone, numgen=j)
			print("\tOuter cone has generators: \n\t{}".format(test_outer_cone.rays_list()))
			print("\tInner cone has generators: \n\t{}".format(test_inner_cone.rays_list()))

