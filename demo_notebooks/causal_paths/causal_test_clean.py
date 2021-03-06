
from ndex.networkn import NdexGraph
import ndex.beta.toolbox as toolbox
import demo_notebooks.causal_paths.causal_utilities as cu


import argparse

parser = argparse.ArgumentParser(description='clean_and_layout_pc_ebs')

parser.add_argument('ndex_input', action='store')
parser.add_argument('ndex_output', action='store')
parser.add_argument('username', action='store')
parser.add_argument('password', action='store')

# NDEx Connection
ndex_server = "http://public.ndexbio.org"
rm_username="test"
rm_password="test"

# Get the RAS machine
network_id='50e3dff7-133e-11e6-a039-06603eb7f303'
G = NdexGraph(server=ndex_server, uuid=network_id, username=rm_username, password=rm_password)

# Compute the source-target network
P1 = cu.get_source_target_network(G, ['EGFR'], ['MAP2K1', 'MAP2K2'], "EGFR to MAP2K1, MAP2K2", npaths=20)

# Apply a layout
toolbox.apply_source_target_layout(P1)

# Apply a cytoscape style from a template network
template_id = '4f53171c-600f-11e6-b0a6-06603eb7f303'
toolbox.apply_template(P1, template_id)

# Save to NDEx in the drh account
P1.upload_to(ndex_server, 'drh', 'drh')

# Compute the source-target network
P2 = cu.get_source_target_network(G, ['MAP2K1'], ['MMP9'], "MAP2K1 to MMP9", npaths=20)

# Apply a layout
toolbox.apply_source_target_layout(P2)

# Apply a cytoscape style from a template network
template_id = '4f53171c-600f-11e6-b0a6-06603eb7f303'
toolbox.apply_template(P2, template_id)

# Save to NDEx in the drh account
P2.upload_to(ndex_server, 'drh', 'drh')




