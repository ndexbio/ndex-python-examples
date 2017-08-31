
import ndex.client as nc
import ontology_utils
import pronto
from ndex.networkn import NdexGraph

import argparse

parser = argparse.ArgumentParser(description='build a GO ontology map from an OBO file and a gene annotation file')

parser.add_argument('obo_file', action='store')
parser.add_argument('gene_annotation_file', action='store')
parser.add_argument('root_term_id', action='store')

parser.add_argument('ndex_output', action='store')
parser.add_argument('username', action='store')
parser.add_argument('password', action='store')

arg = parser.parse_args()

print "creating term map with gene annotations " + str(arg.gene_annotation_file)
term_map = ontology_utils.create_term_map(arg.gene_annotation_file)

print "loading ontology " + str(arg.obo_file)
ontology = pronto.Ontology(arg.obo_file)

#print "annotated " + str(len(annotated_genes)) + " genes"

print "propagating annotations for root " + arg.root_term_id

propagated_genes = ontology_utils.propagate_ontology_under_root(ontology, arg.root_term_id, term_map)

print "building network"

# create NdexGraph from annotated ontology

map = ontology_utils.ontology2NdexGraph(ontology, term_map, arg.root_term_id)

ndex = nc.Ndex(host="http://www.ndexbio.org", username="drh", password="drh")

map.set_name("GO Biological Process Annotated")

# Apply a cytoscape style from a template network
#template_id = '4f53171c-600f-11e6-b0a6-06603eb7f303'
#toolbox.apply_template(Map, template_id)

# Apply a layout
#ontology_layout.apply(Map)

# Save Map to NDEx in the specified account
#map.upload_to(arg.ndex_output, arg.username, arg.password)

cx = map.to_cx()
ndex.save_new_network(cx)

#edge_aspect = ca.edges(map)

#node_aspect = ca.nodes(map)

#node_attributes = ca.node_attributes(map)

#network_attributes = ca.network_attributes(map)

#print str(len(edge_aspect))

map.write_to("test_map.cx")