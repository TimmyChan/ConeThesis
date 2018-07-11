"""ConeSequence

This module contains the an object that will contain a sequence of cones.

Attributes:
	Outer Cone
	Inner Cone

"""

import cone_tools

class ConeSequence(object):
	"""	Initializes with dimension (Integer)
	Generating Inner and Outer Cone,
	Contains a list ConeSequence[], which
	"""
	dimension = 0 
	def __init__(self,dimension,rmax=10):
		self.OuterCone = cone_tools.generate_cone(dimension, rmax)
		self.InnerCone = 


