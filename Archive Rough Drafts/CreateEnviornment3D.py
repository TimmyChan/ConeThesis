from sage.all import *
from PyNormaliz import *

#=============================#
# GENERATE INITIAL CONDITIONS #
#=============================#

# Temporary Function
# Input: Number of extremeal generators (numgen) in the cone
# Description: Generates (numgen) many vectors in the halfspace z>0
#              and takes conical hull
# Returns: Cone
def generateCone(numgen, RMIN, RMAX):
    vects = [(0,0,0) for i in range(numgen)] # Empty list of vectors
    for i in range(numgen):
        vects[i] = (randint(RMIN,RMAX),randint(RMIN,RMAX),randint(1,RMAX))
        #print("Random Vector {} = {}".format(i,vects[i]))
    Temp = Cone(cone=vects)
    #print Temp.rays()
    return Temp


# Function to generate a primitive rational vector
def GCD(a,b):
    return abs(a) if b==0 else GCD(b, a%b)
def GCD_List(*args):
    return reduce(GCD, args)
def generateRandomVector(RMIN,RMAX):
    a = randint(RMIN, RMAX)
    b = randint(RMIN, RMAX)
    c = randint(RMIN, RMAX)
    d = GCD_List(a,b,c)
    return vector([a/d,b/d,c/d])

def generateOutsideVector(someCone, RMIN, RMAX):
    temp = generateRandomVector(RMIN, RMAX)                                             # Generate Some Random Vector
    #print("Generating Random Vector: {}".format(temp))                        
    while(someCone.contains(temp) or someCone.contains(-temp)):               # Loop to verify v not in C and -v not in C
        #if someCone.contains(temp):
            #print("{} is in the Cone.".format(temp))
        #else:
            #print("{} is in the Cone.".format(-temp,someCone.contains(-temp)))
        temp = generateRandomVector()
        #print("Generating Random Vector: {}".format(temp))     

    #print("All is well, returning: {}".format(temp))
    
    return temp

def generateInitialConditions(gencount, RMIN, RMAX, verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None 
    
    InnerCone = generateCone(gencount, RMIN, RMAX)
    OutsideVector = generateOutsideVector(InnerCone, RMIN, RMAX)
    
    InnerConeGenerators = InnerCone.rays()             # Collect all extremal generators of the inner cone

    OuterConeGenerators = []
    for point in InnerConeGenerators:
        OuterConeGenerators.append(point)
    OuterConeGenerators.append(OutsideVector)
    OuterCone = Cone(OuterConeGenerators)
    #print OuterCone.rays()
    return InnerCone, OuterCone, OutsideVector
