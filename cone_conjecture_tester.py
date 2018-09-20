#!/usr/bin/env sage
""" Wrapper of the experiment, contains all interface stuff
"""
#!/usr/bin/env sage

"""ConeConjectureTester

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

import sage.all
import experiment_io_tools
import cone_tools
import cone_chain


class ConeConjectureTester(object):
	"""All user interface with the Experiment object goes here.
	"""
	main_menu_dict = {1: "New Experiment",
					  2: "Load Existing Experiment",
					  0: "Exit"}


	def __init__(self):
		self.main_choice = experiment_io_tools.menu(ConeConjectureTester.main_menu_dict,"Cone Conjecture Tester v1.0")
		valid_dimension = False
		while not valid_dimension:
			dim = experiment_io_tools.ask_int("Dimension: ")
			if dim > 1:
				valid_dimension = True
			


		if self.main_choice == 1:
			# make a new experiment
			accept_name = False
			while not accept_name:
				self.current_experiment_name = input("Experiment Name: ")
				accept_name = experiment_io_tools.query_yes_no("\tYou entered '{}'. Accept?".format(self.current_experiment_name))

			
		elif self.main_choice == 2:
			# load an old experiment
			
			

			os.listdir("./DATA/{}d/".format(dim))
		elif self.main_choice == 0:
			# exit
			fuckthis = 1


if __name__ == "__main__":
	debug = ConeConjectureTester()