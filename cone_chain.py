#!/usr/bin/env sage

"""ConeChian

This module contains the an object that will contain a sequence of cones
and defines ConeChainElement, an object that will contain experimental data for each cone.
"""
import sage.all
import cone_tools
import experiment_io_tools

class ConeChainElement(object):
	""" A data structure to hold a cone and its hilbert basis
	and associated experimental data.
	Class Attribute:
		num_hilbert_calc (int):		Keeps track of the number of times we call
									Hilbert basis calculations.
	Attributes:
		cone (sage.all.Polyhedron): the cone object to be stored
		generation_step (int):		step in the generation process
		algorithm_used (str):		"i" = initial step
									"t" = top down
									"b" = bottom up
		hilbert_basis (list of lists): Hilbert basis of cone
	"""
	num_hilbert_calc = 0

	def __init__(self,cone,generation_step=0, algorithm_used="i", hilbert_basis=None):
		self.cone = cone
		self.generation_step = generation_step
		self.algorithm_used = algorithm_used
		self.hilbert_basis = hilbert_basis

	def get_hilbert_basis(self):
		""" Retreives the hilbert basis, only calculates once. """
		# if the hilbert_basis data is empty, generate it using Normaliz and store it
		if self.hilbert_basis == None:
			self.hilbert_basis = list(self.cone.integral_points_generators()[1])
			ConeChainElement.num_hilbert_calc += 1
		#return the stored value.
		return self.hilbert_basis

	def rays_list(self):
		"""Returns the extremal generators of the cone 
		self.cone.rays_list() (list of lists): normaliz returns this.
		"""
		return self.cone.rays_list()

	def output_details(self):
		""" Prints basic details about this particular cone. """
		print("rays = {}".format(self.rays_list()))
		print("generated on step {} with algorithm {}".format(self.generation_step,self.algorithm_used))
		print("number of elements in hilbert_basis = {}".format(len(self.hilbert_basis)))


class ConeChain(object):
	""" Initializes with two cones (assuming containment)
	
	We wish the represent the data so that a sequence of cones (poset)

		C = C_0 < ... < C_n = D

	can be "grown" from two ends, the tail or the head so that

	bottom_sequence: C = C_0 < C_1 < ... 
	top_sequence: D = D_0 > D_1 > ...
	
	After some steps, we expect C_n and D_k (for some finite n and k) 
		to satisify the poset condition. When this happens, we will glue the two together;
	cone_poset_chain: [C_0, C_1, ..., C_n, D_k, D_(k-1), ..., D_0]
		Note that top_sequence needs to be "glued" backwards for the containment to make sense!

	Attributes:
		outer_cone (sage.all.Polyhedron): A outer cone
		inner_cone (sage.all.Polyhedron): An inner cone
		top_sequence (list of ConeChainElements): Begins with outer_cone
		bottom_sequence (list of ConeChainElements): Begins with inner_cone
		cone_poset_chain (list of ConeChainElements): Begins empty until glue()
			intended to contain the order of the algorithmetically generated poset chain.
		sequence_complete (boolean): flag to see if the sequence is ready for gluing
		valid_poset (boolean): flag to see if the entire chain fits poset condition. 
	"""
	def __init__(self,inner,outer,rmax=10):
		"""Initiate using cones, then initialize data	"""
		self.outer_cone = outer
		self.inner_cone = inner

		# Lists to store poset elements
		self.top_sequence = [ConeChainElement(outer)]
		self.bottom_sequence = [ConeChainElement(inner)]		
		self.cone_poset_chain = []

		# Internal logic flags
		# sequence complete whenever the poset condition is satisified,
		# so default is False.
		self.sequence_complete = False 
		# sequence is considered a poset chain 
		# when verfiication is checked for every consecutive pair of cones.
		self.valid_poset = True 

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
		""" Appends a cone to the top sequence 
		Args:
			somecone (sage.all.Polyhedron): A polyhedral cone
		Returns: none.
		"""
		self.top_sequence.append(ConeChainElement(somecone,self.number_of_steps(),"t"))


	def append_bottom(self, somecone):
		""" Appends a cone to the bottom sequence 
		Args:
			somecone (sage.all.Polyhedron): A polyhedral cone
		Returns: none.
		"""
		self.bottom_sequence.append(ConeChainElement(somecone,self.number_of_steps(),"b"))

	def top_down(self, steps=1):
		""" Top down algorithm
		Args: none
		Returns: True if top_down completes the sequence
				 False if top_down isn't complete. 
		"""
		
		if self.sequence_complete:
			print("Sequence already complete.")
			return True

		# Collect the set of extremal generators of the intermediate cone that is not in C
		extremal_gens_outside_inner_cone = 	cone_tools.extremal_generators_outside_inner_cone(
												self.bottom_sequence[-1].cone, 
												self.top_sequence[-1].cone)
		
		if len(extremal_gens_outside_inner_cone) == 0:
			print("Ended up with the same cone, run self.check_complete()")
			return self.check_complete()
			

		vector_to_remove = cone_tools.shortest_vector(extremal_gens_outside_inner_cone)
		#print("Vector norms: {}".format([r.norm() for r in extremal_gens_outside_inner_cone]))
		#print("Vector to remove = {} and its norm = {}".format(vector_to_remove,vector_to_remove.norm()))

		intermediate_hilb = self.top_sequence[-1].get_hilbert_basis()
		intermediate_hilb[0]
		#print("intermediate_hilb = {}".format(intermediate_hilb))
		#verboseprint("Hilbert Basis of Intermediate Cone: \n {}".format(IntermediateHB))

		intermediate_hilb.remove(vector_to_remove)

		new_generators = intermediate_hilb + self.bottom_sequence[-1].cone.rays_list()
		#print("Forming new cone with: \n{}".format(new_generators))
		#print("Forming cone with {} vectors in Hilbert Basis of D + Extremal Generators of C.".format(len(new_generators)))
		self.append_top(sage.all.Polyhedron(rays=new_generators,backend='normaliz'))
		# minor recursion; if the number of steps is not the default, then repeat by
		# returning its results.
		if steps > 1:
			return self.top_down(steps-1)
		return self.check_complete()

