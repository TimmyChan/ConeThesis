#!/usr/bin/env sage

import sage.all
import os
import cone_conjecture_tester as cct
import string
import experiment_io_tools

if __name__ == '__main__':
	accept_dimension = False
	while not accept_dimension:
		dimension = experiment_io_tools.ask_int("Dimension? ")
		if dimension >1 :
			accept_dimension = True
		else:
			print("\tEnter valid dimension please.")

	steps = 200
	accept_steps = experiment_io_tools.query_yes_no("Current number of steps to continue is [{}]. Keep settings?".format(steps))
	while not accept_steps:
		steps = experiment_io_tools.ask_int("Steps? ")
		if steps >= 1:
			accept_steps = True
		else:
			print("\tEnter a positive integer please.")


	open_experiments = os.listdir("DATA/{}d".format(dimension))
	open_experiments.sort()
	for experiment in open_experiments:
		tester = cct.ConeConjectureTester(dimension,expr_name=experiment,batchmode=True,steps=steps)
		tester.load_file()
		tester.run_experiment()