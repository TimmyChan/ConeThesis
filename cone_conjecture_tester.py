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

	Attributes:
		directory (string): where will the data be saved/loaded
		dimension (int): dimension of the current experiment.
		experiment_name (string): Experiment name
		current_cone_chain (ConeChain): current actual data

	UI Attributes:
		batch_mode (boolean): flag to denote if batch mode is happening
		
	Global Attributes:
		main_menu_dict (dictionary): dictionary of choices for the main menu
	"""
	text_main_title = "Cone Conjecture Tester v1.0"


	text_create = "Create new experiment"
	
	text_load_continue = "Load and continue existing experiment"
	text_load_copy = "Load and copy existing experiment to new file (Not available yet)"
	text_load_initial = "Load only initial values of previous experiment (Not available yet)"

	text_save_exit = "Save and exit"
	text_summary = "Display summary of current experiment"
	text_run_experiment = "Run current experiment with current settings"
	text_change_settings = "Display and/or change current settings"

	main_menu_dict_initial = {1: text_create,
							2: text_load_continue,
							3: text_load_copy,
							4: text_load_initial,
							9: text_save_exit}

	main_menu_dict_loaded =  { 	0: text_run_experiment,
								1: text_create,
								2: text_load_continue,
								3: text_load_copy,
								4: text_load_initial,
								5: text_summary,
								#6: text_change_settings,
								9: text_save_exit}



	text_top_down = "Top Down"
	text_bottom_up = "Bottom Up"
	text_alternating = "Alternating"

	# not zero
	run_mode_dict = {	1: text_top_down,
						2: text_bottom_up,
						3: text_alternating}

	def __init__(self, dim=None, expr_name=None, some_cone_chain=None, runmode=None, batchmode=False):
		self.dimension = dim  #dimension
		self.experiment_name = expr_name #experiment name
		self.directory = None # default will be DATA/{}d/expr_name/
		self.raw_data_path = None #default will be DATA/{}D/expr_name/expr_name.json

	
		self.bound = 2 # maximum value a coordinate will have


		self.run_mode = 0 # see run_mode_dict for options


		self.steps = 100 # default number of steps to run between printouts
		self.alternation_constant = 1 # number of steps of top down and bottom up to run as you alternate


		self.current_cone_chain = some_cone_chain
		self.batch_mode = batchmode 


		self.loaded = False if self.current_cone_chain is None else True
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
				self.run_mode_menu()
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

											
								
			#9
			elif ConeConjectureTester.main_menu_dict_loaded[main_menu_choice] == ConeConjectureTester.text_save_exit:
				# exit
				self.check_loaded()
				if self.loaded:
					self.save_summary()
					self.current_cone_chain.output_to_terminal()
				running = False


	def main_menu(self):
		if self.loaded:
			return experiment_io_tools.menu(ConeConjectureTester.main_menu_dict_loaded,
											ConeConjectureTester.text_main_title,
											self.file_setting_string()+experiment_io_tools.separator())
		else:
			return experiment_io_tools.menu(ConeConjectureTester.main_menu_dict_initial,
											ConeConjectureTester.text_main_title)


	def run_mode_menu(self):
		if self.loaded:
			return experiment_io_tools.menu(ConeConjectureTester.run_mode_dict,
											"Choose Run Mode")
		else:
			return 0


	def file_setting_string(self):
		""" returns a string that shows settings """
		settings = "Current Settings: \n\tDimension = {}\n".format(self.dimension)
		settings += "\tExperiment Name = {}\n".format(self.experiment_name)
		settings += "\tRaw Data path = {}\n".format(self.raw_data_path)
		return settings


	def create_experiment(self):
		"""Asks the relevant information then checks to see if randomly generated 
		or user inputted"""
		experiment_io_tools.new_screen(ConeConjectureTester.text_create)
		self.ask_dimension()
		self.ask_experiment_name()
		self.update_paths(self.experiment_name)
		#make the directory if it doesn't exist
		try:
			os.makedirs(self.directory, 0755) 
		except:
			None
		self.ask_bound()
		print("Generating New Cones...")
		outer_cone = cone_tools.generate_cone(self.dimension, self.bound)
		inner_cone = cone_tools.generate_inner_cone(outer_cone, self.bound)
		self.current_cone_chain = cone_chain.ConeChain(inner_cone, outer_cone)
		self.save_file("Initial Conditions.json")
		self.save_file()
		self.check_loaded()

		experiment_io_tools.pause()


	def load_experiment(self,initial_condition=False):
		experiment_io_tools.new_screen(ConeConjectureTester.text_load_continue)

		accept_expr_choice = False
		while not accept_expr_choice:
			self.ask_dimension()
			try:
				possible_experiment_names = os.listdir("DATA/{}d/".format(self.dimension))
				choose_experiment_menu = {i+1: possible_experiment_names[i] for i in range(len(possible_experiment_names)) }
				choose_experiment_menu.update({-1:"... back to main menu..."})
				user_choice = experiment_io_tools.menu(choose_experiment_menu)
				if user_choice <> -1:
					self.experiment_name = choose_experiment_menu[user_choice]
					accept_expr_choice = experiment_io_tools.query_yes_no("Your choice is '{}'. \n\tAccept?".format(self.experiment_name))
			except:
				experiment_io_tools.pause("Problem finding or opening folder, likely non-existent path.")

		if user_choice <> -1:
			self.update_paths(self.experiment_name)
			self.load_file(initial_condition)
			self.check_loaded()
			experiment_io_tools.pause()
			self.current_cone_chain.output_to_terminal()
	
				
	def load_file(self,initial_condition):
		print("Loading file: {}".format(self.raw_data_path))
		try:
			with open(self.raw_data_path, 'r') as fp:
				if initial_condition:
					self.current_cone_chain = json.load(fp, cls=cone_chain.ConeChainInitialConditionExtractor)
					self.ask_experiment_name()
					self.update_paths()
					self.save_file()
				else:
					self.current_cone_chain = json.load(fp, cls=cone_chain.ConeChainDecoder)
			print('\tloading successful...')
		except:
			print('\tA file loading error has occured.')

	def save_file(self, filename=None):
		file_name = self.experiment_name+".json" if filename is None else filename
		try:
			with open(self.directory + file_name, 'w') as fp:
				json.dump(self.current_cone_chain, fp, cls=cone_chain.ConeChainEncoder,sort_keys=True,
					indent=4, separators=(',', ': '))
		except:
			None

	def check_loaded(self):
		if self.current_cone_chain is None:
			self.loaded = False
		else:
			self.loaded = True


	def update_paths(self, new_expr_name=None):
		if new_expr_name is None:
			self.ask_experiment_name()
		else:
			self.experiment_name = new_expr_name

		if self.dimension is None:
			self.ask_dimension()
		self.directory = "DATA/{}d/".format(self.dimension) + self.experiment_name + "/"
		self.raw_data_path = self.directory + self.experiment_name + ".json"

				
	def save_summary(self,folder=None,experiment_name=None):
		""" """
		# 
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
		"""Asks user for the experiment name and sets self.experiment_name"""
		if self.experiment_name is not None:
			accept_name = not experiment_io_tools.query_yes_no("Current experiment name set to be {}. Change current setting? ".format(self.experiment_name))
		else:
			accept_name = False
		while not accept_name:
			self.experiment_name = str(raw_input("Experiment Name: "))
			accept_name = experiment_io_tools.query_yes_no("\tYou entered '{}'. Accept?".format(self.experiment_name))


	def ask_dimension(self):
		"""Asks user for the dimension and sets self.dimension"""
		if self.dimension <> None:
			valid_dimension = experiment_io_tools.query_yes_no("Current dimension set to be {}. Keep current setting? ".format(self.dimension))
		else:
			valid_dimension = False

		while not valid_dimension:
			self.dimension = experiment_io_tools.ask_int("Enter dimension: ")
			if self.dimension > 1:
				valid_dimension = True

	def ask_bound(self):
		"""Asks user for the bound of the random number generator and sets self.bound"""
		if self.bound > 0:
			accept_bound = experiment_io_tools.query_yes_no("Current random numbers bound at +/-{}. Keep current setting? ".format(self.bound))
		else:
			accept_bound = False

		while not accept_bound:
			self.bound = experiment_io_tools.ask_int("Enter the absolute bound for coordinates in these vectors: ")
			if self.bound > 0:
				accept_bound = True

	def ask_steps(self):
		"""Asks user for the number of times to run the algorithms between saving and sets self.steps"""
		if self.steps > 0:
			accept_steps = experiment_io_tools.query_yes_no("Run '{}' {} steps. Keep current setting? ".format(ConeConjectureTester.run_mode_dict[self.run_mode],self.steps))
		else:
			accept_steps = False

		while not accept_steps:
			self.steps = experiment_io_tools.ask_int("Enter the number of steps to run {}: ".format(ConeConjectureTester.run_mode_dict[self.run_mode]))
			if self.steps > 0:
				accept_steps = True

	def ask_alternation_constant(self):
		"""Asks user for the number of times to run top_down/bottom_up before alternating"""
		if self.steps > 0:
			accept_alternation_constant = experiment_io_tools.query_yes_no("'{}' is currently set to switch every {} step(s). Keep current setting? ".format(ConeConjectureTester.run_mode_dict[self.run_mode],self.alternation_constant,self.steps))
		else:
			accept_alternation_constant = False

		while not accept_alternation_constant:
			self.alternation_constant = experiment_io_tools.ask_int("Enter the alternating constant: ".format(ConeConjectureTester.run_mode_dict[self.run_mode]))
			if self.stalternation_constanteps > 0:
				accept_alternation_constant = True


	def run_experiment(self):
		if self.run_mode not in ConeConjectureTester.run_mode_dict.keys():
			self.run_mode = self.run_mode_menu()

		self.ask_steps()

		experiment_io_tools.new_screen(self.experiment_name)
		user_continue = experiment_io_tools.query_yes_no("Begin running '{}'?".format(ConeConjectureTester.run_mode_dict[self.run_mode]))

		original_count = self.current_cone_chain.number_of_steps()
		while user_continue:
			print("\trunning '{}' for {} steps...".format(ConeConjectureTester.run_mode_dict[self.run_mode],self.steps))
			steps_ran_this_sitting = self.current_cone_chain.number_of_steps()-original_count
			if ConeConjectureTester.run_mode_dict[self.run_mode] == ConeConjectureTester.text_top_down:
				self.current_cone_chain.top_down(self.steps)
			
			elif ConeConjectureTester.run_mode_dict[self.run_mode] == ConeConjectureTester.text_bottom_up:
				self.current_cone_chain.bottom_up(self.steps)

			elif ConeConjectureTester.run_mode_dict[self.run_mode] == ConeConjectureTester.text_alternating:
				for i in range(self.steps):
					if sage.all.mod(steps_ran_this_sitting, 2*self.alternation_constant) < self.alternation_constant:
						self.current_cone_chain.top_down()
					else:
						self.current_cone_chain.bottom_up()

			print('Printing graph...')
			self.current_cone_chain.generate_hilbert_graphs(self.directory, self.experiment_name)
			print("Saving summary...")
			self.save_summary()
			print('Saving to file...')
			self.save_file()
		
			user_continue = experiment_io_tools.query_yes_no("Completed {} steps this run so far.\n\tSaved data and printed graph. Continue?".format(self.current_cone_chain.number_of_steps()-original_count))
 	

if __name__ == "__main__":
	debug = ConeConjectureTester()