def bottom_up(self,steps=1):
	""" Bottom Up algorithm
	Args: none
	Returns: True if top_down completes the sequence
			 False if top_down isn't complete. 
	"""
		
	if self.sequence_complete:
		print("Sequence already complete.")
		return True

	current_inner = self.bottom_sequence[-1].cone
	current_outer = self.top_sequence[-1].cone

	# find all the extremal generators of outer cone outside of current inner cone
	vlist = cone_tools.extremal_generators_outside_inner_cone(current_inner, current_outer)

	# if the list is empty, we should be done.
	if len(vlist) == 0:
		print("Ended up with the same cone, run self.check_complete()")
		return self.check_complete()
	
	longestv = cone_tools.longest_vector(vlist)
	visible_facets = cone_tools.visible_facets(current_inner, longestv)
	visible_max_lambda_facet = 


	if steps > 1:
		return self.bottom_up(steps-1)
	else:
		return self.check_complete()


	def number_of_steps(self):
		""" Returns the number of steps """
		if self.sequence_complete:
			return len(self.cone_poset_chain) - 2  
		else:
			return len(self.top_sequence) + len(self.bottom_sequence) - 2 


	def verify_validity(self):
		""" Loops through the sequences as appropriate and checks poset conditions
		Note: This is a computationally heavy function, and should not be used frequently
			For optimization, this should be ran once per experiment, instead of for every trial.
		Args: none
		Returns: True - sequence is valid (not necessarily complete)
		"""
		# if the sequence is complete, loop through each consecutive pair
		# and verify the entire sequence is good.
		# break out and return false if even just one of them fail
		# TODO: Need to make this use the index of the cone, and rewrite 
		#		poset_check to operate on the ConeChainElement objects
		#		directly.
		self.valid_poset = True
		if self.sequence_complete:
			# the length of the sequence - 1 because we're looking at consecutive pairs.
			for i in range(self.number_of_steps()-1):
				if not self.poset_check(self.cone_poset_chain[i], self.cone_poset_chain[i+1]):
					self.valid_poset = False
		# otherwise, go through top down and bottom up 
		else:
			if len(self.bottom_sequence) > 1:
				for i in range(len(self.bottom_sequence)-1):
					if not self.poset_check(self.bottom_sequence[i], self.bottom_sequence[i+1]):
						self.valid_poset = False
			if len(self.top_sequence) > 1:
				for i in range(len(self.top_sequence)-1):
					if not self.poset_check(self.top_sequence[-(i+1)], self.top_sequence[-(i+2)]):
						self.valid_poset = False
		return self.valid_poset

	def check_complete(self):
		""" Checks if the sequence is complete 
		1) verify the poset conditions on the last entries of
			top_sequence and bottom_sequence.
		2) if the poset condition is met, glue the bottom_sequence and 
			top_sequence together into cone_poset_chain.
		Args: Nothing
		Returns: Nothing.
		"""
		# debug print("Checking if the last element of top_sequence and bottom_sequence \n satisify the poset condition:")
		
		# sequence is complete if the poset condition is met for the two intermediate cones
		self.sequence_complete = self.poset_check(self.bottom_sequence[-1],
														self.top_sequence[-1])
		# if the sequence is complete, we should glue them together.
		if self.sequence_complete:
			# debug print("Sequence complete!")
			if len(self.cone_poset_chain) == 0:
				self.glue()
			return True
		else:
			return False
		# else:
			# debug print("Sequence incomplete!")
		# debug experiment_io_tools.pause()
		# debug experiment_io_tools.new_screen()
			
	def poset_check(self, inner, outer):
		""" Verifies if the Poset condition is met by inner and outer
		Default behavior for same cone given is to return True.
		We do this by checking the hilbert basis of inner, then outer,
		and verify that:
			1) One or less extremal generator of outer is outside inner, call this v
			2) Hilbert basis of outer take away v should be a subset of
				the Hilbert basis of inner.
		Args: 
			inner (ConeChainElement
		): "inner" cone
			outer (ConeChainElement
		): "outer" cone (assume inner is contained)
		Returns: 
			poset_condition
			poset_condition (Boolean): 	True if C, D satisify the poset condition
											or if they're the same cone;
										False otherwise.
		"""

		# retreive the hilbert basis 
		hilbert_inner = inner.get_hilbert_basis()
		hilbert_outer = outer.get_hilbert_basis()

		
		if hilbert_inner == hilbert_outer:
			return True
		# Finding extremal generator of D not in C
		v = cone_tools.extremal_generators_outside_inner_cone(inner.cone,outer.cone)
		# debug print("hilbert_outer = {}".format(hilbert_outer))
		# debug print("v = {}".format(v))
		if len(v) > 1:
			# if there's more than one extremal generator outside of C, 
			# this cannot satisify the poset condition.
			return False
		# Removing the extremal generator (should be just one) from hilbert_outer
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
		cone_poset_chain

		1) Check if sequence_complete flag is true; 
		2) if yes, join the bottom_sequence and top_sequence into cone_poset_chain
		so that cone_poset_chain begins with bottom_sequence, then top_sequence in reverse order
		"""
		if self.sequence_complete:
			# debug print("Now arranging data.")
			# get the index of the last element of each sequence.
			# If we run bottom up or top down purely, one of the sequence
			# ends with inner_cone or outer_cone, creating an overlap.
			# if the sequence's ends are the same cone, just pop one WLOG
			if self.bottom_sequence[-1].cone == self.top_sequence[-1].cone:
				# debug print("Removing a cone from top_sequence because \n the last elements in the sequences are equal...")
				# experiment_io_tools.pause()
				self.top_sequence.pop() # Remove one of the repeated cones
 
			# if we end up with some different cones:
			self.cone_poset_chain = self.cone_poset_chain + self.bottom_sequence
			self.cone_poset_chain = self.cone_poset_chain + [self.top_sequence[-(i+1)] for i in range(len(self.top_sequence))]
			if len(self.top_sequence) == 0:
				self.top_sequence.append(self.cone_poset_chain[-1])

	def output_to_terminal(self):
		""" Prints essencial information about the sequence """
		experiment_io_tools.new_screen("Printing summary information about the cone chain:")
		print("inner_cone has generators: \n{}".format(self.inner_cone.rays_list()))
		print("outer_cone has generators: \n{}".format(self.outer_cone.rays_list()))
		print("sequence_complete = {}".format(self.sequence_complete))
		print("top_sequence has length {}".format(len(self.top_sequence)))
		print("bottom_sequence has length {}".format(len(self.bottom_sequence)))
		print("cone_poset_chain has length {}".format(len(self.cone_poset_chain)))
		print("we have used Normaliz for hilbert basis calculation {} times.".format(ConeChainElement.num_hilbert_calc))
		experiment_io_tools.pause()
		experiment_io_tools.new_screen()

	def chain_details(self):
		switcher = {
			0: ("bottom_sequence",self.bottom_sequence),
			1: ("top_sequence", self.top_sequence),
			2: ("cone_poset_chain", self.cone_poset_chain)
		}
		for key in range(3):
			experiment_io_tools.new_screen("Printing details of the chain.")
			print(switcher[key][0])
			i = 0
			for tcone in switcher[key][1]:
				print(switcher[key][0]+"[{}]:".format(i))
				tcone.output_details()
				i = i + 1 
				if sage.all.mod(i,5) == 0:
					experiment_io_tools.pause()
			experiment_io_tools.pause()
		self.output_to_terminal()
		experiment_io_tools.new_screen()
	
		
if __name__ == "__main__":
	""" Some testing code here """
	"""
	experiment_io_tools.new_screen()
	for i in range(4):
		# loop through dimension 2 through 5
		dim = i + 2
		outer = cone_tools.generate_cone(dim)
		inner = cone_tools.generate_inner_cone(outer)

		trial = ConeChain(inner,outer)
		trial.output_to_terminal()
	"""

	# known cones in Z^2 for testing.
	outer = sage.all.Polyhedron(rays=[[1,0],[1,3]],backend="normaliz")
	middle = sage.all.Polyhedron(rays=[[1,0],[1,2]],backend="normaliz")
	inner = sage.all.Polyhedron(rays=[[1,0],[1,1]],backend="normaliz")

	print("Running top test (known chain, running topdown):")
	toptest = ConeChain(inner, outer)
	toptest.output_to_terminal()
	print("Appending middle cone to top")
	toptest.top_down()
	toptest.check_complete()
	toptest.output_to_terminal()
	toptest.chain_details()


	for i in range(3):
		experiment_io_tools.new_screen("Generating Cone for dimension {}:".format(i+2))
		test_outer_cone = cone_tools.generate_cone(i+2)
		test_inner_cone = cone_tools.generate_inner_cone(test_outer_cone)

		print("\tOuter cone has generators: \n\t{}".format(test_outer_cone.rays_list()))
		print("\tInner cone has generators: \n\t{}".format(test_inner_cone.rays_list()))

		rand_test = ConeChain(test_inner_cone, test_outer_cone)

		print("Now running top down...")
		rand_test.top_down(50)
		experiment_io_tools.pause()
		rand_test.chain_details()
"""
	# what happens when we give a pair C,D st L(D) = L(C) + v (direct sum)
	# for some v outside of :(D)?
	print("Running short test (input of elementary ascend):")
	experiment_io_tools.pause()
	shorttest = ConeChain(inner, middle)
	shorttest.output_to_terminal()
	shorttest.check_complete()
	shorttest.output_to_terminal()


	# what happens when we append to top?
	print("Running top test (known chain, append to top):")
	toptest = ConeChain(inner, outer)
	print("Next screen should say incomplete")
	experiment_io_tools.pause()
	toptest.check_complete()
	print("Appending middle cone to top")
	toptest.append_top(middle)
	toptest.check_complete()
	toptest.output_to_terminal()
	toptest.chain_details()

	# What happens when we append to bottom ? 
	print("Running bottom test (known chain, append to bottom:")
	bottomtest = ConeChain(inner, outer)
	print("Next screen should say incomplete")
	experiment_io_tools.pause()
	bottomtest.check_complete()
	print("Appending middle cone to bottom")
	bottomtest.append_bottom(middle)
	bottomtest.check_complete()
	bottomtest.output_to_terminal()
	bottomtest.chain_details()
	print("Is bottomtest a valid poset sequence?... {}".format(bottomtest.verify_validity()))

	# What happens when we put in the same cone? 
	# Expecting a cone chain of length 1 at the end.
	sameconetest = ConeChain(inner, inner)
	sameconetest.check_complete()
	experiment_io_tools.pause()
	sameconetest.output_to_terminal()
"""
