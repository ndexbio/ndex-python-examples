__author__ = 'dexter'

import json
import cx_helper as cxh
from copy import deepcopy


# TODO handle list attributes

class ObjectWithAttributes():

    def __init__(self):
        self.attributes = {}

    def add_attribute(self, name, value, type=None):
        attribute_list = self.attributes.get(name)
        if not attribute_list:
            attribute_list = []
            self.attributes[name] = attribute_list
        attribute_list.append({'value': value, 'type': type})

    def get_attribute(self, name):
        values = self.attributes.get(name)
        if values and values.length > 0:
            return values[0]
        return None

    def get_attributes(self, name):
        values = self.attributes.get(name)
        if values:
            return values
        return []

    def merge_attributes(self, new_attributes):
        for new_key in new_attributes:
            match_exists = False
            for old_key in self.attributes:
                if new_key == old_key and type(self.attributes[old_key]) is list:
                    match_exists = True
                    for n in new_attributes[new_key]:
                        should_add = True
                        for o in self.attributes[new_key]:
                            if n['type'] == o['type'] and n['value'] == o['value']:
                                should_add = False
                                break
                        if should_add:
                            self.attributes[new_key].append(n)
            if not match_exists:
                self.attributes[new_key] = new_attributes[new_key]

class NodeCX(ObjectWithAttributes):
    def __init__(self, node_id):
        self.n = None
        self.r = None
        self.id = node_id
        self.downstream_edges = []
        self.upstream_edges = []
        ObjectWithAttributes.__init__(self)

    def get_represents(self):
        return self.get_attribute('represents')

    def get_aliases(self):
        return self.get_attributes('aliases')

    def get_ids(self):
        ids = []
        # include the name of the node
        if self.n:
            ids.append(self.n)
        # include the represents for the node
        represents = self.get_represents()
        if represents:
            ids.append(represents)
        # include all the aliases for the node
        aliases = self.get_aliases()
        for alias in aliases:
            ids.append(alias)
        return ids

    def add_upstream_edge(self, edge):
        self.upstream_edges.append(edge)

    def add_downstream_edges(self, edge):
        self.downstream_edges.append(edge)

class EdgeCX(ObjectWithAttributes):
    def __init__(self, edge_id):
        self.s = None
        self.t = None
        self.i = None
        self.id = edge_id
        ObjectWithAttributes.__init__(self)

