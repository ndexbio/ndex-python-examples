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

    def findDirectedPaths(self, network_cx,source_list, target_list, uuid=None, server=None, npaths=20, relation_type=None):
        #print "in paths"
        if(uuid is not None):
            #G = NdexGraph(server=server, uuid=uuid)
            G = deepcopy(self.get_reference_network(uuid, server))
        else:
            if type(network_cx) is NdexGraph:
                G = network_cx
            else:
                G = NdexGraph(cx=network_cx)

        # Compute the source-target network
        P1 = cu.get_source_target_network(G, source_list, target_list, "Title placeholder", npaths=npaths, relation_type=relation_type)

        # Apply a layout
        #toolbox.apply_source_target_layout(P1.get('network'))

        # Apply a cytoscape style from a template network
        #template_id = '4f53171c-600f-11e6-b0a6-06603eb7f303'
        template_id = '07762c7e-6193-11e5-8ac5-06603eb7f303'

        toolbox.apply_template(P1.get('network'), template_id)
        #layouts.apply_directed_flow_layout(P1.get('network'))

        #TODO: Process the forward and reverse lists.  Generate [{node1},{edge1},{node2},{edge2},etc...]

        F = P1.get('forward')
        R = P1.get('reverse')
        G_prime = P1.get('network')

        new_forward_list = self.label_node_list(F, G, G_prime)  # TODO check efficiency of this call
        new_reverse_list = self.label_node_list(R, G, G_prime)  # TODO check efficiency of this call

        G = None

        return {'forward': P1.get('forward'), 'forward_english': new_forward_list, 'reverse_english': new_reverse_list, 'reverse': P1.get('reverse'), 'network': P1.get('network').to_cx()}

    def findDirectedPathsBatch(self, network_cx, source_target_list, uuid=None, server=None, npaths=20, relation_type=None):
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
        P1 = cu.get_source_target_network_batch(G, source_target_list, "Title placeholder", npaths=npaths, relation_type=relation_type)

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

        return self.ref_networks.get(uuid)

    def label_node_list(self, n_list, G, G_prime):
        outer = []
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

            outer.append(inner)

        return outer