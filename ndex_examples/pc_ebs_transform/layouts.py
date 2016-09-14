import networkx as nx

def _create_edge_tuples(attractor, target):
    return [(a,t) for a in attractor for t in target]

def _add_attractor(G, attracted_nodes):
    attractor_list =[]
    attractor_list.append(G.add_new_node())
    edge_tuples = _create_edge_tuples(attractor_list, attracted_nodes)
    G.add_edges_from(edge_tuples, interaction='in-complex-with')
    return attractor_list[0]

def apply_directed_flow_layout(G, directed_edge_types):
    target_only_nodes = []
    source_only_nodes = []
    initial_pos = {}
    fixed = []
    upstream_attractor = None
    downstream_attractor = None

    for node in G.nodes():
        out_count = 0
        in_count = 0
        initial_pos[node] = (0, 0)
        edge_id = None
        for edge in G.out_edges([node], keys=True):
            edge_id = edge[2]
            interaction = G.get_edge_attribute_value_by_id(edge_id, "interaction")
            if interaction in directed_edge_types:
                out_count = out_count + 1
        for edge in G.in_edges([node], keys=True):
            edge_id = edge[2]
            interaction = G.get_edge_attribute_value_by_id(edge_id, "interaction")
            if interaction in directed_edge_types:
                in_count = in_count + 1

        if out_count is 0 and in_count > 0:
            target_only_nodes.append(node)

        if in_count is 0 and out_count > 0:
            source_only_nodes.append(node)

        # if in_count is 0 and out_count is 0:
        #     G.remove_node(node)

    if len(target_only_nodes) > 0:
        print target_only_nodes
        downstream_attractor = _add_attractor(G, target_only_nodes)
        initial_pos[downstream_attractor] = (1, 0.5)
        fixed.append(downstream_attractor)

    if len(source_only_nodes) > 0:
        print source_only_nodes
        upstream_attractor = _add_attractor(G, source_only_nodes)
        initial_pos[upstream_attractor] = (0, 0.5)
        fixed.append(upstream_attractor)

    print fixed

    G.pos = nx.spring_layout(G.to_undirected(), pos=initial_pos, fixed=fixed)

    #G.remove_nodes_from([downstream_attractor])
    #G.remove_nodes_from([upstream_attractor])

    print G.pos