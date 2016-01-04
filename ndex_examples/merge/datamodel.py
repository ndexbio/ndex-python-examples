__author__ = 'dexter'

from cxio.cx_reader import CxReader

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

class NodeCX(ObjectWithAttributes):
    def __init__(self, node_id):
        self.n = None
        self.r = None
        self.id = node_id
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
        reader = CxReader(cx_stream)
        for element in reader.aspect_elements():
            aspect_name = element.get_name()
            self.add_element(element.get_name(), element.get_data())

    # if for external node Y in some other network, there is a corresponding node X in this network,
    # then merge the attributes and return the id for X
    # Otherwise, create a new node Z in this network, copy attributes from Y to Z and return the id for Z
    def find_or_add_node(self, node, shared_nodes, node_to_gene_map):
        to_node_id = shared_nodes.get(node.id)
        if to_node_id:
            return to_node_id
        else:
            gene = node_to_gene_map.get(node.id)
            # make a copy of node in to_network and add it to shared_nodes
            to_node = self.add_node(node_id=None, represents=gene, attributes=node.attributes, name=node.n)
            shared_nodes[node.id] = to_node.id
        return to_node.id

    def add_node(self, node_id=None, name=None, represents=None, attributes={}):
        if node_id:
            self.max_node_id = max(self.max_node_id, node_id)
        else:
            self.max_node_id += self.max_node_id
            node_id = self.max_node_id

        node = NodeCX(node_id)
        self.id_node_map[node_id] = node
        if name:
            node.n = name
        if represents:
            node.r = represents
        node.attributes = attributes
        return node

    # Given that we want an edge between nodes specified by source_id, target_id, and interaction
    # we first attempt to find an edge meeting those specifications.
    # If found, we merge any additional attributes to the edge and return the edge.
    # Otherwise, we add a new edge and return it.
    def find_or_add_edge(self, source_id, target_id, interaction, attributes):


    def add_edge(self, source_id, target_id, interaction, attributes):
        source_node = self.get_node_by_id(source_id)
        target_node = self.get_node_by_id(target_id)
        self.max_edge_id += self.max_edge_id
        edge_id = self.max_edge_id
        edge = EdgeCX(edge_id)
        edge.s = source_node
        edge.t = target_node
        edge.i = interaction
        edge.attributes = attributes
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
            node = self.add_node(node_id)
        return node

    def get_edge_by_id(self, edge_id):
        edge = self.id_edge_map.get(edge_id)
        if not edge:
            edge = EdgeCX(edge_id)
            self.id_edge_map[edge_id] = edge
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
        stream.write("TODO: output method for network")