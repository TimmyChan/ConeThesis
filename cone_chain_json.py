#!/usr/bin/env sage


import sage.all
import cone_tools
import cone_chain
import experiment_io_tools
import datetime
import os, sys
import json

class ConeChainElementEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, cone_chain.ConeChainElement):
			cone_rays_list_json = cone_tools.rays_list_to_json_array(obj.cone_rays_list)
			hilb_basis = cone_tools.rays_list_to_json_array(obj.hilbert_basis)
			return {'cone_rays_list' : cone_rays_list_json, 
				'generation_step' : obj.generation_step, 
				'algorithm_used' : obj.algorithm_used, 
				'hilbert_basis' : hilb_basis}
		return json.JSONEncoder.default(self, obj)

class ConeChainElementDecoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
	
	def object_hook(self, dictionary):
		if 'cone_rays_list' in dictionary:
			cone = sage.all.Polyhedron(rays=dictionary['cone_rays_list'],backend='normaliz')
		
		if dictionary['hilbert_basis'] == 'null':
			return cone_chain.ConeChainElement(cone,
				dictionary['generation_step'], 
				dictionary['algorithm_used'])
		
		else:
			return cone_chain.ConeChainElement(cone,
				dictionary['generation_step'], 
				dictionary['algorithm_used'],
				dictionary['hilbert_basis'])


class ConeChainEncoder(json.JSONEncoder):
	def default(self,obj):
		if isinstance(obj, cone_chain.ConeChain):
			outer_cone_rays_list_json = cone_tools.rays_list_to_json_array(obj.outer_cone_rays_list)
			inner_cone_rays_list_json = cone_tools.rays_list_to_json_array(obj.inner_cone_rays_list)
			top_seq = [json.dumps(cone_element,cls=ConeChainElementEncoder) for cone_element in obj.top_sequence]
			bottom_seq = [json.dumps(cone_element,cls=ConeChainElementEncoder) for cone_element in obj.bottom_sequence]
			poset_chain = [json.dumps(cone_element,cls=ConeChainElementEncoder) for cone_element in obj.cone_poset_chain]
			
			return {'outer_cone_rays_list' : outer_cone_rays_list_json,
				'inner_cone_rays_list' : inner_cone_rays_list_json,
				'dimension' : obj.dimension,
				'top_sequence': top_seq,
				'bottom_sequence': bottom_seq,
				'cone_poset_chain': poset_chain,
				'sequence_complete': obj.sequence_complete,
				'valid_poset': obj.valid_poset}
		return json.JSONEncoder.default(self, obj)

class ConeChainDecoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
	def object_hook(self, dictionary):
		if 'outer_cone_rays_list' in dictionary:
			outer = sage.all.Polyhedron(rays=dictionary['outer_cone_rays_list'],backend='normaliz')
		if 'inner_cone_rays_list' in dictionary:
			inner = sage.all.Polyhedron(rays=dictionary['inner_cone_rays_list'],backend='normaliz')
		top_seq = [json.loads(cone_element,cls=ConeChainElementDecoder) for cone_element in dictionary['top_sequence']]
		bottom_seq = [json.loads(cone_element,cls=ConeChainElementDecoder) for cone_element in dictionary['bottom_sequence']]
		poset_chain = [json.loads(cone_element,cls=ConeChainElementDecoder) for cone_element in dictionary['cone_poset_chain']]
		return cone_chain.ConeChain(inner, outer, top_seq, bottom_seq, poset_chain, dictionary['sequence_complete'], dictionary['valid_poset'])

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