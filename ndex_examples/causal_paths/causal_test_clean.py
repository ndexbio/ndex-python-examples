import ndex.client as nc
import sys
from ndex.networkn import NdexGraph
import networkx as nx
from itertools import islice,chain
import ndex.beta.toolbox as toolbox

def k_shortest_paths(G, source, target, k, weight=None):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))

def shortest_paths_csv(sp_list, netn_obj, fh, path_counter=0):
    for l in sp_list:
        path_counter=path_counter+1
        genes_in_path=netn_obj.get_node_names_by_id_list(l)
        for i in xrange(0,len(genes_in_path)-1):
            es=netn_obj.get_edge_ids_by_node_attribute(genes_in_path[i],genes_in_path[i+1])
            for ed in es:
                fh.write(str(genes_in_path[i])+'\t'
                         + str(netn_obj.get_edge_attribute_by_id(ed,'interaction'))
                         +'\t'+str(genes_in_path[i+1])+'\t'+str(path_counter)+'\n')
    return path_counter

def source_list_to_target_list_all_shortest(sources,targets,netn_obj,npaths=20,fh=open('out_file.txt','w')):
    names = [netn_obj.node[n]['name'] for n in netn_obj.nodes_iter()]
    sources_list=[netn_obj.get_node_ids(i) for i in list(set(sources).intersection(set(names)))]
    sources_ids= list(chain(*sources_list))
    targets_list=[netn_obj.get_node_ids(i) for i in list(set(targets).intersection(set(names)))]
    targets_ids= list(chain(*targets_list))
    path_counter=0
    g=nx.DiGraph(netn_obj)
    for s in sources_ids:
        for t in targets_ids:
            sp_list=k_shortest_paths(g,s,t,npaths)
            path_counter=shortest_paths_csv(sp_list, netn_obj, fh, path_counter=path_counter)


def sources_to_targets_dict(sources,targets,netn_obj,npaths=1):
    names = [netn_obj.node[n]['name'] for n in netn_obj.nodes_iter()]
    sources_list=[netn_obj.get_node_ids(i) for i in list(set(sources).intersection(set(names)))]
    sources_ids= list(chain(*sources_list))
    targets_list=[netn_obj.get_node_ids(i) for i in list(set(targets).intersection(set(names)))]
    targets_ids= list(chain(*targets_list))
    g=nx.DiGraph(netn_obj)
    path_dict={}
    path_counter=0
    for s in sources_ids:
        for t in targets_ids:
            sp_list=k_shortest_paths(g,s,t,npaths)
            for sp in sp_list:
                path_dict[path_counter]=sp
                path_counter=path_counter+1
    return path_dict
#
# def add_edge_property_from_dict(netn_obj,dictionary):
#     """Takes a dictionary with keys of properties which are to be added to a list of edges"""
#     for k in dictionary.keys():
#         for e in dictionary[k]:
#             netn_obj.set_edge_attribute(e,str(k),value)

def indra_causality(netn_obj,two_way_edgetypes):
    #Function for expanding INDRA networks to causal nets.  This involves handling edge types where causality could go both ways
    add_reverse_edges=[]
    for e in netn_obj.edges_iter(data='interaction'):
        if e[2] in two_way_edgetypes:
            add_reverse_edges.append(e)
    for e2 in add_reverse_edges:
        netn_obj.add_edge_between(e2[1],e2[0],interaction=e2[2])

# def cl_develops_from(netn_obj,two_way_edgetypes=[]):
#     #Function for expanding cell ontology networks to causal nets.  This involves handling edge types where causality could go both ways
#     add_reverse_edges=[]
#     for e in netn_obj.edges_iter(data='interaction'):
#         if e[2] in two_way_edgetypes:
#             add_reverse_edges.append(e)
#     for e2 in add_reverse_edges:
#         netn_obj.add_edge_between(e2[1],e2[0],interaction=e2[2])

