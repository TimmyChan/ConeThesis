#!/usr/bin/env sage

import sage.all
import os
import cone_conjecture_tester as cct

if __name__ == "__main__":

	for i in range(2):
		dimension = i + 4
		experiments = os.listdir("DATA/{}d/".format(dimension))
		experiments.sort()
		num_experiments = len(experiments)
		print("Found {} experiments".format(num_experiments))
		for expr in experiments:
			try:
				tester = cct.ConeConjectureTester(dimension, expr_name=expr, batchmode=True)
				tester.update_paths(expr)
				tester.load_file(initial_condition=False)
				tester.check_loaded()
				tester.print_graphs()
			except:
				print("SOME ERROR for {}".format(expr))
	