__author__ = 'aarongary'


import logging
#from numpy import genfromtxt, dot, array
#import math
#from scipy.sparse import coo_matrix
#from scipy.sparse.linalg import expm
#import networkx as nx
from ndex.networkn import NdexGraph
import ndex.beta.toolbox as toolbox
import demo_notebooks.causal_paths.causal_utilities as cu


class DirectedPaths:

    def __init__(self):
        logging.info('DirectedPaths: Initializing')

        logging.info('DirectedPaths: Initialization complete')

    def findPaths(self, network_id,source_list,target_list,ndex_server="http://public.ndexbio.org",
                  rm_username="test",rm_password="test",npaths=20):
        print "in paths"

        G = NdexGraph(server=ndex_server, uuid=network_id, username=rm_username, password=rm_password)

        # Compute the source-target network
        P1 = cu.get_source_target_network(G, source_list, target_list, "EGFR to MAP2K1, MAP2K2", npaths=npaths)

        # Apply a layout
        toolbox.apply_source_target_layout(P1.get('network'))

        # Apply a cytoscape style from a template network
        template_id = '4f53171c-600f-11e6-b0a6-06603eb7f303'
        toolbox.apply_template(P1.get('network'), template_id)

        return {'forward': P1.get('forward'), 'reverse': P1.get('reverse'), 'network': P1.get('network').to_cx()}

    def findDirectedPaths(self, network_cx,source_list,target_list,npaths=20):
        print "in paths"

        G = NdexGraph(cx=network_cx)

        # Compute the source-target network
        P1 = cu.get_source_target_network(G, source_list, target_list, "Title placeholder", npaths=npaths)

        # Apply a layout
        toolbox.apply_source_target_layout(P1.get('network'))

        # Apply a cytoscape style from a template network
        template_id = '4f53171c-600f-11e6-b0a6-06603eb7f303'
        toolbox.apply_template(P1.get('network'), template_id)

        #TODO: Process the forward and reverse lists.  Generate [{node1},{edge1},{node2},{edge2},etc...]

        F = P1.get('forward')
        R = P1.get('reverse')
        G = P1.get('network')

        new_forward_list = self.label_node_list(F, G)

        return {'forward': P1.get('forward'), 'forward_english': new_forward_list, 'reverse': P1.get('reverse'), 'network': P1.get('network').to_cx()}

    def label_node_list(self, n_list, G):
        outer = []
        for f in n_list:
            inner = []
            next_node = 1
            #====================================
            # Take an array of nodes and fill in
            # the edge between the nodes
            #====================================
            while(next_node < len(f)):
                this_edge = G.edge.get(f[next_node - 1]).get(f[next_node]) if G.edge.get(f[next_node - 1]) is not None else None
                if(this_edge is not None):
                    inner.append(G.node.get(f[next_node - 1]).get('name'))
                    inner.append(G[f[next_node - 1]][f[next_node]].itervalues().next()['interaction'])

                next_node += 1

            # The last node needs to be added after the final edge is identified
            inner.append(G.node.get(f[next_node - 1]).get('name'))

            outer.append(inner)

        return outer