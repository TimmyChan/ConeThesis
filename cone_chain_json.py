#!/usr/bin/env sage


import sage.all
import cone_tools
import cone_chain
import experiment_io_tools
import datetime
import os, sys
import json

if __name__ == "__main__":

	'''
	test_cone = cone_tools.generate_cone(3)
	test_cone_chain_element = cone_chain.ConeChainElement(test_cone)
	test_cone_chain_element.output_details()
	dump_tester = json.dumps(test_cone_chain_element, cls=ConeChainElementEncoder)
	print dump_tester
	reloaded_cone = json.loads(dump_tester, cls=ConeChainElementDecoder)
	reloaded_cone.output_details()

	array_o_cones = [cone_chain.ConeChainElement(cone_tools.generate_cone(3)) for i in range(5)]
	array_dump_tester = json.dumps(array_o_cones, cls=ConeChainElementEncoder)
	print array_dump_tester
	reloaded_array = json.loads(array_dump_tester, cls=ConeChainElementDecoder)
	for cone in reloaded_array:
		cone.output_details()
'''

 #=======================================++#

	#experiment_io_tools.pause()

	outside = cone_tools.generate_cone(3)
	inside = cone_tools.generate_inner_cone(outside)
	test_chain = cone_chain.ConeChain(inside, outside)

	test_chain.bottom_up(50)

	test_chain.chain_details()
	chain_dump_tester = json.dumps(test_chain, cls=ConeChainEncoder)

	print chain_dump_tester
	experiment_io_tools.pause()
	reloaded_chain = json.loads(chain_dump_tester,cls=ConeChainDecoder)
	reloaded_chain.chain_details()