class NetworkCX(ObjectWithAttributes):
    def __init__(self):
        self.id_node_map = {}
        self.id_edge_map = {}
        self.opaque_aspects = {}
        self.include_opaque = False
        self.max_edge_id = 0
        self.max_node_id = 0
        ObjectWithAttributes.__init__(self)

    def print_stats(self):
        print("node count = " + str(len(self.id_node_map)))
        print("edge count = " + str(len(self.id_edge_map)))

    def get_nodes(self):
        return self.id_node_map.values()

    def get_edges(self):
        return self.id_edge_map.values()

    def from_cx(self, cx_stream, include_opaque=False):
        self.include_opaque = include_opaque
        cx = json.load(cx_stream)
        for fragment in cx:
            fragment_name, elements = list(fragment.items())[0]
            for element in elements:
                self.add_element(fragment_name, element)
        self.init_node_to_edge_links()

    def init_node_to_edge_links(self):
        for edge in self.get_edges():
            edge.s.add_downstream_edges(edge)
            edge.t.add_upstream_edge(edge)

    # if for external node Y in some other network, there is a corresponding node X in this network,
    # then merge the attributes and return the id for X
    # Otherwise, create a new node Z in this network, copy attributes from Y to Z and return the id for Z
    def find_or_add_node(self, node, shared_nodes, node_to_gene_map, added_nodes):
        to_node_id = shared_nodes.get(node.id)
        if to_node_id:
            return to_node_id
        to_node_id = added_nodes.get(node.id)
        if to_node_id:
            return to_node_id
        else:
            gene = node_to_gene_map.get(node.id)
            # make a copy of node in to_network and add it to shared_nodes
            to_node = self.add_node(represents=gene, attributes=node.attributes, name=node.n)
            added_nodes[node.id] = to_node.id
        return to_node.id

    def add_node(self, name, represents, attributes):

        self.max_node_id += 1
        node_id = self.max_node_id

        node = NodeCX(node_id)
        self.id_node_map[node_id] = node
        node.n = name
        node.r = represents
        node.attributes = deepcopy(attributes)
        return node

    # Given that we want an edge between nodes specified by source_id, target_id, and interaction
    # we first attempt to find an edge meeting those specifications.
    # If found, we merge any additional attributes to the edge and return the edge.
    # Otherwise, we add a new edge and return it.
    def find_or_add_edge(self, source_id, target_id, interaction, attributes):
        source_node = self.get_node_by_id(source_id)
        target_node = self.get_node_by_id(source_id)
        # If either the source node has no exists targets or the target node has no existing sources, this new edge
        # must be new and we can short circuit the analysis by creating a new node. This code is an optimization and
        # not strictly necessary.
        if len(source_node.downstream_edges) == 0 or len(target_node.upstream_edges) == 0:
            return self.add_edge(source_id, target_id, interaction, attributes).id
        # Iterate through the downstream edges of the source only.
        # Going through the upstream edges of the target would be equally valid, but redundant since if the edge exists,
        # it must be BOTH downstream of the source AND upstream of the target.
        for downstream_edge in source_node.downstream_edges:
            # We already know that the source of the downstream edge is the source_node, is the target the target_node?
            if downstream_edge.t.id == target_id:
                # This edge has the same source and target! Very interesting. But is the interaction the same?
                if downstream_edge.i == interaction:
                    # This is the same edge. Merge attributes and return the edge.
                    downstream_edge.merge_attributes(attributes)
                    return downstream_edge.id
        return self.add_edge(source_id, target_id, interaction, attributes).id

    def add_edge(self, source_id, target_id, interaction, attributes):
        source_node = self.get_node_by_id(source_id)
        target_node = self.get_node_by_id(target_id)
        self.max_edge_id += 1
        edge_id = self.max_edge_id
        edge = EdgeCX(edge_id)
        edge.s = source_node
        edge.t = target_node
        edge.i = interaction
        edge.attributes = deepcopy(attributes)
        source_node.add_downstream_edges(edge)
        target_node.add_upstream_edge(edge)
        self.id_edge_map[edge_id] = edge
        return edge

    def add_fragment(self, fragment):
        aspect_name = fragment.get()
        for element in fragment.get():
            self.add_element(aspect_name, element)

    def add_element(self, aspect_name, element):
        if aspect_name == 'nodes':
            self.node_from_cx(element)
        elif aspect_name == 'edges':
            self.edge_from_cx(element)
        elif aspect_name == 'nodeAttributes':
            self.node_attribute_from_cx(element)
        elif aspect_name == 'edgeAttributes':
            self.edge_attribute_from_cx(element)
        elif aspect_name == 'networkAttributes':
            self.network_attribute_from_cx(element)
        elif self.include_opaque:
            self.opaque_element_from_cx(aspect_name, element)

    def get_node_by_id(self, node_id):
        node = self.id_node_map.get(node_id)
        if not node:
            node = NodeCX(node_id)
            self.id_node_map[node_id] = node
            self.max_node_id = max(self.max_node_id, node_id)
        return node

    def get_edge_by_id(self, edge_id):
        edge = self.id_edge_map.get(edge_id)
        if not edge:
            edge = EdgeCX(edge_id)
            self.id_edge_map[edge_id] = edge
            self.max_edge_id = max(self.max_edge_id, edge_id)
        return edge

    def opaque_element_from_cx(self, aspect_name, element):
        aspect = self.opaque_aspects.get(aspect_name)
        if not aspect:
            aspect = []
            self.opaque_aspects[aspect_name] = aspect
        aspect.append(element)

    def node_from_cx(self, element):
        node = self.get_node_by_id(element.get('@id'))
        node.n = element.get('n')

    def node_attribute_from_cx(self, element):
        node = self.get_node_by_id(element.get('po'))
        node.add_attribute(
            element.get('n'),
            element.get('v'),
            element.get('t'))

    def edge_from_cx(self, element):
        edge = self.get_edge_by_id(element.get('@id'))
        edge.s = self.get_node_by_id(element.get('s'))
        edge.t = self.get_node_by_id(element.get('t'))
        edge.i = element.get('i')

    def edge_attribute_from_cx(self, element):
        edge = self.get_edge_by_id(element.get('po'))
        edge.add_attribute(
            element.get('n'),
            element.get('v'),
            element.get('t'))

    def network_attribute_from_cx(self, element):
        self.add_attribute(
            element.get('n'),
            element.get('v'),
            element.get('t'))

    def get_ids(self):
        ids = []
        for node in self.id_node_map.values():
            # include the name of the node
            if node.n:
                ids.append(node.n)
            # include the represents for the node
            represents = node.get_represents()
            if represents:
                ids.append(represents)
            # include all the aliases for the node
            aliases = node.get_aliases()
            for alias in aliases:
                ids.append(alias)
        return ids

    def to_cx(self, stream):
        h = cxh.CXHelper(stream)
        h.start()

        for name in self.attributes:
            for item in self.attributes[name]:
                h.emit_cx_network_attribute(name, item['value'], item['type'])
        for node in self.get_nodes():
            node_id = h.emit_cx_node_w_id(node.id, node.n, node.r)
            for name in node.attributes:
                for item in node.attributes[name]:
                    h.emit_cx_node_attribute(node_id, name, item['value'], item['type'])
        for edge in self.get_edges():
            edge_id = h.emit_cx_edge_w_id(edge.id, edge.s.id, edge.t.id, edge.i)
            for name in edge.attributes:
                for item in edge.attributes[name]:
                    h.emit_cx_edge_attribute(edge_id, name, item['value'])
        h.end()