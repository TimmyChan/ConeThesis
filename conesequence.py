"""ConeSequence

This module contains the an object that will contain a sequence of cones.
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
		bottom_sequence (list of SAGE.geometry.Polyhedron): Begins with inner_cone
		cone_sequence (list of SAGE.geometry.Polyhedron): Begins empty until glue()
	"""
	def __init__(self,inner,outer,rmax=10):
		"""Initiate using cones, then initialize data	"""
		self.outer_cone = outer
		self.inner_cone = inner
		self.top_sequence = [outer]
		self.bottom_sequence = [inner]
		self.sequence_complete = False
		self.cone_sequence = []


	def append_top(self, somecone):
		""" Appends a cone to the top sequence """
		self.top_sequence.append(somecone)

	def append_bottom(self, somecone):
		""" Appends a cone to the bottom sequence """
		self.bottom_sequence.append(somecone)

	def number_of_steps_completed(self):
		""" Returns the number of steps """
		if self.sequence_complete:
			return len(self.cone_sequence) - 2  
		else:
			return len(self.top_sequence) + len(self.bottom_sequence) - 2 # return the 

	def check_complete(self):
		""" Checks if the sequence is complete 
		1) verify the poset conditions on the last entries of
			top_sequence and bottom_sequence.
		2) if the poset condition is met, glue the bottom_sequence and 
			top_sequence together into cone_sequence.
		Args: Nothing
		Returns: Nothing.
		"""
		# get the index of the last element of each sequence.
		top_index = len(self.top_sequence) - 1
		bottom_index = len(self.bottom_sequence) - 1
		# sequence is complete if the poset condition is met for the two intermediate cones
		self.sequence_complete = poset_condition_verification(self.bottom_sequence[bottom_index],
										self.top_sequence[top_index])
		# if the sequence is complete, we should glue them together.
		if self.sequence_complete:
			self.glue()
			
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
		print("The inner cone has generators: \n{}".format(trial.inner_cone_rays()))
		print("The outer cone has generators: \n{}".format(trial.outer_cone_rays()))



