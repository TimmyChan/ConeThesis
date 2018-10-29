#!/usr/bin/env sage

import sage.all
import os
import cone_conjecture_tester as cct
import string

if __name__ == "__main__":
	dimension = 5
	bound = 2
	conditions = 10

	possiblenames = ["{} generators {} bound {}".format(g,b,string.ascii_uppercase[char]) for g in range(dimension,dimension+2) 
		for b in range(1,bound+1)
		for char in range(10)] 
	possiblenames += ["{} generators {} bound {} bottomup".format(g,b,string.ascii_uppercase[char]) for g in range(dimension,dimension+2) for b in range(1,bound+1) for char in range(10)] 
	possiblenames.sort()
	print("Possible names: \n{}".format(possiblenames))

	alreadyopen = os.listdir("DATA/{}d".format(dimension))
	alreadyopen.sort()
	print("Already started: \n{}".format(alreadyopen))

	for n in range(2):
		numgen = dimension + n 
		for condition in range(10):
			#topdown
			mode = 1
			expr_name = "{} generators {} bound {}".format(numgen,bound,string.ascii_uppercase[condition])
			if expr_name not in alreadyopen:
				print("Beginning {}...".format(expr_name))
				tester = cct.ConeConjectureTester(dim=dimension,expr_name=expr_name,runmode=mode,batchmode=True,numgen=numgen,rmax=bound)
				tester.batch_create_experiment()
				tester.run_experiment()
			else:
				print("Skipping {}...".format(expr_name))
				
			#bottomup
			mode = 2
			expr_name_bottomup = expr_name + " bottomup"
			if expr_name_bottomup not in alreadyopen:
				tester = cct.ConeConjectureTester(dim=dimension,expr_name=expr_name_bottomup,runmode=mode,batchmode=True,numgen=numgen,rmax=bound)
				tester.load_file(initial_condition=True,custom_name=expr_name) #load up the associated top down init conditions
				tester.save_file("Initial Conditions")
				tester.save_file()
				tester.save_summary()

				print("Beginning {}...".format(expr_name_bottomup))
				tester.run_mode = 2
				tester.batch_mode = True
				tester.run_experiment()
			else:
				print("Skipping {}...".format(expr_name_bottomup))