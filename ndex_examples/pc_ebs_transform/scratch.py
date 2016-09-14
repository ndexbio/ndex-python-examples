from ndex.networkn import NdexGraph
from layouts import apply_directed_flow_layout


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

# Step 2:
#   apply a layout
apply_directed_flow_layout(G, ['controls-phosphorylation-of', 'controls-transport-of'])

# Step 3
#   get a template network
#   apply the visual style

# Step 4
#   write the network as a new network in the selected account

G.set_name('filtered network')

G.upload_to(ndex_server, username, password)

