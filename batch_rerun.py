#!/usr/bin/env sage

import sage.all
import os
import cone_conjecture_tester as cct
import string
import experiment_io_tools
import time

if __name__ == '__main__':
	'''accept_dimension = False
	while not accept_dimension:
		dimension = experiment_io_tools.ask_int("Dimension? ")
		if dimension >1 :
			accept_dimension = True
		else:
			print("\tEnter valid dimension please.")
	'''
	steps = 200
	accept_steps = experiment_io_tools.query_yes_no("Current number of steps to continue is [{}]. Keep settings?".format(steps))
	while not accept_steps:
		steps = experiment_io_tools.ask_int("Steps? ")
		if steps >= 1:
			accept_steps = True
		else:
			print("\tEnter a positive integer please.")

	run_time = 30 # MINUTES

	accept_time = experiment_io_tools.query_yes_no("Run for {} minutes. Keep settings?".format(run_time))
	while not accept_time:
		run_time = experiment_io_tools.ask_int("Time limit? ")
		if run_time > 0:
			accept_time = True
		if run_time <= 0:
			print("\tEnter a positive integer please.")
	start_time = time.time()
	finish_time = start_time + 60* run_time # run this for 30 minutes

	while time.time() <= finish_time:
		for dimension in range(4,6):
			open_experiments = os.listdir("DATA/{}d".format(dimension))
			open_experiments.sort()
			
			for experiment in open_experiments:
				try:
					tester = cct.ConeConjectureTester(dimension,expr_name=experiment,batchmode=True,steps=steps)
					tester.load_file()
					#if not tester.current_cone_chain.sequence_complete:
					tester.recalc_experiment()
					tester.print_graphs()
					tester.save_file()
					tester.save_summary()					
					#else:
					#	print("{} already complete. Skipping...".format(experiment))
					
				except:
					with open("batch_errors.log",'a') as fp:
						fp.write("{} Error loading/saving ".format(time.time()) + experiment + "\n")
						fp.close()
					print("Error loading/saving " + experiment +". Logged and moving on...")
				
				print("\t\t\tRUN TIME: {} seconds".format(round(time.time()-start_time,2)))
				if time.time()> finish_time:
					break

			if time.time()> finish_time:
				break