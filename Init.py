from sage.all import *
#from PyNormaliz import *



#=================================================#
# GENERATE INITIAL CONDITIONS FOR CONE EXPERIMENT #
#=================================================#
# Input: Number of extremeal generators (numgen) in the cone
# Description: Generates (numgen) many vectors in the halfspace z>0
#              and takes conical hull
# Returns: SAGE Cone


# Functions used to generate a primitive rational vector
def GCD(a,b):
    return abs(a) if b==0 else GCD(b, a%b)
def GCD_List(args):
    return reduce(GCD, args)


def generateRandomVector(dim, RMIN, RMAX, verbose=False):
    vectlist  = [randint(RMIN,RMAX) for i in range(dim-1)]
    vectlist.append(randint(1,RMAX))
    # in testing, so currently ast digit is always 1
    #vectlist.append(1)

    gcd = GCD_List(vectlist)
    #verboseprint("vector before making it primitive = {}, gcd = {}".format(vectlist,gcd))
    primvectlist = [(i / gcd) for i in vectlist] 
    vect = vector(primvectlist)
    #verboseprint("returning {}".format(vect))
    return vect
    
def generateCone(dim, RMIN, RMAX, numgen= dim, FILE=None, verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
                print arg,
                if FILE <> None:
                    FILE.write("\n"+str(arg))
            print

    else:
        verboseprint = lambda *a: None 

    if numgen < dim: 
        numgen = int(dim) + 1
    while True: 
    #keep looping until we have a full dimensional cone. Shouldn't take very long unless the bounds for RMAX is set very low and NUMGEN is close to dim
        vects = [generateRandomVector(dim,RMIN,RMAX,verbose) for i in range(numgen)] # Empty list of vectors
        verboseprint("Generating Cone with: \n{}\n...\n".format(vects))
        Temp = Polyhedron(rays=[vector(v) for v in vects],backend='normaliz')
        # make sure the cone we return satisifies the conditions:
        if Temp.is_full_dimensional():
            break
        #print Temp.rays()
    return Temp


#Function that takes a Cone that is a Polyhedron with normaliz backed
# and returns a vector that is outside of the cone. 
def generateOutsideVector(Cone, RMIN, RMAX,FILE=None,verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
                print arg,
                if FILE <> None:
                    FILE.write("\n"+str(arg))
            print
    else:
        verboseprint = lambda *a: None 
    dim = Cone.dim()
    temp = generateRandomVector(dim, RMIN, RMAX,verbose)                        # Generate Some Random Vector
    #print("Generating Random Vector: {}".format(temp))                        
    while(Cone.contains(temp) or Cone.contains(-1*temp)):               # Loop to verify v not in C and -v not in C
        if Cone.contains(temp):
            verboseprint("{} is in the Cone.".format(temp))
        else:
            verboseprint("{} is in the Cone.".format(-temp))
        temp = generateRandomVector(dim, RMIN,RMAX,verbose)
        #print("Generating Random Vector: {}".format(temp))     

    #print("All is well, returning: {}".format(temp))
    
    return temp


# This function returns two SAGE cones, C & D, and a vector v, where
# D is the conical hull of the extremal generators of C union v 
# input: dim - ambient dimension
#        gencount - number of extremal generators 
def generateInitialConditions(dim, RMIN, RMAX, gencount=10, FILE=None, verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
                print arg,
                if FILE <> None:
                    FILE.write("\n"+str(arg))
            print
    else:
        verboseprint = lambda *a: None 
    verboseprint("\n=============Initializing Experiment============")
    InnerCone = generateCone(dim, RMIN, RMAX, gencount, FILE,verbose)
    OutsideVector = generateOutsideVector(InnerCone, RMIN, RMAX,FILE,verbose)
    OuterCone = InnerCone.convex_hull(Polyhedron(rays=[OutsideVector], backend='normaliz'))
    #print OuterCone.rays_list()
    #print OuterCone.lines_list()
    #InnerConeGenerators = InnerCone.rays()             # Collect all extremal generators of the inner cone
    #OuterConeGenerators = []
    #for point in InnerConeGenerators:
    #    OuterConeGenerators.append(point)
    #OuterConeGenerators.append(OutsideVector)
    #OuterCone = Polyhedron(rays=OuterConeGenerators,backend='normaliz')  
    #print OuterCone.rays


    verboseprint("Extremal Generators of the Inner Cone: \n{}".format(InnerCone.rays()))
    verboseprint("Vector Outside of Inner Cone: {}".format(OutsideVector))
    verboseprint("Extremal Generators of the Outer Cone: \n{}".format(OuterCone.rays()))

    verboseprint("=============Initialization Complete============")
    return InnerCone, OuterCone, OutsideVector
