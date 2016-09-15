from ndex.networkn import NdexGraph
from layouts import apply_directed_flow_layout
import ndex.beta.toolbox as toolbox


ndex_server = 'http://www.ndexbio.org'

source_network_uuid = '74be96a9-0b2d-11e6-b550-06603eb7f303'

template_network_uuid = '74be96a9-0b2d-11e6-b550-06603eb7f303'

username = 'drh'

password = 'drh'

#--------------------------------

G = NdexGraph(server=ndex_server, uuid=source_network_uuid)

# keys = G.get_all_edge_attribute_keys()
#
# for key in keys:
#     print key

# Step 1:
#   filter the edges to remove controls-state-change-of  and  neighbor-of

filter_list = ['controls-state-change-of',  'neighbor-of']

for edge in G.edges(keys=True):
    edge_id = edge[2]
    source_id = edge[0]
    target_id = edge[1]
    interaction = G.get_edge_attribute_value_by_id(edge_id, "interaction")
    if interaction in filter_list:
        G.remove_edge(source_id, target_id, edge_id)

for node_id in G.nodes():
    node_name = G.get_node_attribute_value_by_id(node_id)
    degree = G.degree([node_id])[node_id]
    print node_name + " : " + str()
    if degree is 0:
        print " -- removing " + str(node_name) + " " + str(node_id)
        G.remove_node(node_id)

# Step 2:
#   apply a layout
apply_directed_flow_layout(G, ['controls-phosphorylation-of', 'controls-transport-of'])

# Step 3
#   get a template network
#   apply the visual style

# Apply a cytoscape style from a template network

toolbox.apply_template(G, template_network_uuid)

# Step 4
#   write the network as a new network in the selected account

G.set_name('scratch network')

G.upload_to(ndex_server, username, password)

G.write_to("/Users/dexter/scratch_network.cx")