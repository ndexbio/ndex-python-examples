__author__ = 'aarongary'


import logging
#from numpy import genfromtxt, dot, array
#import math
#from scipy.sparse import coo_matrix
#from scipy.sparse.linalg import expm
#import networkx as nx
from ndex.networkn import NdexGraph
import ndex.beta.toolbox as toolbox
from ndex.beta import layouts
import demo_notebooks.causal_paths.causal_utilities as cu
from copy import deepcopy
from causal_paths.src.path_scoring import PathScoring, EdgeRanking

class DirectedPaths:

    def __init__(self):
        logging.info('DirectedPaths: Initializing')

        logging.info('DirectedPaths: Initialization complete')

        self.ref_networks = {}

    def findPaths(self, network_id, source_list, target_list, ndex_server="http://public.ndexbio.org",
                  rm_username="test",rm_password="test",npaths=20, network_name="Directed Path Network"):
        #print "in paths"

        G = NdexGraph(server=ndex_server, uuid=network_id, username=rm_username, password=rm_password)

        # Compute the source-target network
        P1 = cu.get_source_target_network(G, source_list, target_list, network_name, npaths=npaths)

        # Apply a layout
        toolbox.apply_source_target_layout(P1.get('network'))

        # Apply a cytoscape style from a template network
        template_id = '4f53171c-600f-11e6-b0a6-06603eb7f303'
        toolbox.apply_template(P1.get('network'), template_id)

        return {'forward': P1.get('forward'), 'reverse': P1.get('reverse'), 'network': P1.get('network').to_cx()}

    def findDirectedPaths(self, network_cx, original_edge_map, source_list, target_list, uuid=None, server=None, npaths=20, relation_type=None):
        if(uuid is not None):
            G = self.get_reference_network(uuid, server)
        else:
            if type(network_cx) is NdexGraph:
                G = network_cx
            else:
                G = NdexGraph(cx=network_cx)

        self.original_edge_map = deepcopy(G.edge)

        F, R, G_prime = cu.get_source_target_network(G, original_edge_map, source_list, target_list, "Title placeholder", npaths=npaths, relation_type=relation_type)

        complete_forward_list = self.reattach_edges(F, G, G_prime)  # TODO check efficiency of this call
        complete_reverse_list = self.reattach_edges(R, G, G_prime)  # TODO check efficiency of this call

        subnet = self.reattach_original_edges(F, G)

        G = None

        # Apply a cytoscape style from a template network
        template_id = '07762c7e-6193-11e5-8ac5-06603eb7f303'
        toolbox.apply_template(G_prime, template_id)

        return {'forward': F, 'forward_english': complete_forward_list, 'reverse_english': complete_reverse_list, 'reverse': R, 'network': subnet.to_cx()} #P1.get('network').to_cx()}

    def reattach_original_edges(self, F, G):
        important_nodes = [item for sublist in F for item in sublist]

        H = G.subgraph(important_nodes)
        edge_ranking = EdgeRanking()

        for source in H.edge:
            H[source]

            for target in H[source]:
                best_edge = None
                top_edge = None
                for edge in H[source][target]:
                    H[source][target][edge]["keep"] = False

                    if top_edge is None:
                        top_edge = H[source][target][edge]
                    else:
                        if edge_ranking.edge_type_rank[H[source][target][edge].get("interaction")] < edge_ranking.edge_type_rank[top_edge.get("interaction")]:
                            top_edge = H[source][target][edge]

                top_edge["keep"] = True

        return H

    def findDirectedPathsBatch(self, network_cx, original_edge_map, source_target_list, uuid=None, server=None, npaths=20, relation_type=None):
        #print "in paths"
        if(uuid is not None):
            #G = NdexGraph(server=server, uuid=uuid)
            G = self.get_reference_network(uuid, server)
        else:
            if type(network_cx) is NdexGraph:
                G = network_cx
            else:
                G = NdexGraph(cx=network_cx)

        # Compute the source-target network
        P1 = cu.get_source_target_network_batch(G, original_edge_map, source_target_list, "Title placeholder", npaths=npaths, relation_type=relation_type)

        # Apply a layout
        #toolbox.apply_source_target_layout(P1.get('network'))

        # Apply a cytoscape style from a template network
        #template_id = '4f53171c-600f-11e6-b0a6-06603eb7f303'
        #template_id = '07762c7e-6193-11e5-8ac5-06603eb7f303' #  '67c3b75d-6191-11e5-8ac5-06603eb7f303'

        #toolbox.apply_template(P1.get('network'), template_id)
        #layouts.apply_directed_flow_layout(P1.get('network'))

        #TODO: Process the forward and reverse lists.  Generate [{node1},{edge1},{node2},{edge2},etc...]

        #F = P1.get('forward')
        #R = P1.get('reverse')
        #G_prime = P1.get('network')

        #new_forward_list = self.label_node_list(F, G, G_prime)  # TODO check efficiency of this call
        #new_reverse_list = self.label_node_list(R, G, G_prime)  # TODO check efficiency of this call

        G = None

        return P1  # {'forward': P1.get('forward'), 'forward_english': new_forward_list, 'reverse_english': new_reverse_list, 'reverse': P1.get('reverse'), 'network': P1.get('network').to_cx()}

    def get_reference_network(self, uuid, host):
        if self.ref_networks.get(uuid) is None:
            G = NdexGraph(server=host, uuid=uuid)
            self.ref_networks[uuid] = G
        else:
            print "INFO: using cached network."

        return deepcopy(self.ref_networks.get(uuid))

    def convert_path_to_html(self, paths):
        html_output = "<html><head><link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css' integrity='sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u' crossorigin='anonymous'></head><body><table>"

        for path in paths:
            simplified_path = self.get_best_edges_from_path(path)
            #for

        html_output += "</table class='table'></body></html>"
        print html_output

    def get_best_edges_from_path(self, p):
        edge_ranking = EdgeRanking()
        best_path = []
        total_score = 0
        html_output = "<tr>"
        for i, multi_edges in enumerate(p):
            if i % 2 != 0:  # Odd elements are edges
                if len(multi_edges) > 0:
                    top_edge = None
                    tmp_multi_edges = None
                    if type(multi_edges) is dict:
                        tmp_multi_edges = self.convert_edge_dict_to_array(multi_edges)
                    else:
                        tmp_multi_edges = multi_edges

                    for edge in tmp_multi_edges:
                        if top_edge is None:
                            top_edge = edge
                        else:
                            if edge_ranking.edge_type_rank[edge.get("interaction")] < edge_ranking.edge_type_rank[top_edge.get("interaction")]:
                                top_edge = edge

                    print "top edge: "
                    total_score = total_score + edge_ranking.edge_type_rank[top_edge.get("interaction")]
                    html_output += "<td>" + top_edge.get("interaction") + "</td>"
                    best_path.append(top_edge.get("interaction"))
            else:
                best_path.append(multi_edges)
                html_output += " <td><span style='font-weight: bold'>" + multi_edges + "</span></td> "

        html_output += "<td> %d </td></tr>" % total_score
        #print html_output
        return html_output



    def reattach_edges(self, n_list, G, G_prime):
        result_list = []
        for f in n_list:
            inner = []
            #====================================
            # Take an array of nodes and fill in
            # the edge between the nodes
            #====================================
            for first, second in zip(f, f[1:]):
                if G_prime.edge.get(first) is not None:
                    this_edge = G_prime.edge.get(first).get(second)
                else:
                    this_edge = None

                tmp_edge_list = []

                if(this_edge is not None):
                    if(len(inner) < 1):
                        inner.append(G_prime.node.get(first).get('name'))

                    inner_edge = G.get_edge_data(first,second)

                    for k in inner_edge.keys():
                        tmp_edge_list.append(inner_edge[k])

                    inner.append(tmp_edge_list)
                    inner.append(G_prime.node.get(second).get('name'))

            result_list.append(inner)

        #==========================================
        # Rank the forward paths
        #==========================================
        results_list = []
        try:
            results_list = [f_e_i for f_e_i in result_list if len(result_list) > 0]
        except Exception as e:
            print "error ranking paths"
            print e.message

        path_scoring = PathScoring()

        results_list_sorted = sorted(results_list, lambda x, y: path_scoring.cross_country_scoring(x, y))

        return results_list_sorted