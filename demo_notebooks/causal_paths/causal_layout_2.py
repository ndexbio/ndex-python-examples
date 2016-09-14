import ndex.beta.toolbox as toolbox
from ndex.networkn import NdexGraph

def test_st_layout_full(network_name,edge_file,properties_file):
    G = NdexGraph()
    toolbox.load(G, edge_file, header=False)
    toolbox.annotate(G, properties_file)
    toolbox.apply_source_target_layout(G)
    G.set_name(network_name)
    G.upload_to('http://public.ndexbio.org', 'drh', 'drh')

test_st_layout_full('MMP9_causal_fr','forward-reverse_2.tmp','linker_properties_2.txt')
