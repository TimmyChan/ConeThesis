#!/usr/bin/env sage
""" This module contains the experiment class
Designed to house the experiment's input and output.

TODO: we want to create a list/dictionary for each dimension, 
where each entry will house a tuple of data: a conesequence, 
experimental method used (top_down vs bottom_up vs manual).
"""

from cone_chain import ConeChain
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
		trials (list of ConeChain): collection of randomly generated cone pairs
			and the associated intermediate cones.
		dimension (int): ambient dimension of experiment
		number_of_trials (int): Will determine how many trials to be generated.
		ranodmly_generated (boolean): 	True) randomly generated experiment.
										False) user inputted cones.
		rmax (int): the upper bound used on the random integer generator

		--- below MUST be used when randomly_generated == False ---
		inner_gens (list of lists): extremal generators of inner cone
		outer_gens (list of lists): extremal generators of outer cone
	"""
	def __init__(self, dim, randomly_generated=True, 
				number_of_trials=100, rmax=10,inner_gens=None, outer_gens=None):
		""" Experiment should begin with a fixed dimension
		Reason for this is that experimental data will be saved 
		and eventually recalled from one single JSON database for each dimension.
		"""

		self.trials = []
		# first, set the dimension.
		self.dimension = dim
		# now ask the user if they want the cones to be 
		# randomly generated
		self.randomly_generated = randomly_generated

		
		# if we have the default setting for randomly generated,
		# generate everything
		self.number_of_trials = number_of_trials
		self.rmax = rmax
		if self.randomly_generated:
			# here we generate the trials
			for i in range(number_of_trials):			
				current_outer_cone = cone_tools.generate_cone(self.dimension, self.rmax)
				current_inner_cone = cone_tools.generate_inner_cone(current_outer_cone)
				# Loop through for number of trials and initialize the ConeChian. 
				self.trials.append(ConeChain(current_inner_cone, current_outer_cone))
		else:
			self.rmax = 0
			self.number_of_trials = 1
			# MIGHT NEED THE * self.manual_input()MAYBE NOT
			user_inner_cone = sage.all.Polyhedron(rays=inner_gens, backend='normaliz')
			user_outer_cone = sage.all.Polyhedron(rays=outer_gens, backend='normaliz')
			self.trials.append(ConeChain(user_inner_cone, user_outer_cone))


	

if __name__ == "__main__":
	experiment = Experiment(2)
