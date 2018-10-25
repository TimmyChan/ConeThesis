#!/usr/bin/env sage

import sage.all
import os
import cone_conjecture_tester as cct
import string

if __name__ == "__main__":
	dimension = 5
	for condition in range(10):
		for n in range(2):
			numgen = dimension + n 
			for i in range(2):
				expr_name = "{} generators 1 bound {}".format(numgen,string.ascii_uppercase[condition])
				mode = i+1
				if i == 1:
					expr_name += " bottomup"
				print("Beginning expr_name...")
				tester = cct.ConeConjectureTester(dim=dimension,expr_name=expr_name,runmode=mode,batchmode=True,numgen=numgen)
				tester.batch_create_experiment()
				tester.run_experiment()
