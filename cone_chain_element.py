#!/usr/bin/env sage

"""ConeChain

This module defines ConeChainElement, an object that will contain experimental data for each cone.
"""

import sage.all
import cone_tools
import experiment_io_tools
import json 


class ConeChainElement(object):
	""" A data structure to hold a cone and its hilbert basis
	and associated experimental data.
	Class Attribute:
		(currently not used)
		num_hilbert_calc (int):		Keeps track of the number of times we call
									Hilbert basis calculations.
	Attributes:
		cone (sage.all.Polyhedron): the cone object to be stored
		cone_rays_list (list of lists):	extremal generators of cone object (mostly for JSON)
		generation_step (int):		step in the generation process
		algorithm_used (str):		"i" = initial step
									"t" = top down
									"b" = bottom up
		hilbert_basis (list of lists): Hilbert basis of cone
	"""
	# MAY NOT BE NECESSARY num_hilbert_calc = 0

	def __init__(self,cone,generation_step=0, algorithm_used="i", hilbert_basis=None):
		self.cone = cone
		self.cone_rays_list = cone.rays_list()
		self.generation_step = generation_step
		self.algorithm_used = algorithm_used
		self.hilbert_basis = hilbert_basis
		self.longest_hilbert_basis_element = None if hilbert_basis is None else cone_tools.longest_vector(self.hilbert_basis)

	def get_hilbert_basis(self):
		""" Retreives the hilbert basis, only calculates once. """
		# if the hilbert_basis data is empty, generate it using Normaliz and store it
		if self.hilbert_basis == None:
			self.hilbert_basis = list(self.cone.integral_points_generators()[1])
			#ConeChainElement.num_hilbert_calc += 1
		self.longest_hilbert_basis_element = cone_tools.longest_vector(self.hilbert_basis)
		
		#return the stored value.
		return self.hilbert_basis

	def get_longest_hilbert_basis_element(self):
		if self.longest_hilbert_basis_element == None:
			return cone_tools.longest_vector(self.get_hilbert_basis())
		return self.longest_hilbert_basis_element

	def hilbert_graph_data_size(self):
		return len(self.get_hilbert_basis())

	def hilbert_graph_data_length(self):
		return sage.all.vector(self.get_longest_hilbert_basis_element()).norm()

	def rays_list(self):
		"""Returns the extremal generators of the cone 
		self.cone.rays_list() (list of lists): normaliz returns this.
		"""
		return self.cone_rays_list

	def output_details(self):
		""" Prints basic details about this particular cone. """
		print("rays = {}".format(self.rays_list()))
		print("generated on step {} with algorithm {}".format(self.generation_step,self.algorithm_used))
		if self.hilbert_basis == None:
			L = 0
		else:
			L = len(self.hilbert_basis)
		print("number of elements in hilbert_basis = {}".format(L))

	def calculate(self):
		if self.hilbert_basis == None:
			self.hilbert_basis = list(self.cone.integral_points_generators()[1])
		self.longest_hilbert_basis_element = cone_tools.longest_vector(self.hilbert_basis)
		

class ConeChainElementEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, ConeChainElement):
			cone_rays_list_json = cone_tools.rays_list_to_json_array(obj.cone_rays_list)
			hilb_basis = cone_tools.rays_list_to_json_array(obj.hilbert_basis)
			return {'cone_rays_list' : cone_rays_list_json, 
				'generation_step' : obj.generation_step, 
				'algorithm_used' : obj.algorithm_used, 
				'hilbert_basis' : hilb_basis}
		return json.JSONEncoder.default(self, obj)

class ConeChainElementDecoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
	
	def object_hook(self, dictionary):
		if 'cone_rays_list' in dictionary:
			cone = sage.all.Polyhedron(rays=dictionary['cone_rays_list'],backend='normaliz')
		
		if dictionary['hilbert_basis'] == 'null':
			return ConeChainElement(cone,
				dictionary['generation_step'], 
				dictionary['algorithm_used'])
		
		else:
			return ConeChainElement(cone,
				dictionary['generation_step'], 
				dictionary['algorithm_used'],
				[sage.all.vector(v) for v in dictionary['hilbert_basis']])

