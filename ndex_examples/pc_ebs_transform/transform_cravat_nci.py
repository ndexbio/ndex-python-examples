from ndex.networkn import NdexGraph
from layouts import apply_directed_flow_layout
import ndex.beta.toolbox as toolbox
import ndex.client as nc
import pc_ebs_transform as pc_xform
import argparse

#--------------------------------

def get_input_network_list(ndex, username, password):
    ndex = nc.Ndex(ndex, username=username, password=password)
    return ndex.search_networks(search_string="vegfr1", account_name=username)

def process_network(network_summary, arg, filter_list, template_network_uuid):

    #print "output_group is " + arg.input_groupname
    network_uuid = network_summary.get('externalId')
    network = NdexGraph(server=arg.ndex_input, uuid=network_uuid, username=arg.input_username, password=arg.input_password)
    pc_xform.filter_pc_ebs(network, filter_list)
    pc_xform.remove_orphans(network)

    # Step 2:
    #   apply a directed flow layout
    apply_directed_flow_layout(network, ['controls-phosphorylation-of', 'controls-transport-of'])

    # Step 3
    #   get a network that has a cytoscape visual style to use as a template
    #   apply the visual style

    toolbox.apply_template(network, template_network_uuid)

    # Step 4
    #   write the network as a new network on ndex_output in the selected account
    network.set_name(network.get_name() + ' updated')

    #network.upload_to(arg.ndex_output, arg.output_username, arg.output_password)

    network.write_to("/Users/dexter/" + network.get_name() + ".cx")



#--------------------------------
parser = argparse.ArgumentParser(description='clean_and_layout_pc_ebs')

parser.add_argument('ndex_input', action='store')
parser.add_argument('input_username', action='store')
parser.add_argument('input_password', action='store')

parser.add_argument('ndex_output', action='store')
parser.add_argument('output_username', action='store')
parser.add_argument('output_password', action='store')

arg = parser.parse_args()

filter_list = ['controls-state-change-of',  'neighbor-of']

template_network_uuid = '74be96a9-0b2d-11e6-b550-06603eb7f303'

#--------------------------------

print "input NDEx is " + arg.ndex_input
print "input_username is " + arg.input_username
print "input_password is " + arg.input_password
print "output NDEx is " + arg.ndex_output
print "output_username is " + arg.output_username
print "output_password is " + arg.output_password
print "filter_list is " + str(filter_list)

network_list = get_input_network_list(arg.ndex_input, arg.input_username, arg.input_password)

for network_summary in network_list:
    print network_summary.get('name')
    process_network(network_summary, arg, filter_list, template_network_uuid)





