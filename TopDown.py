
from sage.all import *
from PyNormaliz import *
from Init import *
import numpy as np

# Please note that to make a default cone in SAGE, one must now use 
# sage.geometry.cone.Cone(list), where list is a list of vectors.


#==================#
# GLOBAL VARIABLES #
#==================# 
# The number of generators used for the cone (useful for 3d and up)
NUMGEN = 10


# RESTRICTIONS ON RANDOM NUMBER GENERATOR. 
RMAX = 3
RMIN = -RMAX
INFINITYCORK = 1000000

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
	verboseprint("Extremal generators of Intermediate Cone: \n{}".format(Intermediate.rays()))
	for r in Intermediate.rays():
		if not C.contains(r):
			ExtremalNotinC.append(r)
	verboseprint("Extremal generators not contained in C: {}".format(ExtremalNotinC))
	
	VectorToRemove = min(ExtremalNotinC, key = lambda x: x.norm())
	verboseprint("Vector norms: {}".format([r.norm() for r in ExtremalNotinC]))
	verboseprint(VectorToRemove)
	verboseprint("Vector to remove = {} and its norm = {}".format(VectorToRemove,VectorToRemove.norm()))

	IntermediateHB = SAGEtoNormaliz(Intermediate).HilbertBasis()
	verboseprint("Hilbert Basis of Intermediate Cone: \n {}".format(IntermediateHB))

	IntermediateHB.remove(list([long(i) for i in VectorToRemove]))
	NewGenerators = IntermediateHB + list([list([long(i) for i in ray]) for ray in C.rays()])

	return sage.geometry.cone.Cone(NewGenerators)
	


def TOPDOWNtrial(dim,verbose=False):
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
    C, D, v = generateInitialConditions(dim,NUMGEN, RMIN, RMAX, verbose)
    # for now Testing:
    numC = len(C.rays())
    
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
    
    # STEP 4: look in the definition of TOPDOWNstep.
    counter = 1
    while ((not C.is_equivalent(IntermediateConeSAGE)) and (counter < INFINITYCORK)):
    	IntermediateConeSAGE = TOPDOWNstep(C,IntermediateConeSAGE, verbose)
    	counter = counter + 1
    	print("IntermediateConeSAGE = \n{}".format(IntermediateConeSAGE.rays()))
    	print("Step {}... Original number of extremal rays: {}, Now: {}".format(counter,numC, len(IntermediateConeSAGE.rays())))
    if C.is_equivalent(IntermediateConeSAGE):
        print("Finished in {} steps.\n Intermediate Cone = \n{}\n Goal Cone = \n{} Initial Cone = \n{} ".format(counter,IntermediateConeSAGE.rays(),C.rays(),D.rays()))