def k_shortest_paths_multi(G, sources,targets,npaths=20):
    names = [G.node[n]['name'] for n in G.nodes_iter()]
    sources_list=[G.get_node_ids(i) for i in list(set(sources).intersection(set(names)))]
    sources_ids= list(chain(*sources_list))
    targets_list=[G.get_node_ids(i) for i in list(set(targets).intersection(set(names)))]
    targets_ids= list(chain(*targets_list))
    path_counter=0
    g=nx.DiGraph(G)
    all_shortest_paths = []
    for s in sources_ids:
        for t in targets_ids:
            sp_list=k_shortest_paths(g,s,t,npaths)
            for path in sp_list:
                all_shortest_paths.append(path)
            #path_counter=shortest_paths_csv(sp_list, netn_obj, fh,path_counter=path_counter)
    return list(all_shortest_paths)

def network_from_paths(G, forward, reverse, sources, targets):
    M = NdexGraph()
    edge_tuples=set()
    for path in forward:
        add_path(M, G, path, 'Forward', edge_tuples)
    for path in reverse:
        add_path(M, G, path, 'Reverse', edge_tuples)
    for source in sources:
        M.node[source]['st_layout'] = 'Source'
    for target in targets:
        M.node[target]['st_layout'] = 'Target'
    add_edges_from_tuples(M, list(edge_tuples))
    return M

def add_path(network, old_network, path, label, edge_tuples, conflict_label='Both'):
    add_path_nodes(network, old_network, path, label, conflict_label)
    for index in range(0, len(path)-1):
        tuple=(path[index],path[index+1])
        edge_tuples.add(tuple)

def add_path_nodes(network, old_network, path, label, conflict_label):
    for node_id in path:
        if node_id not in network.node:
            old_name = old_network.node[node_id]['name']
            network.add_node(node_id, st_layout=label, name=old_name)
        else:
            current_label = network.node[node_id]['st_layout']
            if current_label is not label and current_label is not conflict_label:
                network.node[node_id]['st_layout'] = conflict_label

def add_edges_from_tuples(network, tuples):
    for tuple in tuples:
        network.add_edge_between(tuple[0], tuple[1])

def get_node_ids_by_names(G, node_names):
    node_ids = set()
    for name in node_names:
        for id in G.get_node_ids(name, 'name'):
            node_ids.add(id)
    return list(node_ids)


#if __name__ == "__main__":
ndex = nc.Ndex("http://public.ndexbio.org", username="test", password="test")

#Get the RAS machine
ndex_server = "http://public.ndexbio.org"
network_id='50e3dff7-133e-11e6-a039-06603eb7f303'
rm_username="test"
rm_password="test"
G = NdexGraph(server=ndex_server, uuid=network_id, username=rm_username, password=rm_password)
#result = ndex.get_network_as_cx_stream(network_id)
#cx = result.json()
#d = NdexGraph(cx)

# interpret INDRA statements into causal directed edges
# needs to specify which edges must be doubled to provide both forward and reverse
two_way_edgetypes = ['Complex']
indra_causality(G, two_way_edgetypes)

# forward and reverse direction paths for first pair of sources and targets
source_names=['MAP2K1']
target_names=['MMP9']
npaths = 20
forward1 = k_shortest_paths_multi(G, source_names, target_names, npaths)
reverse1 = k_shortest_paths_multi(G, target_names, source_names, npaths)

source_ids=get_node_ids_by_names(G, source_names)
target_ids=get_node_ids_by_names(G, target_names)
P1 = network_from_paths(G, forward1, reverse1, source_ids, target_ids)
P1.set_name("MAP2K1 to MMP9")

#P1.write_to("/Users/dexter/bad_network.cx")

print P1.get_name()

toolbox.apply_source_target_layout(P1)

template_id = '4f53171c-600f-11e6-b0a6-06603eb7f303'
toolbox.apply_template(P1, template_id)

P1.upload_to(ndex_server, 'drh', 'drh')




#forward direction paths sent to test_paths_2.txt
# fh=open('test_paths_2.txt','w')
# sources=['MAP2K1']
# targets=['MMP9']
#
# source_list_to_target_list_all_shortest(sources,targets,d,fh=fh)
# fh.close()

#reverse direction paths sent to test_paths_2_reverse.txt
# fh_reverse=open('test_paths_2_reverse.txt','w')
#
# targets=['MAP2K1']
# sources=['MMP9']
# source_list_to_target_list_all_shortest(sources,targets,d,fh=fh_reverse)
#
# fh_reverse.close()

#at this point, we have all forward and all reverse paths in tab delimited files
#they need to be mergred and we need to derive the forward/revese/both/source/target
#labels, which is done in the Makefile

