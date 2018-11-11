#!/usr/bin/env sage

"""ConeChain

This module contains the an object that will contain a sequence of cones
and defines ConeChainElement, an object that will contain experimental data for each cone.
"""
import sage.all
import cone_tools
import experiment_io_tools
import json 
import sys
from cone_chain_element import ConeChainElement, ConeChainElementEncoder, ConeChainElementDecoder
import pylab as plt
import datetime, os


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
		outer_cone (sage.all.Polyhedron): outer cone
		inner_cone (sage.all.Polyhedron): inner cone, assume outer_cone contains inner_cone
		outer_cone_rays_list (list of lists of integers): Extremal generators of outer cone
		inner_cone_rays_list (list of lists of integers): Extremal generators of inner cone
		top_sequence (list of ConeChainElements): Begins with outer_cone
		bottom_sequence (list of ConeChainElements): Begins with inner_cone
		cone_poset_chain (list of ConeChainElements): Begins empty until glue()
			intended to contain the order of the algorithmetically generated poset chain.
		sequence_complete (boolean): flag to see if the sequence is ready for gluing
		valid_poset (boolean): flag to see if the entire chain fits poset condition. 
	"""
	def __init__(self, inner, outer, 
			top_seq=None, bottom_seq=None,
			poset_chain=None, seq_comp=False, valid = True):
		"""Initiate using cones, then initialize data	"""
		self.outer_cone = outer
		self.inner_cone = inner
		self.outer_cone_rays_list = outer.rays_list()
		self.inner_cone_rays_list = inner.rays_list()
		
		self.dimension = outer.dimension()
		# Lists to store poset elements
		self.top_sequence = [ConeChainElement(outer)] if top_seq is None else top_seq
		self.bottom_sequence = [ConeChainElement(inner)] if bottom_seq is None else bottom_seq
		self.cone_poset_chain = [] if poset_chain is None else poset_chain

		# Internal logic flags
		# sequence complete whenever the poset condition is satisified,
		# so default is False.
		self.sequence_complete = seq_comp 
		# sequence is considered a poset chain 
		# when verfiication is checked for every consecutive pair of cones.
		self.valid_poset = valid 

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
		#intermediate_hilb[0]
		#print("intermediate_hilb = {}".format(intermediate_hilb))
		#verboseprint("Hilbert Basis of Intermediate Cone: \n {}".format(IntermediateHB))

		try:
			intermediate_hilb.remove(vector_to_remove)
		except:
			print("Not sure what happened here but {} is not in intermediate_hilb".format(vector_to_remove))

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
		
		# find the longest of the vectors strictly outside current_inner
		longestv = cone_tools.longest_vector(vlist)

		# collect visible facets WRT longestv
		visible_facets = cone_tools.visible_facets(current_inner, longestv)
		
		# out of those, choose the one with the max lambda
		visible_max_lambda_facet = cone_tools.facets_with_max_lambda(visible_facets, longestv)
		
		# collect all the extremal generators of the facet
		facet_generators =  visible_max_lambda_facet.as_polyhedron().rays_list()

		# form a zonotope (collect the list of vertices of the zonotope) using facet_generators
		preshift_zonotope_gens = cone_tools.zonotope_generators(facet_generators)

		# 1/lambda as discussed in paper. This is the shift factor needed to guarentee the zonotope will
		# contain at least one lattice point.
		shift_factor = 1/ abs(visible_max_lambda_facet.ambient_Hrepresentation(0).eval(sage.all.vector(longestv)))

		# the origin, a point on the zonotope, will be shifted also (so the image is just the shift vector)
		shift_vector = [shift_factor*i for i in longestv]

		# take all the generators, shift them, and then include the shift vector
		shifted_generators = [[gen[i] + shift_vector[i] for i in range(self.dimension)] for gen in preshift_zonotope_gens]
		shifted_generators.append(shift_vector)

		# formally generate the zonotope now
		zono = sage.all.Polyhedron(vertices=shifted_generators,backend='normaliz')
		
		# find the lattice points in the zonotope
		lattice_points_in_zono = list(zono.integral_points())

		# then find the shortest one
		shortest_lattice_point_in_zono = cone_tools.shortest_vector(lattice_points_in_zono)

		self.append_bottom(current_inner.convex_hull(sage.all.Polyhedron(rays=[shortest_lattice_point_in_zono],backend='normaliz')))

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
		# sequence is complete if the poset condition is met for the two intermediate cones
		self.sequence_complete = self.poset_check(self.bottom_sequence[-1],
														self.top_sequence[-1])
		# if the sequence is complete, we should glue them together.
		if self.sequence_complete:
			if len(self.cone_poset_chain) == 0:
				self.glue()
			return True
		else:
			return False
		
	def poset_check(self, inner, outer):
		""" Verifies if the Poset condition is met by inner and outer
		Default behavior for same cone given is to return True.
		We do this by checking the hilbert basis of inner, then outer,
		and verify that:
			1) One or less extremal generator of outer is outside inner, call this v
			2) Hilbert basis of outer take away v should be a subset of
				the Hilbert basis of inner.
		Args: 
			inner (ConeChainElement): "inner" cone
			outer (ConeChainElement): "outer" cone (assume inner is contained)
		Returns: 
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

		if len(v) > 1:
			# if there's more than one extremal generator outside of C, 
			# this cannot satisify the poset condition.
			return False
		# Removing the extremal generator (should be just one) from hilbert_outer
		#print("DEBUG: v[0] = {}".format(v[0]))
		if len(v) == 1:
			try:
				hilbert_outer.remove(v[0])
			except:
				print("Failed trying to remove \n\t{} from \n{}".format(v[0],hilbert_outer))

		# Assume that the poset condition is satisified at this point, then
		# loop through each vector in the Hilbert basis of D, 
			poset_condition = True
			for vect in hilbert_outer:
				# the poset condition will remain true as long as 
				# each vect in Hilbert basis of D is also
				# contained in the Hilbert basis of D
				poset_condition = poset_condition and (vect in hilbert_inner) 
			
			return poset_condition
		if len(v) == 0:
			return True

	def glue(self):
		""" Glue bottom_sequence and top_sequence and store into 
		cone_poset_chain

		1) Check if sequence_complete flag is true; 
		2) if yes, join the bottom_sequence and top_sequence into cone_poset_chain
		so that cone_poset_chain begins with bottom_sequence, then top_sequence in reverse order
		"""
		if self.sequence_complete:
			# get the index of the last element of each sequence.
			# If we run bottom up or top down purely, one of the sequence
			# ends with inner_cone or outer_cone, creating an overlap.
			# if the sequence's ends are the same cone, just pop one WLOG
			temp_seq = [i for i in self.top_sequence]
				
			if self.bottom_sequence[-1].cone == self.top_sequence[-1].cone:
				temp_seq.pop() # Remove one of the repeated cones
 
			# if we end up with some different cones:
			self.cone_poset_chain = [] + self.bottom_sequence
			self.cone_poset_chain = self.cone_poset_chain + [temp_seq[-(i+1)] for i in range(len(temp_seq))]
			
	def output_to_terminal(self):
		""" Prints essencial information about the sequence
			Args: None
			Returns: None 
		"""
		experiment_io_tools.new_screen("Printing summary information about the cone chain:")
		print("inner_cone has generators: \n{}\n".format(self.inner_cone.rays_list()))
		print("outer_cone has generators: \n{}\n".format(self.outer_cone.rays_list()))
		print("\tsequence_complete = {}\n".format(self.sequence_complete))
		print("\ttop_sequence has length {}\n".format(len(self.top_sequence)))
		print("\tbottom_sequence has length {}\n".format(len(self.bottom_sequence)))
		print("\tcone_poset_chain has length {}\n".format(len(self.cone_poset_chain)))
		#print("we have used Normaliz for hilbert basis calculation {} times.".format(ConeChainElement.num_hilbert_calc))
		experiment_io_tools.pause()
		experiment_io_tools.new_screen()

	
		

	def chain_details(self):
		""" Prints the details for each cone in the chain 
			Args: None
			Returns: None
		"""
		if self.sequence_complete:
			experiment_io_tools.new_screen("Printing details of the (complete) chain.")
			# only need to use case 2,
			# go through each cone in the cone_poset_chain:
			i = 0
			for tcone in self.cone_poset_chain:
				print("cone_poset_chain"+"[{}]:".format(i))
				tcone.output_details()
				i = i + 1 
				# pause every fifth cone
				if sage.all.mod(i,5) == 0:
					experiment_io_tools.pause()

		else:
			# do the same as above but with bottom_sequence
			# and top sequence instead.
			switcher = {
				0: ("bottom_sequence",self.bottom_sequence),
				1: ("top_sequence", self.top_sequence),
			}
			for key in range(2):
				experiment_io_tools.new_screen("Printing details of the (incomplete) chain.")
				print(switcher[key][0])
				i = 0
				for tcone in switcher[key][1]:
					print(switcher[key][0]+"[{}]:".format(i))
					tcone.output_details()
					i = i + 1 
					if sage.all.mod(i,5) == 0:
						experiment_io_tools.pause()
				experiment_io_tools.pause()
		# now print a summary
		self.output_to_terminal()
		experiment_io_tools.new_screen()

	def generate_hilbert_graphs(self, folder=None, experiment_name=None):
		directory = "DATA/{}d/Hilbert Graphs of Unnamed Experiments/".format(self.dimension) if folder is None else folder
		filename = str(datetime.datetime.now()) if experiment_name is None else experiment_name
		try:
			os.makedirs(directory, 0755) 
		except:
			NotImplemented



		switcher = {"top_sequence" : self.top_sequence,
					"bottom_sequence" : self.bottom_sequence,
					"cone_poset_chain" : self.cone_poset_chain}

		i = 0
		for name in switcher:
			if len(switcher[name]) > 1:
				length_filename = name + " LENGTH {} steps.png".format(self.number_of_steps())
				length_filename_no_step = name + " LENGTH.png"
				hilbert_graph_data_length = [cone.hilbert_graph_data_length() for cone in switcher[name]]
				plt.figure(i)
				
				plt.plot(hilbert_graph_data_length)
				plt.xlabel("Number of Steps: {}".format(name))
				plt.ylabel("Vector Norm")
				plt.title("Length of the longest element in the Hilbert Basis: {}".format(name))
				plt.savefig(directory + length_filename)
				plt.savefig(directory + length_filename_no_step)
				plt.close(i)

				size_filename = name + " SIZE {} steps.png".format(self.number_of_steps())
				size_filename_nostep = name + " SIZE.png"
				hilbert_graph_data_size = [cone.hilbert_graph_data_size() for cone in switcher[name]]
				plt.figure(i+1)
				plt.xlabel("Number of Steps: {}".format(name))
				plt.ylabel("Number of Vectors")
				plt.title("Size of the Hilbert Basis: {}".format(name))
				plt.plot(hilbert_graph_data_size)
				plt.savefig(directory + size_filename)
				plt.savefig(directory + size_filename_nostep)
				plt.close(i+1)
			i += 2
	def recalc(self):
		print("\t\tRecalculating Hilbert basis for top_sequence...")
		for cone in self.top_sequence:
			cone.get_hilbert_basis(forced=True)

		print("\t\tRecalculating Hilbert basis for bottom_sequence...")
		for cone in self.bottom_sequence:
			cone.get_hilbert_basis(forced=True)


		print("\t\tRecalculating Hilbert basis for cone_poset_chain...")
		for cone in self.cone_poset_chain:
			cone.get_hilbert_basis(forced=True)

		

