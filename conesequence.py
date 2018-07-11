"""ConeSequence

This module contains the an object that will contain a sequence of cones.

Attributes:
	outer_cone (SAGE.geometry.Polyhedron): Normaliz backend cone
	inner_cone (SAGE.geometry.Polyhedron): Normaliz backend cone,
											contained inside outer_cone.

"""

import cone_tools

class ConeSequence(object):
	""" Initializes with dimension (Integer)
	Generating Inner and Outer Cone,
	Contains a list ConeSequence[], which
	"""
	def __init__(self,inner,outer,rmax=10):
		"""Initiate cones and a sequence to contain the cones"""
		self.outer_cone = outer
		self.inner_cone = inner
		self.cone_sequence = []
		self.sequence_complete = False
		self.sequence_analyzed = False
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



