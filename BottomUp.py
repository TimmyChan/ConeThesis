from sage.all import *
from sage.misc import *
#import PyNormaliz as PyNormaliz
import numpy as np
from Init import *

# Function takes on C, v: v is external to C
# 	Returns a list of facets [f1,f2,...,fn], where each f_i is visible WRT v
def facetsVisiblefromV(C,v):

	if C.contains(v):
		return None
	else:
		#print("v = {}\n C = \n{}".format(v,C.rays_list()))
		numfacets = len(C.faces(C.dim()-1)) # counts the number of facets of codimension 1

		facets = C.faces(C.dim()-1)
		#print("Number of facets of C = {} = {}".format(numfacets,len(facets)))
		#print facets
		visiblefacets = []
		for facet in facets:
			#print("Facet {}:".format(facets.index(facet)))
			facetIneq = facet.ambient_Hrepresentation(0)
			#print("\tambient halfspace {}".format(facetIneq))
			facetIsVisibile = (facetIneq.eval(vector(v)) < 0)
			#print facetIneq.eval(vector(v))
			#print("\trays = {}".format(facet.as_polyhedron().rays_list()))
			if facetIsVisibile:
				#print("\t Facet {} visible!".format(facets.index(facet)))
				visiblefacets.append(facet)
		#print visiblefacets
		return visiblefacets


def facetsMaxLambda(visiblefacets,v):
	return max(visiblefacets, key = lambda x: abs(x.ambient_Hrepresentation(0).eval(vector(v))))


# takes a list of vectors of the same dimension
# returns a vector that is the termwise sum of each vector in the list.

def vectorsum(listofvectors):
	length = len(listofvectors)
	dim = len(listofvectors[0])
	summand = [0 for i in range(dim)]
	for i in range(length):
		for d in range(dim):
			summand[d] = summand[d] + listofvectors[i][d]
	return summand

def zonotope(vectlist):
	n = len(vectlist)
	dim = len(vectlist[0])
	combo = list(powerset(vectlist))
	combo.remove([])
	#print combo
	zonogens = [vectorsum(c) for c in combo]
	#print zonogens
	#return Polyhedron(vertices=zonogens,backend='normaliz')
	return zonogens


def BOTTOMUPstep(C,v,FILE=None,verbose=False):
	if verbose:
		def verboseprint(*args):
			for arg in args:
				print arg,
				if FILE <> None:
					FILE.write("\n"+str(arg))
			print
	else:
		verboseprint = lambda *a: None 

	dimension = len(v)
	visibleFacetsofIntermediate = facetsVisiblefromV(C,v)

	visiblemaxlambdaFacet = facetsMaxLambda(visibleFacetsofIntermediate, v)

	generators =  visiblemaxlambdaFacet.as_polyhedron().rays_list()
	#print("generators of visible facet with max lambda = {}".format(generators))
	
	#print("generators of parallelopiped: {}".format(paragens))
	zonotopeGenerators = zonotope(generators)

	ShiftFactor = 1/ abs(visiblemaxlambdaFacet.ambient_Hrepresentation(0).eval(vector(v)))

	#print("Lambda = {}".format(ShiftFactor))

	ShiftedVertex = [ShiftFactor*i for i in v]

	#print("Lambda v = {}".format(ShiftedVertex))
	#shiftedGenerators = [[gen[i] + ShiftedVertex[i] for i in range(dimension)] for gen in paragens]
	shiftedGenerators = [[gen[i] + ShiftedVertex[i] for i in range(dimension)] for gen in zonotopeGenerators]

	shiftedGenerators.append(ShiftedVertex)


	#print shiftedGenerators


	zono = Polyhedron(vertices=shiftedGenerators,backend='normaliz')
	#print zono
	integralpoints = list(zono.integral_points())
	#print integralpoints
	shortestIntegralPoint = shortestvector(integralpoints)
	verboseprint("Returning the convex hull of Intermediate with {}...".format(shortestIntegralPoint))
	return C.convex_hull(Polyhedron(rays=[shortestIntegralPoint],backend='normaliz'))

def BOTTOMUPtrial(C,D,FILE=None,verbose=False):
	if verbose:
		def verboseprint(*args):
			for arg in args:
				print arg,
				if FILE <> None:
					FILE.write("\n"+str(arg))
			print
	else:
		verboseprint = lambda *a: None 
	

	Intermediate = C 

	# loop through each extremeal vector
	vlist = ExtremalGeneratorNotContainedbyInnerCone(Intermediate,D)
	counter = 0
	while vlist <> []:
		verboseprint("Extremal generators of D not in Intermediate: {}".format(vlist))
		longestv = longestvector(vlist)
		counter = counter + 1
		if verbose:
			printseparator()
		verboseprint("Step {}".format(counter))
		Intermediate = BOTTOMUPstep(Intermediate,longestv,FILE,verbose)
		vlist = ExtremalGeneratorNotContainedbyInnerCone(Intermediate,D)

	return counter, C, D
	
'''

C,D = generateInitialConditions(2, 0, 100)
dimension = C.dim()
sanitycheck(C,D)
print("C generated by: {}".format(C.rays_list()))
print("D generated by: {}".format(D.rays_list()))


BOTTOMUPtrial(C,D,verbose=True)

'''