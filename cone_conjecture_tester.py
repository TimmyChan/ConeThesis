#!/usr/bin/env sage
""" Wrapper of the experiment, contains all interface stuff
"""
#!/usr/bin/env sage

"""ConeConjectureTester

This module contains the an object that will contain a sequence of cones
and defines ConeChainElement, an object that will contain experimental data for each cone.

"""

import sage.all
import json 
import sys
from cone_chain_element import ConeChainElement, ConeChainElementEncoder, ConeChainElementDecoder
import pylab as plt
import datetime, os

import experiment_io_tools
import cone_tools
import cone_chain


class ConeConjectureTester(object):
	"""All user interface with the Experiment object goes here.
	Class Attributes:
		text_* (string): menu strings used for every experiment's Terminal UI
		main_menu_dict_* (dict): dictionaries where the key is the choice and the value is the menu texts.

	UI Attributes:
		batch_mode (boolean): flag to denote if batch mode is happening
		loaded (boolean): flag to denote if the object contains an active experiment.
		
	"""
	text_main_title = "Cone Conjecture Tester v1.0"

	text_create = "Create new experiment"
	text_load_continue = "Load and continue existing experiment"
	text_load_copy = "Load and copy existing experiment to new file"
	text_load_initial = "Load only initial values of previous experiment"
	text_manual_input = "Create new experiment (manual_input)"
	text_save_exit = "Save and exit"

	text_summary = "Display summary of current experiment"
	text_run_experiment = "Run current experiment with current settings"
	text_print_graphs = "Generate and save graphical data."
	text_display_all_details = "Display all details"


	main_menu_dict_initial = {1: text_create,
							2: text_load_continue,
							3: text_load_copy,
							4: text_load_initial,
							8: text_manual_input,
							1337: text_save_exit}

	main_menu_dict_loaded =  { 	0: text_run_experiment,
								1: text_create,
								2: text_load_continue,
								3: text_load_copy,
								4: text_load_initial,
								5: text_summary,
								6: text_print_graphs,
								7: text_display_all_details,
								8: text_manual_input,
								1337: text_save_exit}


	# names of the algorithms
	text_top_down = "Top Down"
	text_bottom_up = "Bottom Up"
	text_alternating = "Alternating"

	# not zero
	run_mode_dict = {	1: text_top_down,
						2: text_bottom_up,
						3: text_alternating}

	def __init__(self, dim=None, expr_name=None, some_cone_chain=None, runmode=None, batchmode=False, directory=None, numgen=None, steps=None, rmax=2):
	'''
	Attributes: 
		dimension (int): dimension of the experiment, expecting dim >= 2
		experiment_name (string): the name of the experiment 
		directory (string): the directory the experiment will be contained
		raw_data_path (string): the path to the .JSON file that contains all raw data
		bound (int): the bound on the absolute value of the coordinates of the randomly generated vectors
		run_mode (int): 1 = Top Down, 2 = Bottom Up, 3 = Alternating
		steps (int): Steps to run before saving and prompting to continue again.
		alternation_constant (int): number of steps to run each algorithm before switching.
		current_cone_chain (ConeChain): object to contain the mathematical data
		num_gen (int): number of extremal generators used for the randomly generated cones.
	'''
		self.dimension = dim  #dimension
		self.experiment_name = expr_name #experiment name
		self.directory = directory # default will be DATA/{}d/expr_name/
		self.raw_data_path = None #default will be DATA/{}D/expr_name/expr_name.json

	
		self.bound = rmax # maximum value a coordinate will have


		self.run_mode = 0 if runmode is None else runmode # see run_mode_dict for options

		self.steps = 200 if steps is None else steps
		self.alternation_constant = 1 # number of steps of top down and bottom up to run as you alternate


		self.current_cone_chain = some_cone_chain
		self.batch_mode = batchmode 

		self.num_gen = numgen

		self.loaded = False if self.current_cone_chain is None else True
		if not batchmode:
			self.steps = 100 if steps is None else steps # default number of steps to run between printouts
			self.begin()		

	def begin(self):
		running = True
		while running:
			main_menu_choice = self.main_menu()			
			"""{ 	0: text_run_experiment,
					1: text_create,
					2: text_load_continue,
					3: text_load_copy,
					4: text_load_initial,
					5: text_summary,
					9: text_save_exit}"""
			#0
			if ConeConjectureTester.main_menu_dict_loaded[main_menu_choice] == ConeConjectureTester.text_run_experiment:
				# run a loaded experiment
				self.run_mode = self.run_mode_menu()
				self.run_experiment()	

			#1
			elif ConeConjectureTester.main_menu_dict_loaded[main_menu_choice] == ConeConjectureTester.text_create:
				# make a new experiment
				self.create_experiment()			

			#2
			elif ConeConjectureTester.main_menu_dict_loaded[main_menu_choice] == ConeConjectureTester.text_load_continue:
				# load an old experiment
				self.load_experiment()

			#3
			elif ConeConjectureTester.main_menu_dict_loaded[main_menu_choice] == ConeConjectureTester.text_load_copy:
				# load an old experiment
				self.load_experiment()
				#ask for new naem
				self.ask_experiment_name()
				#update all paths
				self.update_paths()
				# save data to new spot
				self.save_file()

			#4
			elif ConeConjectureTester.main_menu_dict_loaded[main_menu_choice] == ConeConjectureTester.text_load_initial:
				# load an old experiment
				self.load_experiment(initial_condition=True)

			#5
			elif ConeConjectureTester.main_menu_dict_loaded[main_menu_choice] == ConeConjectureTester.text_summary:
				# load an old experiment
				self.current_cone_chain.output_to_terminal()
				self.save_summary()

			#6
			elif ConeConjectureTester.main_menu_dict_loaded[main_menu_choice] == ConeConjectureTester.text_print_graphs:
				# print the graphs
				self.print_graphs()
					
			
			#7: 
			elif ConeConjectureTester.main_menu_dict_loaded[main_menu_choice] == ConeConjectureTester.text_display_all_details:
				self.current_cone_chain.output_to_terminal()
				self.current_cone_chain.chain_details()

			#8:
			elif ConeConjectureTester.main_menu_dict_loaded[main_menu_choice] == ConeConjectureTester.text_manual_input:
				self.manual_create_experiment()


								
			#1337
			elif ConeConjectureTester.main_menu_dict_loaded[main_menu_choice] == ConeConjectureTester.text_save_exit:
				# exit
				self.check_loaded()
				if self.loaded:
					self.current_cone_chain.output_to_terminal()
					print('Printing graphs...')
					self.current_cone_chain.generate_hilbert_graphs(self.directory, self.experiment_name)
					print("Saving summary...")
					self.save_summary()
					print('Saving to file...')
					self.save_file()
		
				running = False


	def print_graphs(self):
		'''	Generates and saves graphs to the appropriate directory.'''
		print('Printing graphs to {}'.format(self.directory))
		self.current_cone_chain.generate_hilbert_graphs(self.directory, self.experiment_name)
		#experiment_io_tools.pause()

	def main_menu(self):
		""" (Terminal UI) Main menu"""
		if self.loaded:
			return experiment_io_tools.menu(ConeConjectureTester.main_menu_dict_loaded,
											ConeConjectureTester.text_main_title,
											self.file_setting_string()+experiment_io_tools.separator())
		else:
			return experiment_io_tools.menu(ConeConjectureTester.main_menu_dict_initial,
											ConeConjectureTester.text_main_title)


	def run_mode_menu(self):
		""" (Terminal UI) Asks user for the mode they want to run."""
		self.check_loaded()
		if self.loaded:
			return experiment_io_tools.menu(ConeConjectureTester.run_mode_dict,
											"Choose Run Mode for '{}'".format(self.experiment_name))
		else:
			return 0

	def deduce_run_mode(self):
		""" (Internal logic function) Determines what mode a loaded experiment has even 
			if runmode was not saved. """
		self.check_loaded()
		if self.loaded:
			if self.batch_mode:
				top_down_count = len(self.current_cone_chain.top_sequence)
				bottom_up_count = len(self.current_cone_chain.bottom_sequence)
				if top_down_count > bottom_up_count and bottom_up_count == 1:
					self.run_mode=1 # topdown
					return
				elif top_down_count < bottom_up_count and top_down_count ==1:
					self.run_mode = 2 # bottomup
					return
				elif top_down_count >= bottom_up_count -1 and top_down_count <= bottom_up_count + 1:
					self.run_mode = 3
					return
			self.run_mode = self.run_mode_menu()
		else:
			return 0

	def file_setting_string(self):
		""" returns a string that shows settings """
		settings = "Current Settings: \n\tDimension = {}\n".format(self.dimension)
		settings += "\tExperiment Name = {}\n".format(self.experiment_name)
		settings += "\tRaw Data path = {}\n".format(self.raw_data_path)
		return settings


	def generate_cones(self):
		""" Takes input from user either by script or by the UI and generates cones """
		if self.bound is None or not self.batch_mode:
			self.ask_bound()
		if self.num_gen is None or not self.batch_mode:
			self.ask_num_gen()
		print("Generating New Cones...")
		cones_unacceptable = True
		while cones_unacceptable:
			outer_cone = cone_tools.generate_cone(self.dimension, rmax=self.bound, numgen=self.num_gen)
			inner_cone = cone_tools.generate_inner_cone(outer_cone, rmax=self.bound, numgen=self.num_gen)
			cones_unacceptable = (inner_cone.rays_list() == outer_cone.rays_list())
		self.current_cone_chain = cone_chain.ConeChain(inner_cone, outer_cone)
		print("Geneation successful!")
				 
	def create_experiment(self):
		"""Asks the relevant information then checks to see if randomly generated 
		or user inputted"""
		experiment_io_tools.new_screen(ConeConjectureTester.text_create)
		self.ask_dimension()
		self.ask_experiment_name()
		self.update_paths(self.experiment_name)
		
		self.generate_cones()
		
		self.save_file("Initial Conditions")
		self.save_file()
		self.check_loaded()

		experiment_io_tools.pause()



	def manual_create_experiment(self):
		""" PUre UI version of creating experiment, user manually inputs everything """
		experiment_io_tools.new_screen(ConeConjectureTester.text_manual_input)
		self.ask_dimension()
		self.ask_experiment_name()
		self.update_paths(self.experiment_name)
		self.manual_input()
		
		self.save_file("Initial Conditions")
		self.save_file()
		self.check_loaded()

		experiment_io_tools.pause()


	def batch_create_experiment(self,experiment_name=None):
		"""Creates experiment without running it. Does not involve TUI unless there are errors."""
		if experiment_name==None:
			self.update_paths(self.experiment_name)
		else:
			self.update_paths(experiment_name)
		
		if self.bound is None:
			self.ask_bound()
		if self.num_gen is None:
			self.ask_num_gen()

		self.check_loaded()
		if not self.loaded:
			self.generate_cones()	 
		
		self.save_file("Initial Conditions")
		self.save_file()



	def load_experiment(self,initial_condition=False):
		""" Terminal UI for loading a experiment. """
		if self.batch_mode is False:
			experiment_io_tools.new_screen(ConeConjectureTester.text_load_continue)

		user_choice = -1337 
		accept_expr_choice = False
		while (not accept_expr_choice) and (self.batch_mode is False):
			self.ask_dimension()
			try:
				# get the list of experiments and sort it
				possible_experiment_names = os.listdir("DATA/{}d/".format(self.dimension))
				possible_experiment_names.sort()
				# Ask user by making a menu...
				choose_experiment_menu = {i+1: possible_experiment_names[i] for i in range(len(possible_experiment_names)) }
				choose_experiment_menu.update({-1:"... back to main menu..."})
				user_choice = experiment_io_tools.menu(choose_experiment_menu)
				if user_choice <> -1:
					self.experiment_name = choose_experiment_menu[user_choice]
					accept_expr_choice = experiment_io_tools.query_yes_no("Your choice is '{}'. \n\tAccept?".format(self.experiment_name))
				else:
					return
			except:
				experiment_io_tools.pause("Problem finding or opening folder, likely non-existent path.")

		if user_choice <> -1:
			self.update_paths(self.experiment_name)
			self.load_file(initial_condition)
			self.check_loaded()
			experiment_io_tools.pause()
			self.current_cone_chain.output_to_terminal()


	def load_file(self,initial_condition=False,custom_name=None):
		""" Loads a json file into the current_cone_chain 
			Args:
				initial_condition (boolean): 	True if seeking only the initial cones
												False if seeking the whole file (Default)
				custom_name (string):	Sets the name of the experiment to be loaded
		"""

		# if no custom name, then simply load with current settings (TUI version)
		# if there is a custom name, update paths to the appropriate experiment name then attempt to load.

		self.update_paths()
		if custom_name is None:
			filepath = self.raw_data_path
		else:
			filepath = "DATA/{}d/{}/{}.json".format(self.dimension, custom_name,custom_name)

		print("Loading file: {}".format(filepath))
		try:
			with open(filepath, 'r') as fp:
				if initial_condition:
					self.current_cone_chain = json.load(fp, cls=cone_chain.ConeChainInitialConditionExtractor)
					if not self.batch_mode or self.experiment_name is None:
						self.ask_experiment_name()
					self.update_paths()
					
				else:
					self.current_cone_chain = json.load(fp, cls=cone_chain.ConeChainDecoder)
			print('\tloading successful...')
		except:
			print('\tA file loading error has occured.')
		self.save_file()

	def save_file(self, filename=None):
		'''Saves the data from the current cone chain to a file in self.directory
			Args: filename (string): The name of the file with no extensions.
		'''

		self.update_paths()		
		if filename is None:
			file_path = self.raw_data_path
		else:
			file_path = self.directory + filename +".json"

		with open(file_path, 'w') as fp:
			json.dump(self.current_cone_chain, fp, cls=cone_chain.ConeChainEncoder,sort_keys=True,
				indent=4, separators=(',', ': '))
	
	def check_loaded(self):
		''' Verifies that current_cone_chain is loaded by verifying it's not "none '''
		if self.current_cone_chain is None:
			self.loaded = False
		else:
			self.loaded = True


	def update_paths(self, new_expr_name=None):
		''' A function to update self.directory and self.raw_datapath
			Args: new_expr_name (string): The name of the experiment we wish to save/load from	
		'''
		
		# logic to determine the file name in a clear way:
		# if the experiment_name is not set and there's no custom name provided:
		if new_expr_name is None and self.experiment_name is None:
			self.ask_experiment_name()
		elif new_expr_name is not None:
			self.experiment_name = new_expr_name

		# usually set, but just in case...
		if self.dimension is None:
			self.ask_dimension()

		#set the directory and raw data path to be new
		self.directory = "DATA/{}d/".format(self.dimension) + self.experiment_name + "/"
		self.raw_data_path = self.directory + self.experiment_name + ".json"

		#make the directory if it doesn't exist
		try:
			os.makedirs(self.directory, 0755) 
		except:
			NotImplemented
			#print("Error making directory {}".format(self.directory))
		#print("DEBUG: raw_data_path = {}".format(self.raw_data_path))
				
	def save_summary(self,folder=None,experiment_name=None):
		""" Writes current summary of data to a text file.""" 
		summary_name = "Data Summary.txt"
		try:
			os.makedirs(self.directory, 0755) 
		except:
			NotImplemented
		fileobj = open(self.directory + summary_name , "w")
		fileobj.write("inner_cone has generators: \n{}\n".format(self.current_cone_chain.inner_cone.rays_list()))
		fileobj.write("outer_cone has generators: \n{}\n".format(self.current_cone_chain.outer_cone.rays_list()))
		fileobj.write("\tsequence_complete = {}\n".format(self.current_cone_chain.sequence_complete))
		fileobj.write("\ttop_sequence has length {}\n".format(len(self.current_cone_chain.top_sequence)))
		fileobj.write("\tbottom_sequence has length {}\n".format(len(self.current_cone_chain.bottom_sequence)))
		fileobj.write("\tcone_poset_chain has length {}\n".format(len(self.current_cone_chain.cone_poset_chain)))
		fileobj.close()

	def ask_experiment_name(self):
		""" (Terminal UI) Asks user for the experiment name and sets self.experiment_name"""
		if self.experiment_name is not None:
			accept_name = not experiment_io_tools.query_yes_no("Current experiment name set to be {}. Change current setting? ".format(self.experiment_name))
		else:
			accept_name = False
		while not accept_name:
			self.experiment_name = str(raw_input("Experiment Name: "))
			accept_name = experiment_io_tools.query_yes_no("\tYou entered '{}'. Accept?".format(self.experiment_name))


	def ask_dimension(self):
		""" (Terminal UI) Asks user for the dimension and sets self.dimension"""
		if self.dimension <> None:
			valid_dimension = experiment_io_tools.query_yes_no("Current dimension set to be {}. Keep current setting? ".format(self.dimension))
		else:
			valid_dimension = False

		while not valid_dimension:
			self.dimension = experiment_io_tools.ask_int("Enter dimension: ")
			if self.dimension > 1:
				valid_dimension = True

	def ask_bound(self):
		""" (Terminal UI) Asks user for the bound of the random number generator and sets self.bound"""
		if self.bound > 0:
			accept_bound = experiment_io_tools.query_yes_no("Current random numbers bound at +/-{}. Keep current setting? ".format(self.bound))
		else:
			accept_bound = False

		while not accept_bound:
			self.bound = experiment_io_tools.ask_int("Enter the absolute bound for coordinates in these vectors: ")
			if self.bound > 0:
				accept_bound = True

	def ask_num_gen(self):
		""" (Terminal UI) Asks user for the number of generators needed"""
		if self.num_gen is not None:
			accept_num = experiment_io_tools.query_yes_no("Current number of generators = {}. Keep settings?".format(self.num_gen))
		else:
			accept_num = False

		while not accept_num:
			self.num_gen = experiment_io_tools.ask_int("Enter the number of generators for each cone: ")
			if self.num_gen >= self.dimension:
				accept_num = True
			else:
				print("Please input a number greater or equal to the dimension chosen for a full dimensional cone.")



	def ask_steps(self):
		""" (Terminal UI) Asks user for the number of times to run the algorithms between saving and sets self.steps"""
		if self.steps > 0:
			accept_steps = experiment_io_tools.query_yes_no("Currently '{}' is set to run for [{}] steps. Keep current setting? ".format(ConeConjectureTester.run_mode_dict[self.run_mode],self.steps))
		else:
			accept_steps = False

		while not accept_steps:
			self.steps = experiment_io_tools.ask_int("Enter the number of steps to run {}: ".format(ConeConjectureTester.run_mode_dict[self.run_mode]))
			if self.steps > 0:
				accept_steps = True

	def ask_alternation_constant(self):
		""" (Terminal UI) Asks user for the number of times to run top_down/bottom_up before alternating
			CURRENTLY NOT USED... DEFAULT SET TO 1.
		"""
		
		if self.steps > 0:
			accept_alternation_constant = experiment_io_tools.query_yes_no("'{}' is currently set to switch every {} step(s). Keep current setting? ".format(ConeConjectureTester.run_mode_dict[self.run_mode],self.alternation_constant,self.steps))
		else:
			accept_alternation_constant = False

		while not accept_alternation_constant:
			self.alternation_constant = experiment_io_tools.ask_int("Enter the alternating constant: ".format(ConeConjectureTester.run_mode_dict[self.run_mode]))
			if self.stalternation_constanteps > 0:
				accept_alternation_constant = True


	def run_experiment(self):
		""" Runs the experiment using current settings 
			Assumes:
			1) current_cone_chain is not empty
			2) If you're in batch mode, self.run_mode() is set.
		"""
		# ask run_mode (1 - Top Down, 2 - Bottom up, 3 - Alternating?)
		if self.run_mode is None or self.run_mode == 0 or self.run_mode not in ConeConjectureTester.run_mode_dict.keys():
			self.deduce_run_mode()


		# verify number of steps to run between printing/saving data
		if self.batch_mode is False:
			self.ask_steps()
			experiment_io_tools.new_screen(self.experiment_name)
			user_continue = experiment_io_tools.query_yes_no("Begin running '{}'?".format(ConeConjectureTester.run_mode_dict[self.run_mode]))
		else:
			user_continue = True

		# Beginning running experiment
		original_count = self.current_cone_chain.number_of_steps()
		while user_continue:
			print("\trunning '{}' for {} steps...".format(ConeConjectureTester.run_mode_dict[self.run_mode],self.steps))
			steps_ran_this_sitting = self.current_cone_chain.number_of_steps()-original_count
			if ConeConjectureTester.run_mode_dict[self.run_mode] == ConeConjectureTester.text_top_down:
				self.current_cone_chain.top_down(self.steps)
			
			elif ConeConjectureTester.run_mode_dict[self.run_mode] == ConeConjectureTester.text_bottom_up:
				self.current_cone_chain.bottom_up(self.steps)

			elif ConeConjectureTester.run_mode_dict[self.run_mode] == ConeConjectureTester.text_alternating:
				for step_counter in range(self.steps):
					if sage.all.mod(step_counter, 2*self.alternation_constant) < self.alternation_constant:
						self.current_cone_chain.top_down(self.alternation_constant)
					else:
						self.current_cone_chain.bottom_up(self.alternation_constant)

			# At the end of each loop we save some data...
			self.print_graphs()
			print("Saving summary...")
			self.save_summary()
			print('Saving to file...')
			self.save_file()
		
			if self.batch_mode is False:
				user_continue = experiment_io_tools.query_yes_no("Completed {} steps this run so far.\n\tSaved data and printed graph. Continue?".format(self.current_cone_chain.number_of_steps()-original_count))
 			else:
 				user_continue = False



 	def manual_input(self):
 		""" Terminal UI function to allow for manual input of experiments. """
		continueinput = True

		while continueinput:
			outer_generators = []
		
			while True:
				try:
					experiment_io_tools.new_screen("Entering Extremal Generators of Outer Cone")
					
					print("Current list of extremal generators for the OUTER cone: {}".format(outer_generators))
					experiment_io_tools.printseparator()
					handle = raw_input("Please enter an extremal generator \"x_1,...,x_d\" of the outer cone without quotes, \nor type \"finish\" when done: ")
					if str(handle).lower() == "finish":
						if len(outer_generators) +1 < self.dimension:
							print("Not enough generators for a full dimensional cone!")
						else:
							break
					else:
						handlelist = [ int(i) for i in handle.split(",")]						
						if len(handlelist) <> self.dimension:
							print("Incorrect dimension.")
						else:
							outer_generators.append(handlelist)		
				except Exception as inputerror:
					print("Input error detected: {}".format(inputerror))
				
			temp_outer = sage.all.Polyhedron(rays=outer_generators,backend='normaliz')
			
			inner_generators = []
			while True:
				try:
					experiment_io_tools.new_screen("Entering Extremal Generators of Inner Cone")

					print("Current list of extremal generators for the INNER cone: {}".format(inner_generators))
					experiment_io_tools.printseparator()
					handle = raw_input("Please enter an extremal generator \"x_1,...,x_d\" of the inner cone without quotes, \nor type \"finish\" when done: ")
					if handle.lower() == "finish":
						if len(inner_generators) < self.dimension:
							print("Not enough generators for a full dimensional cone!")
							break
						else:
							break
					else:
						handlelist = [int(i) for i in handle.split(",")]						
						if len(handlelist) <> self.dimension:
							print("Incorrect dimension.")
						elif temp_outer.contains(handlelist):
							inner_generators.append(handlelist)
						else:
							print("{} is not contained in outer cone!".format(handlelist))				
				except Exception as inputerror:
					print("Input error detected: {}".format(inputerror))
				
			temp_inner = sage.all.Polyhedron(rays=inner_generators,backend='normaliz')
			continueinput = not cone_tools.sanity_check(temp_inner,temp_outer)
			if continueinput:
				print("Some error occured, please do this again.")
		self.current_cone_chain = cone_chain.ConeChain(temp_inner,temp_outer)

	#################################################
	# DEBUG FUNCTION: Recalculate all Hilbert Basis #
	#################################################

	def recalc_experiment(self):
		print("Recalculating '{}'".format(self.experiment_name))

		totalsteps = self.current_cone_chain.number_of_steps()
		print("There are {} cones.".format(totalsteps))
		self.current_cone_chain.recalc()



if __name__ == "__main__":
	debug = ConeConjectureTester()