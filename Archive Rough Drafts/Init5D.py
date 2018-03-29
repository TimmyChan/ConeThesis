from sage.all import *
from PyNormaliz import *



#=================================================#
# GENERATE INITIAL CONDITIONS FOR CONE EXPERIMENT #
#=================================================#
# Input: Number of extremeal generators (numgen) in the cone
# Description: Generates (numgen) many vectors in the halfspace z>0
#              and takes conical hull
# Returns: SAGE Cone
def generateCone(dim, numgen, RMIN, RMAX):
    vects = [(0 for i in range(dim)) for i in range(numgen)] # Empty list of vectors
    for i in range(numgen):

        vects[i] = vector([randint(RMIN, RMAX) for i in range(dim)-1].append(1))
        #print("Random Vector {} = {}".format(i,vects[i]))
    Temp = sage.geometry.cone.Cone(vects)
    #print Temp.rays()
    return Temp

# Functions used to generate a primitive rational vector
def GCD(a,b):
    return abs(a) if b==0 else GCD(b, a%b)
def GCD_List(*args):
    return reduce(GCD, args)
def generateRandomVector(dim, RMIN,RMAX,verbose=False):
    vectlist  = [randint(RMIN,RMAX) for i in range(dim)-1]
    
    gcd = GCD_List(vectlist)
    verboseprint("vectlist = {}, gcd = {}".format(vectlist,gcd))
    vectlist = vectlist/gcd 
    vectlist = vectlist.append(1)
    vect = vector(vectlist)
    verboseprint("returning {}".format(vect))
    return vect
    


#Function that takes a SAGE 
def generateOutsideVector(dim, SAGECone, RMIN, RMAX):
    temp = generateRandomVector(RMIN, RMAX)                                             # Generate Some Random Vector
    #print("Generating Random Vector: {}".format(temp))                        
    while(SAGECone.contains(temp) or SAGECone.contains(-1*temp)):               # Loop to verify v not in C and -v not in C
        #if someCone.contains(temp):
            #print("{} is in the Cone.".format(temp))
        #else:
            #print("{} is in the Cone.".format(-temp,someCone.contains(-temp)))
        temp = generateRandomVector(dim, RMIN,RMAX)
        #print("Generating Random Vector: {}".format(temp))     

    #print("All is well, returning: {}".format(temp))
    
    return temp


# This function returns two SAGE cones, C & D, and a vector v, where
# D is the conical hull of the extremal generators of C union v 
def generateInitialConditions(dim, gencount, RMIN, RMAX, verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None 
    
    InnerCone = generateCone(dim,gencount, RMIN, RMAX)
    OutsideVector = generateOutsideVector(dim, InnerCone, RMIN, RMAX)
    
    InnerConeGenerators = InnerCone.rays()             # Collect all extremal generators of the inner cone

    OuterConeGenerators = []
    for point in InnerConeGenerators:
        OuterConeGenerators.append(point)
    OuterConeGenerators.append(OutsideVector)
    OuterCone = sage.geometry.cone.Cone(OuterConeGenerators)
    #print OuterCone.rays()
    return InnerCone, OuterCone, OutsideVector
