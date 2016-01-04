import merge as m
import json
from os import listdir, makedirs, path
from os.path import isfile, isdir, join, abspath, dirname, exists, basename, splitext
import datamodel as dm
import idmapper

parent_dir = dirname(abspath(__file__))

noi_file = join(parent_dir, "test_files/network_of_interest.cx")
network_c_file = join(parent_dir, "test_files/network_c.cx")
merged_file = join(parent_dir, "test_files/network_merge.cx")

with open(noi_file, 'rb') as network_of_interest:
    to_network = dm.NetworkCX()
    to_network.from_cx(network_of_interest)

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

with open(network_c_file, 'rb') as input:
    from_network = dm.NetworkCX()
    from_network.from_cx(input)

from_network.print_stats()

#print(from_network.get_nodes().)

from_network_node_to_gene_map = m.node_to_gene_map(from_network, idmapper.get_genes(from_network.get_ids()))
#
merged_network = m.merge(from_network, to_network, from_network_node_to_gene_map, to_network_gene_to_node_map)
#
with open(merged_file, 'wb') as output:
     merged_network.to_cx(output)




