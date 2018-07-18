"""ConeSequence

This module contains the an object that will contain a sequence of cones.
"""

import cone_tools

class TimmyCone(object):
	""" A data structure to hold a cone and its hilbert basis
	Attributes:
		cone (sage.all.Polyhedron): the cone object to be stored
		generation_step (int):		step in the generation process
		algorithm_used (str):		"i" = initial step
									"t" = top down
									"b" = bottom up
		hilbert_basis (list of lists): Hilbert basis of cone
	"""
	def __init__(self,cone,generation_step, algorithm_used, hilbert_basis=None)
		self.cone = cone
		self.generation_step = generation_step
		self.algorithm_used = algorithm_used
		self.hilbert_basis = hilbert_basis

	

class ConeChain(object):
	""" Initializes with two cones (assuming containment)
	
	We wish the represent the data so that a sequence of cones (poset)

		C = C_0 < ... < C_n = D

	can be "grown" from two ends, the tail or the head so that

	bottom_sequence: C = C_0 < C_1 < ... 
	top_sequence: D = D_0 > D_1 > ...
	
	After some steps, we expect C_n and D_k (for some finite n and k) 
		to satisify the poset condition. When this happens, we will glue the two together;
	cone_sequence: [C_0, C_1, ..., C_n, D_k, D_(k-1), ..., D_0]
		Note that top_sequence needs to be "glued" backwards for the containment to make sense!

	Attributes:
		outer_cone (sage.all.Polyhedron): A outer cone
		inner_cone (sage.all.Polyhedron): An inner cone
		top_sequence (list of TimmyCones): Begins with outer_cone
		bottom_sequence (list of TimmyCones): Begins with inner_cone
		cone_sequence (list of TimmyCones): Begins empty until glue()
			intended to contain the order of the algorithmetically generated poset chain.
	"""
	def __init__(self,inner,outer,rmax=10):
		"""Initiate using cones, then initialize data	"""
		self.outer_cone = outer
		self.inner_cone = inner

		# Lists to store poset elements
		self.top_sequence = [TimmyCone(outer,0,"i")]
		self.bottom_sequence = [TimmyCone(inner,0,"i")]		
		self.cone_sequence = []

		# Internal logic flags
		self.sequence_complete = False # sequence complete whenever the poset condition is satisified.
		self.poset_chain = False # sequence is considered a poset chain when verfiication is checked for every cone.

		# Dictionary to hold data associated with each cone in the sequences.
		self.cone_dict = {	self.outer_cone:(list(self.outer_cone.integral_points_generators()[1]),"i",0),
							self.inner_cone:(list(self.inner_cone.integral_points_generators()[1]),"i",0)}
	

	def current_inner(self):
		""" get the current inner cone 
		Args: none
		Returns: bottom_sequence[-1].cone (sage.all.Polyhedron)
		"""
		return self.bottom_sequence[-1].cone


	def current_outer(self):
		""" get the current outer cone 
		Args: none
		Returns: top_sequence[-1].cone (sage.all.Polyhedron)
		"""
		return self.top_sequence[-1].cone


	def append_top(self, somecone):
		""" Appends a cone to the top sequence and adds to cone_dict
		Args:
			somecone (sage.all.Polyhedron): A polyhedral cone
		Returns: none.
		"""
		self.top_sequence.append(somecone)
		self.cone_dict[somecone] = ([],"t",self.number_of_steps())


	def append_bottom(self, somecone):
		""" Appends a cone to the bottom sequence and adds to cone_dict
		Args:
			somecone (sage.all.Polyhedron): A polyhedral cone
		Returns: none.
		"""self.bottom_sequence.append(somecone)
		self.cone_dict[somecone] = ([],"b",self.number_of_steps())


	def number_of_steps(self):
		""" Returns the number of steps """
		if self.sequence_complete:
			return len(self.cone_sequence) - 2  
		else:
			return len(self.top_sequence) + len(self.bottom_sequence) - 2 


	def verify_validity(self):
		""" Loops through the sequences as appropriate and checks poset conditions
		Note: This is a computationally heavy function, and should not be used frequently
			For optimization, this should be ran once per experiment, instead of for every trial.
		Args: none
		Returns: True - sequence is valid
		"""
		if self.sequence_complete:
			for i in range(len(self.cone_sequence)-1):

		else:
			if len(self.bottom_sequence) > 1:
				for i in range(len(self.bottom_sequence)-1):
					if not self.poset_condition_checker(self.bottom_sequence[i], self.bottom_sequence[i+1])
						return False
			if len(self.top_sequence) > 1:
				for i in range(len(self.top_sequence)-1):
					if not self.poset_condition_checker(self.top_sequence[i], self.bottom_sequence[i+1])
						return False
		return True

	def check_complete(self):
		""" Checks if the sequence is complete 
		1) verify the poset conditions on the last entries of
			top_sequence and bottom_sequence.
		2) if the poset condition is met, glue the bottom_sequence and 
			top_sequence together into cone_sequence.
		Args: Nothing
		Returns: Nothing.
		"""
		# sequence is complete if the poset condition is met for the two intermediate cones
		self.sequence_complete = 
			cone_tools.poset_condition_checker(	self.bottom_sequence[-1],
												self.top_sequence[-1])
		# if the sequence is complete, we should glue them together.
		if self.sequence_complete:
			self.glue()


	def poset_condition_checker(self, inner, outer):
		""" Verifies if the Poset condition is met by inner and outer
		Default behavior for same cone given is to return True.
		We do this by checking the hilbert basis of inner, then outer,
		and verify that:
			1) One or less extremal generator of outer is outside inner, call this v
			2) Hilbert basis of outer take away v should be a subset of
				the Hilbert basis of inner.
		Args: 
			inner (sage.all.Polyhedron): "inner" cone
			outer (sage.all.Polyhedron): "outer" cone (assume inner is contained)
		Returns: 
			poset_condition, hilbert_inner, hilbert_outer
			poset_condition (Boolean): 	True if C, D satisify the poset condition
											or if they're the same cone;
										False otherwise.
			hilbert_inner (list of lists): Hilbert Basis of inner cone
			hilbert_outer (list of lists): Hilbert Basis of outer cone.
		TODO:
			store hilbert basis calculated here into cone_dict -> key = inner / outer,
					value of first element of this list needs to change only.
		"""

		# Computing Hilbert basis of C and D:
		hilbert_inner = list(inner.integral_points_generators()[1])
		hilbert_outer = list(outer.integral_points_generators()[1])
		
		# TODO: store the hilbert basis into cone_dict 
		# 		ASK JUNE HOW

		# if they're the same cone just return true...
		if inner == outer:
			return True
		# Finding extremal generator of D not in C
		v = extremal_generators_outside_inner_cone(inner,outer)
		
		if len(v) > 1:
			# if there's more than one extremal generator outside of C, 
			# this cannot satisify the poset condition.
			return False
		# Removing the extremal generator (should be just one) from hilbert_working
		hilbert_outer.remove(v[0])

		# Assume that the poset condition is satisified at this point, then
		# loop through each vector in the Hilbert basis of D, 
		poset_condition = True
		for vect in hilbert_outer:
			# the poset condition will remain true as long as 
			# each vect in Hilbert basis of D is also
			# contained in the Hilbert basis of D
			poset_condition = poset_condition and (vect in hilbert_inner) 
		
		return poset_condition
			

	def glue(self):
		""" Glue bottom_sequence and top_sequence and store into 
		cone_sequence

		1) Check if sequence_complete flag is true; 
		2) if yes, join the bottom_sequence and top_sequence into cone_sequence
		so that cone_sequence begins with bottom_sequence, then top_sequence in reverse order
		"""
		if self.sequence_complete:
			# get the index of the last element of each sequence.
			top_index = len(self.top_sequence) - 1
			bottom_index = len(self.bottom_sequence) - 1
			# If we run bottom up or top down purely, one of the sequence
			# ends with inner_cone or outer_cone, creating an overlap.
			# if the sequence's ends are the same cone, just pop one WLOG
			if self.bottom_sequence[bottom_index] == self.top_sequence[top_index]:
				self.top_sequence.pop() # Remove one of the repeated cones
 
			# if we end up with some different cones:
			self.cone_sequence = self.bottom_sequence + self.top_sequence.reverse()




if __name__ == "__main__":
	""" Some testing code here """
	for i in range(3):
		# loop through dimension 2 through 5
		dim = i +2
		outer = cone_tools.generate_cone(dim)
		inner = cone_tools.generate_inner_cone(outer)

		trial = ConeSequence(inner,outer)
		print("The inner cone has generators: \n{}".format(trial.inner_cone.rays_list()))
		print("The outer cone has generators: \n{}".format(trial.outer_cone.rays_list()))
		


