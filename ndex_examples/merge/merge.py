# Merge procedure:
#  - merged network starts as a copy of the target
#  - nodes are mapped to genes
#  - shared node: nodes in target and source that map to same gene
#  - edges from source network that connect to one or more shared nodes are added to the merged network.
#  - Source properties are added to shared nodes
#  - Source nodes and edges copied to the merged retain their properties
#
#
#  Map all node identifiers or node names to genes.
# Give preference to identifiers
# If only one network has structured identifiers, determine species from that network
# If neither network has identifiers that specify species, just match on names
# If cross-species, the target network species has precedence.
# Homology mapping will probably NOT be in the PAG version, but if we can do it that would be cool.


import datamodel as dm

def make_label_map(response):
    label_map = {}
    for match in response.get('matched'):
        species = match.get('species')
        if species and species == 'human':
            id = match.get('in')
            matches = match.get('matches')
            if id and matches:
                sym = matches.get("Symbol")
                if sym:
                    label_map[id] = sym
    return label_map

def node_to_gene_map(network, label_map):
    node_to_gene_map = {}
    for node in network.get_nodes():
        #print("node id = " + node.id)
        for identifier in node.get_ids():
            #print("  id = " + identifier)
            gene_symbol = label_map.get(identifier)

            if gene_symbol:
                #print("  sym = " + gene_symbol)
                node_to_gene_map[node.id] = gene_symbol
                break

    return node_to_gene_map

def gene_to_node_map(network, label_map):
    gene_to_node_map = {}
    for node in network.get_nodes():
        for identifier in node.get_ids():
            gene_symbol = label_map.get(identifier)
            if gene_symbol:
                gene_to_node_map[gene_symbol] = node.id
    return gene_to_node_map


def merge(from_network, to_network, from_network_node_to_gene_map, to_network_gene_to_node_map):
    # 1. Make a map of shared_nodes: from_network nodes mapped to to_network nodes based on shared gene ids
    # 2. For each shared node, copy all from_network edges containing a shared node to the to_network
    #  - In each copy operation, copy all node and edge attributes
    shared_nodes  = {}
    # Make shared_nodes map
    for from_node in from_network.get_nodes():
        from_gene = from_network_node_to_gene_map.get(from_node.id)
        if from_gene:
            to_node = to_network_gene_to_node_map.get(from_gene)
            if to_node:
                shared_nodes[from_node.id] = to_node.id

    # copy edges containing shared nodes
    for from_edge in from_network.get_edges():
        if shared_nodes.get(from_edge.s.id) or shared_nodes.get(from_edge.t.id):
            copy_edge(from_edge, to_network, from_network, shared_nodes, from_network_node_to_gene_map)

    return to_network


def copy_edge(edge, from_network, to_network, shared_nodes, from_network_node_to_gene_map):
    source_id = to_network.find_or_add_node(edge.s, shared_nodes, from_network_node_to_gene_map)
    target_id = to_network.find_or_add_node(edge.t, shared_nodes, from_network_node_to_gene_map)
    return to_network.find_or_create_edge(source_id, target_id, edge.i, edge.attributes)




