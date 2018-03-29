from sage.all import *
from PyNormaliz import *



#=================================================#
# GENERATE INITIAL CONDITIONS FOR CONE EXPERIMENT #
#=================================================#
# Input: Number of extremeal generators (numgen) in the cone
# Description: Generates (numgen) many vectors in the halfspace z>0
#              and takes conical hull
# Returns: SAGE Cone
def generateCone(dim, numgen, RMIN, RMAX,verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None 

    vects = [[0 for i in range(dim)] for i in range(numgen)] # Empty list of vectors
    for i in range(numgen):
        vect = [randint(RMIN, RMAX) for j in range(dim-1)]        
        vect.append(randint(1,RMAX))
        vects[i] = vect
        verboseprint("Random Vector {} = {}".format(i,vects[i]))
    Temp = sage.geometry.cone.Cone([vector(v) for v in vects])
    print Temp.rays()
    return Temp

# Functions used to generate a primitive rational vector
def GCD(a,b):
    return abs(a) if b==0 else GCD(b, a%b)
def GCD_List(args):
    return reduce(GCD, args)


def generateRandomVector(dim, RMIN,RMAX,verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None 
    
    vectlist  = [randint(RMIN,RMAX) for i in range(dim-1)]
    vectlist.append(randint(1,RMAX))
    gcd = GCD_List(vectlist)
    verboseprint("vector before making it primitive = {}, gcd = {}".format(vectlist,gcd))
    primvectlist = [(i / gcd) for i in vectlist] 
    vect = vector(primvectlist)
    verboseprint("returning {}".format(vect))
    return vect
    


#Function that takes a SAGE 
def generateOutsideVector(dim, SAGECone, RMIN, RMAX,verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None 

    temp = generateRandomVector(dim, RMIN, RMAX,verbose)                                             # Generate Some Random Vector
    #print("Generating Random Vector: {}".format(temp))                        
    while(SAGECone.contains(temp) or SAGECone.contains(-1*temp)):               # Loop to verify v not in C and -v not in C
        if SAGECone.contains(temp):
            verboseprint("{} is in the Cone.".format(temp))
        else:
            verboseprint("{} is in the Cone.".format(-temp,someCone.contains(-temp)))
        temp = generateRandomVector(dim, RMIN,RMAX,verbose)
        #print("Generating Random Vector: {}".format(temp))     

    #print("All is well, returning: {}".format(temp))
    
    return temp


# This function returns two SAGE cones, C & D, and a vector v, where
# D is the conical hull of the extremal generators of C union v 
# input: dim - ambient dimension
#        gencount - number of extremal generators 
def generateInitialConditions(dim, gencount, RMIN, RMAX, verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None 
    verboseprint("=============Initializing Experiment============")
    InnerCone = generateCone(dim,gencount, RMIN, RMAX,verbose)
    OutsideVector = generateOutsideVector(dim, InnerCone, RMIN, RMAX,verbose)
    

    InnerConeGenerators = InnerCone.rays()             # Collect all extremal generators of the inner cone

    OuterConeGenerators = []
    for point in InnerConeGenerators:
        OuterConeGenerators.append(point)
    OuterConeGenerators.append(OutsideVector)
    OuterCone = sage.geometry.cone.Cone(OuterConeGenerators)
    #print OuterCone.rays

    #InnerCone = sage.geometry.cone.Cone([[-3,-1,1],[-3,0,1],[-2,-2,1],[2,0,1],[-2,2,1],[2,-1,1],[1,-3,1]])
    #OutsideVector = [3,1,1]
    #OuterCone = sage.geometry.cone.Cone([[-3,-1,1],[-3,0,1],[-2,-2,1],[2,0,1],[-2,2,1],[2,-1,1],[1,-3,1],[3,1,1]])
    
    verboseprint("Extremal Generators of the Inner Cone: \n{}".format(InnerCone.rays()))
    verboseprint("Vector Outside of Inner Cone: {}".format(OutsideVector))
    verboseprint("Extremal Generators of the Outer Cone: \n{}".format(OuterCone.rays()))

    verboseprint("=============Initialization Complete============")
    return InnerCone, OuterCone, OutsideVector
