
from sage.all import *
from PyNormaliz import *
from Init4D import *
import numpy as np

FILE = open('RawDataTopDown3D','a')

# Please note that to make a default cone in SAGE, one must now use 
# sage.geometry.cone.Cone(list), where list is a list of vectors.


#==================#
# GLOBAL VARIABLES #
#==================# 

NUMOFTRIALS = 10
NUMOFTESTS = 100

# The number of generators used for the cone (useful for 3d and up)
NUMGEN = 10


# RESTRICTIONS ON RANDOM NUMBER GENERATOR. 
RMAX = 2
RMIN = -RMAX
INFINITYCORK = RMAX^2

# Takes the sage.geometry.cone.Cone() object and returns an equaivalent object in Normaliz
def SAGEtoNormaliz(ConeSAGE):
	ConeGenerators = ConeSAGE.rays()

	# Get a numpy matrix so that we can use .tolist()
	ConeGeneratorsinMatrixForm = np.matrix(ConeGenerators.matrix())    
	return Cone(cone=ConeGeneratorsinMatrixForm.tolist())



# One step in the loop, step 4 in the psuedocode 
# Assumes Intermediate is a SAGE default cone object.
def TOPDOWNstep(C,Intermediate, verbose=False):
	if verbose:
		def verboseprint(*args):
			for arg in args:
				print arg,
			print
	else:
		verboseprint = lambda *a: None 

	# Collect the set of extremal generators of the intermediate cone that is not in C
	ExtremalNotinC = []
	verboseprint("Extremal generators of Intermediate Cone: {}".format(Intermediate.rays()))
	for r in Intermediate.rays():
		if not C.contains(r):
			ExtremalNotinC.append(r)
	verboseprint("Extremal generators not contained in C: {}".format(ExtremalNotinC))
	
	VectorToRemove = min(ExtremalNotinC, key = lambda x: x.norm())
	verboseprint("Vector norms: {}".format([r.norm() for r in ExtremalNotinC]))
	verboseprint(VectorToRemove)
	verboseprint("Vector to remove = {} and its norm = {}".format(VectorToRemove,VectorToRemove.norm()))

	IntermediateHB = SAGEtoNormaliz(Intermediate).HilbertBasis()
	IntermediateHB.remove(list([long(i) for i in VectorToRemove]))
	NewGenerators = IntermediateHB + list([list([long(i) for i in ray]) for ray in C.rays()])

	return sage.geometry.cone.Cone(NewGenerators)
	


def TOPDOWNtrial(verbose=False):
    if verbose:
        def verboseprint(*args):
            for arg in args:
               print arg,
            print
    else:
        verboseprint = lambda *a: None 
    
    # Initialize conditions 
    # C is the inner cone
    # D is the conical hull of the union of the extremal generators of C and v
    C, D, v = generateInitialConditions(NUMGEN, RMIN, RMAX, verbose)
    
    numC = len(C.rays())

    print("Extremal Generators of the Inner Cone: \n{}".format(C.rays()))
    print("Vector Outside of Inner Cone: {}".format(v))
    print("Extremal Generators of the Outer Cone: \n{}".format(D.rays()))
    
    # STEP 1: Set the "intermediate cone" to be D at the first step.
    IntermediateCone = SAGEtoNormaliz(D) # IntermediateCone IS A NORMALIZ OBJECT!!!

    # STEP 2: Get the Hilbert Basis for "intermediate cone".
    IntermediateHilbertBasis = IntermediateCone.HilbertBasis()
    verboseprint("Hilbert Basis of D: {}".format(IntermediateHilbertBasis))
    
    # STEP 3.1: Remove v from Hilb(D_0) or "intermediate hilbert basis" list 
    IntermediateHilbertBasis.remove(list([long(i) for i in v]))
    if not list([long(i) for i in v]) in IntermediateHilbertBasis:
    	verboseprint("v removed ok")
  	# STEP 3.2: Take the conical Hull of the list from step 3.1, iterate to next step.
    IntermediateConeSAGE = sage.geometry.cone.Cone(IntermediateHilbertBasis)
    
    counter = 1
    while not C.is_equivalent(IntermediateConeSAGE):
    	IntermediateConeSAGE = TOPDOWNstep(C,IntermediateConeSAGE, verbose)
    	counter = counter + 1
    	print("IntermediateConeSAGE = {}".format(IntermediateConeSAGE.rays()))  	
    	print("Step {}... Original number of extremal rays: {}, Now: {}".format(counter,numC, len(IntermediateConeSAGE.rays())))


TOPDOWNtrial()
