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

      
def makePrimitive(vectlist):
	"""Given some vector v in Z^d, return primitive of v
	Args:
		vectlist (list of integers): list of length d representing some vector in Z^d
	Returns:
		vector(primvectlist) (SAGE vector): v * 1/GCD(entries of v). 
	"""
    gcd = GCD_List(vectlist)
    primvectlist = [(i / gcd) for i in vectlist] 
    return vector(primvectlist)

def generateRandomVector(dim, RMIN, RMAX, verbose=False):
    vectlist  = [randint(RMIN,RMAX) for i in range(dim-1)]
    vectlist.append(randint(1,RMAX))
    # in testing, so currently ast digit is always 1
    #vectlist.append(1)

    
    vect = makePrimitive(vectlist)
    #verboseprint("returning {}".format(vect))
    return vect
 