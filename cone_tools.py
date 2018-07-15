""" Contains methods required to generate cones randomly."""
from sage.all import *
from sage.misc import *
# Functions used to generate a primitive rational vector
def gcd(a,b):
	"""Greatest Common Divisor using Euclidean Algorithm
	Args: 
		a (int): some integer
		b (int): some integer
	Returns: 
		int: Greatest Common Divisor of a and b.
	""" 
	return abs(a) if b==0 else GCD(b, a%b)


def gcd_of_list(args):
	"""Greatest Common Divisor of a list of integers
	Intended for use to scale a lattice vector
	Args:
		args (list of int)
	Returns:
		int: Greatest Common Divisor of args.
	"""
	return reduce(GCD, args)


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
	return vector(primvectlist)


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
	vectlist  = [randint(-rmax,rmax) for i in range(dim-1)]
	# make the first n-1 entries
	vectlist.append(randint(1,rmax))
	# append the last entry  
	vect = makePrimitive(vectlist) 
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
	temp = Polyhedron(rays=[vector(v) for v in vects],backend='normaliz')
	# conical hull of vectors in list vects.
		
	while (not temp.is_full_dimensional()): 
		#keep looping until we have a full dimensional cone. 
		vects.append(generate_random_vector(dim,rmax))
		temp = Polyhedron(rays=[vector(v) for v in vects],
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
	inner = Polyhedron(rays=[vector(v) for v in vectlist],
					   backend='normaliz')		
	while not inner.is_full_dimensional():
		#keep looping until we have a full dimensional cone. 
		temp_vect = generate_random_vector(dim, rmax)
		if outer.contains(temp_vect):
			vectlist.append(temp_vect)
		inner = Polyhedron(rays=[vector(v) for v in vectlist],
						  backend='normaliz')
		# keep tacking on random vectors, eventually 
		# the convex hull will be full dimensional
	return inner

def poset_condition_verification(C,D):
	""" Verifies if the Poset condition is met by C, D 
	Default behavior for same cone given is to return True.
	We do this by checking the hilbert basis of C, then D,
	and verify that:
		1) One or less extremal generator of D is outside C, call this v
		2) Hilbert basis of D take away v should be a subset of
			the Hilbert basis of C.
	Args: 
		C (SAGE.geometry.Polyhedron): "inner" cone
		D (SAGE.geometry.Polyhedron): "outer" cone
	Returns: 
		poset_condition (Boolean): 	True if C, D satisify the poset condition
										or if they're the same cone;
									False otherwise.
	TODO:
		Maybe make this return a tuple, so that the hilbert basis calculation can be saved.
	"""

	# Computing Hilbert basis of C and D:
	HilbC = list(C.integral_points_generators()[1])
	HilbD = list(D.integral_points_generators()[1])

	# if they're the same cone just return true...
	if C == D:
		return True
	# Finding extremal generator of D not in C
	v = extremal_generators_outside_inner_cone(C,D)
	
	if len(v) > 1:
		# if there's more than one extremal generator outside of C, 
		# this cannot satisify the poset condition.
		return False
	# Removing the extremal generator (should be just one) from HilbD
	HilbD.remove(v[0])

	# Assume that the poset condition is satisified at this point, then
	# loop through each vector in the Hilbert basis of D, 
	poset_condition = True
	for vect in HilbD:
		# the poset condition will remain true as long as 
		# each vect in Hilbert basis of D is also
		# contained in the Hilbert basis of D
		poset_condition = poset_condition and (vect in HilbC) 
	
	return poset_condition

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
	ext_gens_final = [vector(i for i in v) for v in ext_gens]

	return ext_gens_final 

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

