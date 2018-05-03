from sage.all import *
from Output import *
#from PyNormaliz import *

#=================================================#
# GENERATE INITIAL CONDITIONS FOR CONE EXPERIMENT #
#=================================================#

def stepcheck(C,D,verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
                print arg,
                if FILE <> None:
                    FILE.write("\n"+str(arg))
            print
    else:
        verboseprint = lambda *a: None 
    verboseprint("Checking that HilbD remove v subset of HilbC...")
    if C == D:
        #print("same cone!")
        return True
    verboseprint("\tComputing Hilbert basis of C...")
    HilbC = list(C.integral_points_generators()[1])

    verboseprint("\tComputing Hilbert basis of D...")
    HilbD = list(D.integral_points_generators()[1])
    verboseprint("\tFinding extremal generator of D not in C")
    v = ExtremalGeneratorNotContainedbyInnerCone(C,D)
    
    #print("HilbC = \n{}\nHilbD = \n{}\nv = {} ".format(HilbC,HilbD,v[0]))
    verboseprint("\t\tRemoving {} from HilbD".format(v))
    HilbD.remove(v[0])

    BOOL = True
    for vect in HilbD:
        BOOL = BOOL and (vect in HilbC) 
    verboseprint("\t\tHilbD \\ v  is a subset of HilbC? {}".format(BOOL))
    return BOOL

# Functions used to generate a primitive rational vector
def GCD(a,b):
    return abs(a) if b==0 else GCD(b, a%b)
def GCD_List(args):
    return reduce(GCD, args)

#checks to see if C is in D
def conecontainment(C,D):
    sofar = True
    for ray in C.rays():
        sofar = (sofar and D.contains(ray))
    return sofar

# expects a list of integer vectors, returns one with shortest norm.
def shortestvector(vectorlist):
    return min(vectorlist, key = lambda x: x.norm())

def longestvector(vectorlist):
    try:
        return max(vectorlist, key = lambda x: x.norm()) 
    except:
        return None

      
# takes a list of integers returns a primitive vector 
def makePrimitive(vectlist):
    gcd = GCD_List(vectlist)
    #verboseprint("vector before making it primitive = {}, gcd = {}".format(vectlist,gcd))
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
    

# returns True if C,D satisifies all hypothesis.
def sanitycheck(C,D):
    if not C.is_full_dimensional():
        print("C is not full dimensional!")
        printseparator()
        printseparator()
        print("RESTARTING INPUT!")
    if not D.is_full_dimensional():
        print("D is not full dimensional!")
        printseparator()
        printseparator()
        print("RESTARTING INPUT!")
    if not C.lines_list() == []:
        print("C is not proper!")
        printseparator()
        printseparator()
        print("RESTARTING INPUT!")
    if not D.lines_list() == []:
        print("D is not proper!")
        printseparator()
        printseparator()        
        print("RESTARTING INPUT!")
    if not conecontainment(C,D):
        print("C is not in D!")
        printseparator()
        printseparator()
        print("RESTARTING INPUT!")
    return (C.is_full_dimensional() and D.is_full_dimensional() and C.lines_list() == [] and D.lines_list() == [] and conecontainment(C,D))
        

def generateCone(dim, RMIN, RMAX, numgen=10, FILE=None, verbose=False):
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
    OuterCone = generateCone(dim, RMIN, RMAX, gencount, FILE,verbose)
    InnerConeGenerators = [(0 for i in range(dim))]
    while len(InnerConeGenerators) < gencount:
        temp = generateRandomVector(dim, RMIN, RMAX)
        if OuterCone.contains(temp):
            InnerConeGenerators.append(temp)
    InnerCone = Polyhedron(rays=InnerConeGenerators,backend='normaliz')
    #    OutsideVectorList = [generateOutsideVector(InnerCone, RMIN, RMAX,FILE,verbose) for i in range(gencount)]
    #    OuterCone = Polyhedron(rays=OutsideVectorList, backend='normaliz')
    


    verboseprint("Extremal Generators of the Inner Cone: \n{}".format(InnerCone.rays_list()))
    #verboseprint("Vector Outside of Inner Cone: {}".format(OutsideVector))
    verboseprint("Extremal Generators of the Outer Cone: \n{}".format(OuterCone.rays_list()))

    verboseprint("=============Initialization Complete============")
    return InnerCone, OuterCone#, OutsideVector


def ExtremalGeneratorNotContainedbyInnerCone(Inner, Outer,FILE=None,verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
                print arg,
                if FILE <> None:
                    FILE.write("\n"+str(arg))
            print
    else:
        verboseprint = lambda *a: None 
    if not Outer.intersection(Inner) == Inner : 
        print("Something is wrong!")
    #verboseprint("Extremal generators of Intermediate Cone: \n{}".format(Outer.rays_list()))
    ExtremalGenerators = Outer.rays_list()
    for r in Outer.rays_list():
        #print("Checking {}...".format(r))
        if (Inner.contains(r)):
            ExtremalGenerators.remove(r)
    ExtremalGeneratorsFinal = [vector(i for i in v) for v in ExtremalGenerators]
    verboseprint("Number of Extremal Generators NOT contained in C: {}".format(len(ExtremalGeneratorsFinal)))
    #verboseprint("Extremal generators not contained in C: {}".format(ExtremalGeneratorsFinal))
    #FILE.write("\nExtremal generators not contained in C: {}".format(ExtremalGeneratorsFinal))
    return ExtremalGeneratorsFinal







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
