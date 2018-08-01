#!/usr/bin/env sage
""" Wrapper of the experiment, contains all interface stuff
"""

import sage.all
import experiment
import experiment_io_tools
import cone_tools
import cone_chain


class ConeConjectureTester(object):
	"""All user interface with the Experiment object goes here.
	"""
	def __init__(self):


	def ask_random_or_input(self):
		""" Prompts user if they want to generate the cone 
		randomly or raw input 
		Args: none
		Returns: True if randomly generated, False otherwise.
		"""
		experiment_io_tools.new_screen("Initializing experiment in dimension {}...".format(self.dimension))
		return experiment_io_tools.query_yes_no("Generate cones randomly?")


	def ask_number_of_trials(self):
		""" Prompts user if they want default number of trials 
		Args: none
		Returns: 
			DEFAULT_NUM_OF_TRIALS if default
			numtrials otherwise.
		"""
		experiment_io_tools.new_screen("Initializing randomly generated experiment in dimension {}...".format(self.dimension))
		# ask if we keep default number of trials, if so just skip everything else
		if experiment_io_tools.query_yes_no("Keep default number of trials ({})?".format(DEFAULT_NUMBER_OF_TRIALS)):
			return DEFAULT_NUMBER_OF_TRIALS
		else:
			# otherwise we loop through until we get a valid input
			while True:
				try:
					# ask for an input here, if we have 1 or more done.
					numtrials = int(input("Number of trials = "))
					if numtrials >= 1:
						return numtrials
					else:
						print("Please enter a positive integer...")
				except:
					print("Please enter a positive integer...")
			return numtrials


	def manual_input(self):
		""" prompts to input cones
		Args: none
		Returns: user_inner, user_outer
			user_inner (SAGE.geometry.Polyhedron)
			user_outer (SAGE.geometry.Polyhedron)
		"""

	def vector_input(self):
		""" Prompts user to input a vector.
		Args: none
		Returns: integer vector
		"""