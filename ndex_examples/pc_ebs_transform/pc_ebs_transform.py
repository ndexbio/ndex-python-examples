
def filter_pc_ebs(network, filter_list):

    for edge in network.edges(keys=True):
        edge_id = edge[2]
        source_id = edge[0]
        target_id = edge[1]
        interaction = network.get_edge_attribute_value_by_id(edge_id, "interaction")
        if interaction in filter_list:
            network.remove_edge(source_id, target_id, edge_id)

def remove_orphans(network):
    #   remove nodes with no edges
    for node_id in network.nodes():
        node_name = network.get_node_attribute_value_by_id(node_id)
        degree = network.degree([node_id])[node_id]
        #print node_name + " : " + str()
        if degree is 0:
            print " -- removing " + str(node_name) + " " + str(node_id)
            network.remove_node(node_id)


