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
	"""Generate a random vector of the form (x_1, x_2, ..., x_(d-1), x_d)
	where each x_i is in the interval [-rmax,rmax] except x_d which is in [1,rmax]
	Args:
		dim (int): dimension of the ambient space, number of entries in vector
		rmax (int): max number for random number generator
	Returns:
	"""
	rmin = -rmax 
	vectlist  = [randint(rmin,rmax) for i in range(dim-1)]	
	# create a list d-1 of random numbers 
	vectlist.append(randint(1,rmax))	# append the last entry
	vect = make_primitive(vectlist)		# 
	return vect
 

def generate_cone(dim, rmax=10, numgen=10, file=None, verbose=False):
	""" Generates a random SAGE polyhedral cone C with Normaliz backend
	where C is pointed, proper,full dimensional and lies strictly in 
	the halfspace x_d > 0.
	Args:
		dim (int): dimension of the ambient space, number of entries in vector
		rmax (int): max number for random number generator
		numgen (int): number of generators. (Default = 10)
		file (FILE): for outputting data will migrate to JSON
		verbose (boolean): option for verbose mode
	Returns:
		Temp (SAGE.geometry.Polyhedron): SAGE cone object with Normaliz backend. 
	"""
	# Verbose option; 
	if verbose:
		def verboseprint(*args):
			for arg in args:
				print arg,
				if FILE <> None:
					FILE.write("\n"+str(arg))
			print
	else:
		verboseprint = lambda *a: None  # default verbose print does nothing


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

if __name__ == "__main__":
	for i in range(3):
		print("Generating Cone for dimension {}:".format(i+2))
		test_outer_cone = generate_cone(i+2, 10)
		test_inner_cone = generate_inner_cone(test_outer_cone)
		print("\tOuter cone has generators: \n\t{}".format(test_outer_cone.rays_list()))
		print("\tInner cone has generators: \n\t{}".format(test_inner_cone.rays_list()))

