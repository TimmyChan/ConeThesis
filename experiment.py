""" This module contains the experiment class
Designed to house the experiment's input and output.

TODO: we want to create a list/dictionary for each dimension, 
where each entry will house a tuple of data: a conesequence, 
experimental method used (top_down vs bottom_up vs manual).
"""

from cone_sequence import ConeSequence
import cone_tools
import experiment_io_tools

#suggested number of trials and random number generator cap
#
DEFAULT_NUMBER_OF_TRIALS = 100

class Experiment(object):
	""" Experiment class:
	Args:
		dim (int): dimension setting
	Attributes:
		dimension (int): ambient dimension of experiment
		ranodmly_generated (boolean): 	True) randomly generated experiment.
										False) user inputted cones.
		rmax (int): the upper bound used on the random integer generator	
		trials (list of ConeSequence): Will be initialized when experiment is created.
	"""
	def __init__(self, dim):
		""" Experiment should begin with a fixed dimension
		Reason for this is that experimental data will be saved 
		and eventually recalled from one single JSON database for each dimension.
		"""
		# first, set the dimension.
		self.dimension = dim
		# now ask the user if they want the cones to be 
		# randomly generated
		self.randomly_generated = self.ask_random_or_input()

		self.trials = []
		# if we want randomly generated, ask how many trials,
		# and set rmax
		if self.randomly_generated:
			self.number_of_trials = self.ask_number_of_trials()
			self.rmax = self.ask_rmax()

		else:
			self.rmax = 0
			self.number_of_trials = 1
			self.trial.append(ConeSequence(self.manual_input()))
		


	def ask_random_or_input(self):
		""" Prompts user if they want to generate the cone 
		randomly or raw input 
		Args: none
		Returns: True if randomly generated, False otherwise.
		"""
		experiment_io_tools.new_screen()
		return query_yes_no("Generate cones randomly?")

	def ask_number_of_trials(self):
		""" Prompts user if they want default number of trials 
		Args: none
		Returns: 
			DEFAULT_NUM_OF_TRIALS if default
			numtrials otherwise.
		"""
		experiment_io_tools.new_screen()
		# ask if we keep default number of trials, if so just skip everything else
		if query_yes_no("Keep default number of trials ({})?".format(DEFAULT_NUMBER_OF_TRIALS)):
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