class ConeChainEncoder(json.JSONEncoder):
	def default(self,obj):
		if isinstance(obj, ConeChain):
			outer_cone_rays_list_json = cone_tools.rays_list_to_json_array(obj.outer_cone_rays_list)
			inner_cone_rays_list_json = cone_tools.rays_list_to_json_array(obj.inner_cone_rays_list)
			top_seq = [json.dumps(cone_element,cls=ConeChainElementEncoder) for cone_element in obj.top_sequence]
			bottom_seq = [json.dumps(cone_element,cls=ConeChainElementEncoder) for cone_element in obj.bottom_sequence]
			poset_chain = [json.dumps(cone_element,cls=ConeChainElementEncoder) for cone_element in obj.cone_poset_chain]
			
			return {'outer_cone_rays_list' : outer_cone_rays_list_json,
				'inner_cone_rays_list' : inner_cone_rays_list_json,
				'dimension' : obj.dimension,
				'top_sequence': top_seq,
				'bottom_sequence': bottom_seq,
				'cone_poset_chain': poset_chain,
				'sequence_complete': obj.sequence_complete,
				'valid_poset': obj.valid_poset}
		return json.JSONEncoder.default(self, obj)

class ConeChainDecoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
	def object_hook(self, dictionary):
		if 'outer_cone_rays_list' in dictionary:
			outer = sage.all.Polyhedron(rays=dictionary['outer_cone_rays_list'],backend='normaliz')
		if 'inner_cone_rays_list' in dictionary:
			inner = sage.all.Polyhedron(rays=dictionary['inner_cone_rays_list'],backend='normaliz')
		top_seq = [json.loads(cone_element,cls=ConeChainElementDecoder) for cone_element in dictionary['top_sequence']]
		bottom_seq = [json.loads(cone_element,cls=ConeChainElementDecoder) for cone_element in dictionary['bottom_sequence']]
		poset_chain = [json.loads(cone_element,cls=ConeChainElementDecoder) for cone_element in dictionary['cone_poset_chain']]
		return ConeChain(inner, outer, top_seq, bottom_seq, poset_chain, dictionary['sequence_complete'], dictionary['valid_poset'])



