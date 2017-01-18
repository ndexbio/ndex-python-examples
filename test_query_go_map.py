from causal_paths.src.causpaths import DirectedPaths
import demo_notebooks.causal_paths.causal_utilities as cu
import ndex.client as nc
import ndex.networkn as networkn
import ndex.beta.layouts as layouts
import ndex.beta.toolbox as toolbox

def get_template(ndex, template_id):
    if not template_id:
        raise ValueError("no template id")
    print "template_id: " + str(template_id)
    response = ndex.get_network_as_cx_stream(template_id)
    template_cx = response.json()
    t_network = networkn.NdexGraph(template_cx)
    return t_network

server = "http://preview.ndexbio.org"
username = "drh"
password = "drh"
go_map_id = "5582e8b7-c230-11e6-9509-0ac135e8bacf"
#root_term_id = "GO:0008150"
#target_term_ids = ["GO:0060748"]
npaths = 100

source_name_list = ["cartilage condensation"]
target_name_list = ["biological_process"]

# create the server

ndex = nc.Ndex(server, username, password)

#  get the template

template_id = "87276dca-b8dd-11e6-a353-06832d634f41"
dev_ndex = nc.Ndex("http://dev.ndexbio.org", "nci-test", "nci-test")
template_network = get_template(dev_ndex, template_id)

# find directed paths between root and terms
# apply go map style
# format with directed flow

network = networkn.NdexGraph(server=server, uuid=go_map_id, username=username, password=password)
print "ontology network loaded"

# Compute the source-target network, destructively modifying the original network
path_object = cu.get_source_target_network_new(network,
                                               source_name_list,
                                               target_name_list,
                                               "go map query test",
                                               npaths=npaths,
                                               direction='forward')
print "path search done"

# Apply a cytoscape style from a template network
toolbox.apply_network_as_template(network, template_network)
print "style applied"

# Apply a layout
directed_edge_types = ["hasParent"]
# layouts.apply_directed_flow_layout(network, directed_edge_types=directed_edge_types)
layouts.apply_source_target_layout(network)
print "layout applied"
# save result
ndex.save_new_network(network.to_cx())

print "result saved"

# directedPaths = DirectedPaths()
#
# path_object = directedPaths.findPaths(
#     go_map_id,
#     source_list,
#     target_list,
#     ndex_server=server,
#     rm_username=username,
#     rm_password=password,
#     npaths=20)


