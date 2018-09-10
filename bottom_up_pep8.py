from sage.all import *
from sage.misc import *
#import PyNormaliz as PyNormaliz
import numpy as np
from Init import *

def visible_facets(cone,vect):
	''' C is a full dimensional cone, v is external to C and returns 
			a list of facets [f1,f2,...,fn], where each f_i is visible WRT v 
		Args:
			cone (sage.all.Polyhedron): Some cone
			vect (sage vector): a vector outside of cone.
		Returns:
			visiblefacets (List of face): Returns a list of faces that are 
				visible to vect
	'''
	if cone.contains(vect):
		return None
	else:
		#print("v = {}\n C = \n{}".format(v,C.rays_list()))
		numfacets = len(cone.faces(cone.dim()-1)) # counts the number of facets of codimension 1

		facets = cone.faces(cone.dim()-1)
		visiblefacets = []
		for facet in facets:
			#print("Facet {}:".format(facets.index(facet)))
			facet_ineq = facet.ambient_Hrepresentation(0)
			#print("\tambient halfspace {}".format(facet_ineq))
			facet_visibile = (facet_ineq.eval(vector(vect)) < 0)
			#print facet_ineq.eval(vector(v))
			#print("\trays = {}".format(facet.as_polyhedron().rays_list()))
			if facet_visibile:
				visiblefacets.append(facet)
		
		return visiblefacets


def facets_with_max_lambda(visiblefacets,v):
	''' given visible facets, find max lambda '''
	return max(visiblefacets, key = lambda x: abs(x.ambient_Hrepresentation(0).eval(vector(v))))



def vector_sum(listofvectors):
	''' Returns vector sum of a given list of vectors  takes a list of vectors of the same dimension
	returns a vector that is the termwise sum of each vector in the list.
	'''
	length = len(listofvectors)
	dim = len(listofvectors[0])
	summand = [0 for i in range(dim)]
	for i in range(length):
		for d in range(dim):
			summand[d] = summand[d] + listofvectors[i][d]
	return summand


def zonotope_generators(vectlist):
	'''  Form a zonotope given v_1,...,v_n. Gives the vertices of said zonotope.
	Args:
		vectlist (list of vectors): assumes they're all same dimension.
	Returns:
		zonogens (list of vectors): vertices of a zonotope_generators generated
			by vectlist.
	'''

	# First create the powerset of the list	and remove the empty set.
	dimension = len(vectlist[0])
	combo = list(powerset(vectlist))
	combo.remove([])
	combo.append([[0 for i in range(dimension)]])
	#print combo
	zonogens = [vector_sum(c) for c in combo]
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
	# dimension of the space must be the length of each vector
	dimension = len(v)
	visibleFacetsofIntermediate = visible_facets(C,v)

	visiblemaxlambdaFacet = facets_with_max_lambda(visibleFacetsofIntermediate, v)

	generators =  visiblemaxlambdaFacet.as_polyhedron().rays_list()
	#print("generators of visible facet with max lambda = {}".format(generators))
	
	#print("generators of parallelopiped: {}".format(paragens))
	zonotope_gens = zonotope_generators(generators)

	ShiftFactor = 1/ abs(visiblemaxlambdaFacet.ambient_Hrepresentation(0).eval(vector(v)))

	#print("Lambda = {}".format(ShiftFactor))

	ShiftedVertex = [ShiftFactor*i for i in v]

	#print("Lambda v = {}".format(ShiftedVertex))
	#shiftedGenerators = [[gen[i] + ShiftedVertex[i] for i in range(dimension)] for gen in paragens]
	shiftedGenerators = [[gen[i] + ShiftedVertex[i] for i in range(dimension)] for gen in zonotope_gens]

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
	
	# Cone for interations
	Intermediate = C 

	# loop through each extremeal vector
	vlist = ExtremalGeneratorNotContainedbyInnerCone(Intermediate,D)
	counter = 0
	while vlist <> []:
		# if the list is empty, we're done. Print the list to show where we are...
		verboseprint("Extremal generators of D not in Intermediate: {}".format(vlist))
		# work on the longest vector first
		longestv = longestvector(vlist)
		counter = counter + 1
		if verbose:
			printseparator()
		verboseprint("Step {}".format(counter))
		# iterate through the algorithm once. 
		Intermediate = BOTTOMUPstep(Intermediate,longestv,FILE,verbose)
		# collect the list of extremal generators not in C again
		vlist = ExtremalGeneratorNotContainedbyInnerCone(Intermediate,D)

	return counter, C, D
	


def bottom_up(self):
	""" Bottom Up algorithm
	Args: none
	Returns: True if top_down completes the sequence
			 False if top_down isn't complete. 
	"""
		
	if self.sequence_complete:
		print("Sequence already complete.")
		return True

	current_inner = self.