class ConeChainInitialConditionExtractor(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
	def object_hook(self, dictionary):
		if 'outer_cone_rays_list' in dictionary:
			outer = sage.all.Polyhedron(rays=dictionary['outer_cone_rays_list'],backend='normaliz')
		if 'inner_cone_rays_list' in dictionary:
			inner = sage.all.Polyhedron(rays=dictionary['inner_cone_rays_list'],backend='normaliz')
		return ConeChain(inner, outer)



		
if __name__ == "__main__":

	""" Some testing code here """

	steps = 50
	
	bound = 100

	valid_dimension = False
	while not valid_dimension:
		dim = experiment_io_tools.ask_int("Dimension: ")
		if dim > 1:
			valid_dimension = True

	accept_name = False
	while not accept_name:
		experiment_name = str(raw_input("Experiment Name: "))
		accept_name = experiment_io_tools.query_yes_no("\tYou entered '{}'. Accept?".format(experiment_name))

	directory = "DATA/{}d/".format(dim)  + experiment_name + "/"
	try:
		os.makedirs(directory, 0755) 
	except:
		NotImplemented

	raw_data_file_path = directory + experiment_name + ".json"

	print("Loading file: {}".format(raw_data_file_path))

	
	
	toptest = None 
	try:
		with open(raw_data_file_path, 'r') as fp:
			toptest = json.load(fp, cls=ConeChainDecoder)
		print('\tloading successful...')
	except:
		print('\tA file loading error has occured, generating new cones.')
		test_outer_cone = cone_tools.generate_cone(dim,bound)
		test_inner_cone = cone_tools.generate_inner_cone(test_outer_cone,bound)
		toptest = ConeChain(test_inner_cone, test_outer_cone)
		with open(directory + experiment_name + " initial conditions.json", 'w') as fp:
			json.dump(toptest, fp, cls=ConeChainEncoder,sort_keys=True,
				indent=4, separators=(',', ': '))
		
	experiment_io_tools.pause()


	
	 


	print('Graphing current data')
	toptest.generate_hilbert_graphs(directory, experiment_name)
	toptest.output_to_terminal()
	#toptest.save_summary(directory, experiment_name)
	user_continue = experiment_io_tools.query_yes_no("Begin more testing?")


	original_count = toptest.number_of_steps()
	while user_continue:
		print('\trunning top down for {} steps...'.format(steps))
		toptest.top_down(steps)
		print('Printing graph...')
		toptest.generate_hilbert_graphs(directory, experiment_name)
		#print("Saving summary...")
		#toptest.save_summary(directory, experiment_name)
		print('Saving to file...')

		with open(raw_data_file_path, 'w') as fp:
			json.dump(toptest, fp, cls=ConeChainEncoder,sort_keys=True,
				indent=4, separators=(',', ': '))
		
		user_continue = experiment_io_tools.query_yes_no("Completed {} steps this run so far.\n\tSaved data and printed graph. Continue?".format(toptest.number_of_steps()-original_count))
 	


"""
	experiment_io_tools.new_screen()
	for i in range(4):
		# loop through dimension 2 through 5
		dim = i + 2
		outer = cone_tools.generate_cone(dim)
		inner = cone_tools.generate_inner_cone(outer)

		trial = ConeChain(inner,outer)
		trial.output_to_terminal()


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
	steps = 50
	i=0
	#for i in range(2):
	experiment_io_tools.new_screen("Generating Cone for dimension {}:".format(i+2))
	test_outer_cone = cone_tools.generate_cone(i+2)
	test_inner_cone = cone_tools.generate_inner_cone(test_outer_cone)

	print("\tOuter cone has generators: \n\t{}".format(test_outer_cone.rays_list()))
	print("\tInner cone has generators: \n\t{}".format(test_inner_cone.rays_list()))

	top_down_rand_test = ConeChain(test_inner_cone, test_outer_cone)

	print("Now running {} steps of top_down algorithm...".format(steps))
	top_down_rand_test.top_down(steps)
	experiment_io_tools.pause()
	top_down_rand_test.chain_details()

	
	#for i in range(2):
	experiment_io_tools.new_screen("Generating Cone for dimension {}:".format(i+2))
	test_outer_cone = cone_tools.generate_cone(i+2)
	test_inner_cone = cone_tools.generate_inner_cone(test_outer_cone)

	print("\tOuter cone has generators: \n\t{}".format(test_outer_cone.rays_list()))
	print("\tInner cone has generators: \n\t{}".format(test_inner_cone.rays_list()))

	bottom_up_rand_test = ConeChain(test_inner_cone, test_outer_cone)

	print("Now running {} steps of bottom_up algorithm...".format(steps))
	bottom_up_rand_test.bottom_up(steps)
	experiment_io_tools.pause()
	bottom_up_rand_test.chain_details()


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
