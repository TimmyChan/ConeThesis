""" Contains methods required to generate cones randomly."""

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
		C (sage.geometry.polyhedron): Cone with Normaliz Backend
		D (sage.geometry.polyhedron): Cone with Normaliz Backend
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
		SAGE vector: one with shortest norm.
		None: if the list is empty or there's some other error
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
		SAGE vector: one with longest norm.
		None: if the list is empty or there's some other error
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
		SAGE vector: v * 1/GCD(entries of v). 
	"""
    gcd = GCD_List(vectlist)
    # Store the GCD of the list of vectors,
    primvectlist = [(i / gcd) for i in vectlist] 
    # create new list where each entry of v is divided by gcd
    return vector(primvectlist)

def generate_random_vector(dim, rmax=10, verbose=False):
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
 