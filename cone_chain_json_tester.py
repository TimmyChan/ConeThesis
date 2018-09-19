#!/usr/bin/env sage


import sage.all
import cone_tools
import cone_chain
import experiment_io_tools

import json



if __name__ == "__main__":


	i=0
	experiment_io_tools.new_screen("Generating Cone for dimension {}:".format(i+2))
	test_outer_cone = cone_tools.generate_cone(i+2)
	test_inner_cone = cone_tools.generate_inner_cone(test_outer_cone)

	print("\tOuter cone has generators: \n\t{}".format(test_outer_cone.rays_list()))
	print("\tInner cone has generators: \n\t{}".format(test_inner_cone.rays_list()))

	json_test = cone_chain.ConeChain(test_inner_cone, test_outer_cone)

	json_test.chain_details()

