import merge as m
import json
from pprint import pprint
from os import listdir, makedirs, path
from os.path import isfile, isdir, join, abspath, dirname, exists, basename, splitext
import datamodel as dm
import idmapper
import ndex.client as nc



parent_dir = dirname(abspath(__file__))

ndex = nc.Ndex(host='http://dev2.ndexbio.org/', username='jackthetech', password='jackthetech')

network_of_interest_id = 'cce68a98-b68e-11e5-b3f0-0251251672f9'
reference_network_id = '6d1291da-b68f-11e5-b3f0-0251251672f9'

network_of_interest = ndex.get_network_as_cx_stream(network_of_interest_id)
to_network = dm.NetworkCX()
to_network.from_cx(network_of_interest.json())

print("--to_network_stats--")
to_network.print_stats()

to_genes = idmapper.get_genes(to_network.get_ids())
print("--------- id mapper response -------------")
print(json.dumps(to_genes, sort_keys=True, indent=4, separators=(',', ': ')))

to_label_map = m.make_label_map(to_genes)
print("--------- to_label_map -------------")
print(json.dumps(to_label_map, sort_keys=True, indent=4, separators=(',', ': ')))



to_network_gene_to_node_map = m.gene_to_node_map(to_network, to_label_map)
print("--------- to_network_gene_map -------------")

print(json.dumps(to_network_gene_to_node_map, sort_keys=True, indent=4, separators=(',', ': ')))

reference_network = ndex.get_network_as_cx_stream(reference_network_id)
from_network = dm.NetworkCX()
from_network.from_cx(reference_network.json())

print("--from_network_stats--")
from_network.print_stats()

from_genes = idmapper.get_genes(from_network.get_ids())
from_label_map = m.make_label_map(from_genes)
from_network_node_to_gene_map = m.node_to_gene_map(from_network, from_label_map)
#
merged_network = m.merge(from_network, to_network, from_network_node_to_gene_map, to_network_gene_to_node_map)

merged_network.attributes['name'] = [{'type':None, 'value': 'my_merged_network'}]

merged_file = join(parent_dir, "test_files/network_merge.cx")
with open(merged_file, 'wt') as output:
     merged_network.to_cx(output)



cx_stream = open(merged_file, 'rb')
ndex_uuid = ndex.save_cx_stream_as_new_network(cx_stream)



