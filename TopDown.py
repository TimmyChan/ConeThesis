from sage.all import *
from sage.misc import *
#import PyNormaliz as PyNormaliz
import numpy as np
from Init import *

# Please note that to make a default cone in SAGE, one must now use 
# sage.geometry.cone.Cone(list), where list is a list of vectors.



INFINITYCORK = 10000


def ExtremalGeneratorNotContainedbyInnerCone(Inner, Outer,FILE,verbose=False):
	if verbose:
		def verboseprint(*args):
			for arg in args:
				print arg,
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

# One step in the loop, step 4 in the psuedocode 
# Assumes Intermediate is a SAGE default cone object.
def TOPDOWNstep(C,Intermediate,FILE,verbose=False):
	if verbose:
		def verboseprint(*args):
			for arg in args:
				print arg,
				FILE.write("\n"+str(arg))
			print
	else:
		verboseprint = lambda *a: None 

	# Collect the set of extremal generators of the intermediate cone that is not in C
	ExtremalNotinC = ExtremalGeneratorNotContainedbyInnerCone(C, Intermediate,FILE,verbose)

	
	VectorToRemove = min(ExtremalNotinC, key = lambda x: x.norm())
	verboseprint("Vector norms: {}".format([r.norm() for r in ExtremalNotinC]))
	verboseprint("Vector to remove = {} and its norm = {}".format(VectorToRemove,VectorToRemove.norm()))

	IntermediateHB = list(Intermediate.integral_points_generators()[1])
	#verboseprint(IntermediateHB)
	#verboseprint("Hilbert Basis of Intermediate Cone: \n {}".format(IntermediateHB))

	IntermediateHB.remove(VectorToRemove)
	NewGenerators = IntermediateHB + list([list([long(i) for i in ray]) for ray in C.rays()])
	#verboseprint("Forming new cone with: \n{}".format(NewGenerators))
	verboseprint("Forming cone with {} vectors in Hilbert Basis of D + Extremal Generators of C.".format(len(NewGenerators)))
	return Polyhedron(rays=NewGenerators,backend='normaliz')
	


def TOPDOWNtrial(C,D,FILE,verbose=False):
	if verbose:
		def verboseprint(*args):
			for arg in args:
			   print arg,
			   FILE.write("\n"+str(arg))
			print
	else:
		verboseprint = lambda *a: None 
	
	numC = len(C.rays()) 	# number of extremal generaters in C
	dim = C.dim()			# ambient dimension (since C is assumed full dimension)
	# STEP 1: Set the "intermediate cone" to be D at the first step.
	IntermediateCone = D # IntermediateCone is a Polyhedron with normaliz backend


	if verbose and dim <= 3:
		PLOT = D.plot() + C.plot()
		PLOT.save(FILE.name[:-4] + "INITIAL CONDITION.png")

	# STEP 2: Get the Hilbert Basis for "intermediate cone".
	#IntermediateHilbertBasis = list(IntermediateCone.integral_points_generators()[1])
	#verboseprint("Hilbert Basis of D: {}".format(IntermediateHilbertBasis))
	#FILE.write("\nHilbert Basis of D: {}".format(IntermediateHilbertBasis))
	
	# STEP 3.1: Remove v from Hilb(D_0) or "intermediate hilbert basis" list 
	#IntermediateHilbertBasis.remove(v)
	#if not list([long(i) for i in v]) in IntermediateHilbertBasis:
	#	verboseprint("v removed ok")
	# STEP 3.2: Take the conical Hull of the list from step 3.1, iterate to next step.
	#FirstStepGenerators = IntermediateHilbertBasis + C.rays_list()
	#verboseprint("Taking Conical Hull of: \n{}".format(FirstStepGenerators))
	#IntermediateCone = Polyhedron(rays=FirstStepGenerators,backend='normaliz')

	# STEP 4: look in the definition of TOPDOWNstep.
	counter = 0
	if verbose and dim <= 3:
		PLOT = D.plot() + C.plot()
		PLOT.save(FILE.name[:-4] + "STEP {}.png".format(counter))

	IntermediateCone = D
	while (not C ==IntermediateCone):
		IntermediateCone = TOPDOWNstep(C,IntermediateCone,FILE,verbose)
		counter = counter + 1
		if verbose and dim <= 3:
			PLOT = IntermediateCone.plot() + D.plot()
			PLOT.save(FILE.name[:-4] + "STEP {}.png".format(counter))
		#print("IntermediateConeSAGE = \n{}".format(IntermediateConeSAGE.rays()))
		verboseprint("Finished Step {} - Original number of extremal rays: {}, Now: {}".format(counter,numC, len(IntermediateCone.rays())))
		#FILE.write("\nStep {}... Original number of extremal rays: {}, Now: {}".format(counter,numC, len(IntermediateCone.rays())))
		
		if not D.intersection(IntermediateCone) == IntermediateCone:
			print("ERROR: Intermediate Cone not in D")
			FILE.write("\nERROR: Intermediate Cone not in D")
			
			break
		if not IntermediateCone.intersection(C) == C:
			FILE.write("\nERROR: C not in Intermediate Cone")
			break
		#if not D.contains(IntermediateConeSAGE) or not IntermediateConeSAGE.contains(C):
		#	print("ERROR: D.contains(IntermediateConeSAGE) = {} \nIntermediateConeSAGE.contains(C) = {}".format(D.contains(IntermediateConeSAGE),IntermediateConeSAGE.contains(C)))
		#	break
		if counter >= INFINITYCORK:
			print("ERROR: At step {}, possible candidtate for nonterminating case...".format(counter))
			FILE.write("\nERROR: At step {}, possible candidtate for nonterminating case...".format(counter))
			PrintCD(C,D,FILE)
			break
	if C == IntermediateCone:
		verboseprint("\n Intermediate Cone = \n{}\n Goal Cone = \n{}\n Initial Cone = \n{}\n\tFinished in {} steps. ".format(IntermediateCone.rays_list(),C.rays_list(),D.rays_list(),counter))
		#FILE.write("\n Intermediate Cone = \n{}\n Goal Cone = \n{}\n Initial Cone = \n{}\n\tFinished in {} steps. ".format(IntermediateCone.rays_list(),C.rays_list(),D.rays_list(),counter))
	return counter, C, D 


