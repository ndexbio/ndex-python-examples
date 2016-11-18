from __future__ import division
from ndex.networkn import NdexGraph


def create_similarity_map(id_lists, min_subsumption, id_attribute="genes"):
    similarity_map = NdexGraph()
    set_name_to_node_id_map = {}
    id_sets = {}
    for set_name in id_lists:
        id_list = id_lists[set_name]
        id_sets[set_name] = set(id_list)
        att = {id_attribute: id_list}
        node_id = similarity_map.add_new_node(set_name, att)
        set_name_to_node_id_map[set_name] = node_id
        
    for set_name_1 in id_sets.keys():
        source_node_id = set_name_to_node_id_map[set_name_1]
        for set_name_2 in id_sets.keys():
            if set_name_1 != set_name_2:
                overlap = id_sets[set_name_1].intersection(id_sets[set_name_2])
                size_overlap=len(overlap)
                if size_overlap != 0:
                    subsumes_measure=size_overlap/len(id_sets[set_name_2])
                    if subsumes_measure > min_subsumption:
                        target_node_id = set_name_to_node_id_map[set_name_2]
                        atts = {"sub" : subsumes_measure, "overlap": overlap, "overlap_size": size_overlap}
                        similarity_map.add_edge_between(source_node_id, target_node_id, "subsumed_by", atts)



