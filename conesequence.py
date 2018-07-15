"""ConeSequence

This module contains the an object that will contain a sequence of cones.

Attributes:
	outer_cone (SAGE.geometry.Polyhedron): Normaliz backend cone
	inner_cone (SAGE.geometry.Polyhedron): Normaliz backend cone,
											contained inside outer_cone.

"""

import cone_tools

class ConeSequence(object):
	""" Initializes with two cones (assuming containment)
	
	We wish the represent the data so that a sequence of cones (poset)

		C = C_0 < ... < C_n = D

	can be "grown" from two ends, the tail or the head. 
	bottom_sequence: C = C_0 < C_1 < ... 
	top_sequence: D = D_0 > D_1 > ...
	
	After some steps, we expect C_n and D_k (for some finite n and k) 
		to satisify the poset condition. When this happens, we will glue the two together;
	cone_sequence: [C_0, C_1, ..., C_n, D_k, D_(k-1), ..., D_0]
		Note that top_sequence needs to be "glued" backwards for the containment to make sense!

	Attributes:
		outer_cone (SAGE.geometry.Polyhedron): A outer cone
		inner_cone (SAGE.geometry.Polyhedron): An inner cone
		top_sequence (list of SAGE.geometry.Polyhedron): Begins with outer_cone
		bottom_sequence (liset of SAGE.geometry.Polyhedron): Begins with inner_cone
	"""
	def __init__(self,inner,outer,rmax=10):
		"""Initiate using cones, then initialize data

		"""
		self.outer_cone = outer
		self.inner_cone = inner
		self.top_sequence = [outer]
		self.bottom_sequence = [inner]
		self.sequence_complete = False
		self.cone_sequence = []

	def get_inner_cone(self):
		""" Returns actual inner cone
		Args:
		Returns: 
			self.inner_cone (SAGE.geometry.Polyhedron)
			"""
		return self.inner_cone

	def inner_cone_rays(self):
		""" Returns a list of extremal generators of inner_cone
		Args:
		Returns: 
			self.inner_cone.rays_list()
		"""
		return self.inner_cone.rays_list()

	def get_outer_cone(self):
		""" Returns actual outer cone
		Args:
		Returns: 
			self.outer_cone (SAGE.geometry.Polyhedron)
			"""
		return self.outer_cone

	def outer_cone_rays(self):
		""" Returns a list of extremal generators of outer_cone
		Args:
		Returns: 
			self.outer_cone.rays_list()
		"""
		return self.outer_cone.rays_list()

	def append_top(self, somecone):
		""" Appends a cone to the top sequence """
		top_sequence.append(somecone)

	def append_bottom(self, somecone):
		""" Appends a cone to the bottom sequence """
		bottom_sequence.append(somecone)

	def check_complete(self):
		


if __name__ == "__main__":
	""" Some testing code here """
	for i in range(3):
		# loop through dimension 2 through 5
		dim = i +2
		outer = cone_tools.generate_cone(dim)
		inner = cone_tools.generate_inner_cone(outer)

		trial = ConeSequence(inner,outer)
		print("The inner cone has generators: \n{}".format(trial.inner_cone_rays()))
		print("The outer cone has generators: \n{}".format(trial.outer_cone_rays()))



