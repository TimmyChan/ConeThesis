""" This module contains the experiment class
Designed to house the experiment's input and output.

TODO: we want to create a list/dictionary for each dimension, 
where each entry will house a tuple of data: a conesequence, 
experimental method used (top_down vs bottom_up vs manual).
"""

from ConeSequence import ConeSequence
from experiment_io_tools import *

#suggested number of trials and random number generator cap
#
DEFAULT_NUMBER_OF_TRIALS = 100

class Experiment(object):
	""" Experiment class:
	Args:
		dim (int): dimension setting
	Attributes:
		dimension (int): ambient dimension of experiment
		generated (boolean): 	True) randomly generated experiment.
								False) user inputted cones.
		rmax (int): the upper bound used on the random integer generator
		data (List of tuples): Each entry will house (trial, experiment_type, 
														hilbert_basis_dict, rmax_used):
			trial (ConeSequence): Will be initialized when experiment is created.
			experiment_type (string): 	
				"Top Down" = purely top down generated sequence
				"Bottom Up" = purely bottom up generated sequence
				"Manual" = manually generated sequence
				TODO: ... Other types can be discussed 
			hilbert_basis_dict (dictionary of lists): A dictionary where each key 
				is a cone in trial, and each value is the associated hilbert basis 
				which is a list of vectors. Stays empty until trial.sequence_complete == True,
				at analyze data	step.

	"""
	def __init__(self, dim):
		""" Experiment should begin with a fixed dimension
		Reason for this is that experimental data will be saved 
		according to 
		"""
		# first, set the dimension.
		self.dimension = dim
		self.generated = self.ask_random_or_input()
		self.number_of_trials = self.ask_number_of_trials()


	def ask_random_or_input(self):
		""" Prompts user if they want to generate the cone 
		randomly or raw input 
		Args: none
		Returns: True if randomly generated, False otherwise.
		"""
		new_screen()
		return query_yes_no("Generate cones randomly?")

	def ask_number_of_trials(self):
		""" Prompts user if they want default number of trials 
		Args: none
		Returns: 
			DEFAULT_NUM_OF_TRIALS if default
			numtrials otherwise.
			"""
		new_screen()
		if query_yes_no("Keep default number of trials ({})?".format(DEFAULT_NUMBER_OF_TRIALS)):
			return DEFAULT_NUMBER_OF_TRIALS
		else:
			while True:
				try:
					numtrials = int(input("Number of trials = "))
					if numtrials > 1:
						return numtrials
					else:
						print("Please enter a positive integer...")
				except:
					print("Please enter a positive integer...")
			return numtrials
