from ndex.networkn import NdexGraph
from layouts import apply_directed_flow_layout
import ndex.beta.toolbox as toolbox
import pc_ebs_transform as pc_xform

import argparse

parser = argparse.ArgumentParser(description='clean_and_layout_pc_ebs')

parser.add_argument('ndex_input', action='store')
parser.add_argument('ndex_output', action='store')
parser.add_argument('username', action='store')
parser.add_argument('password', action='store')

arg = parser.parse_args()

filter_list = ['controls-state-change-of',  'neighbor-of']

source_network_uuid = '74be96a9-0b2d-11e6-b550-06603eb7f303'

template_network_uuid = '74be96a9-0b2d-11e6-b550-06603eb7f303'

#--------------------------------

print "input NDEx is " + arg.ndex_input
print "input UUID is " + source_network_uuid
print "output NDEx is " + arg.ndex_output
print "username is " + arg.username
print "password is " + arg.password

G = NdexGraph(server=arg.ndex_input, uuid=source_network_uuid)

pc_xform.filter_pc_ebs(G, filter_list)

pc_xform.remove_orphans(G)

# Step 2:
#   apply a directed flow layout
apply_directed_flow_layout(G, ['controls-phosphorylation-of', 'controls-transport-of'])

# Step 3
#   get a network that has a cytoscape visual style to use as a template
#   apply the visual style

toolbox.apply_template(G, template_network_uuid)

# Step 4
#   write the network as a new network on ndex_output in the selected account

G.set_name(G.get_name() + ' updated')

G.upload_to(arg.ndex_output, arg.username, arg.password)

G.write_to("/Users/dexter/scratch_network.cx")