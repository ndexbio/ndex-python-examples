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

# Get CX for target, place fragments in output_fragments
# Gather nodes and identifiers from node attributes
# normalize identifiers to genes, index nodes by genes
# Get CX from source
# Gather nodes and identifers
# normalize to genes
# for each match, put in shared nodes
# scan edges and edge attributes for shared nodes
# for each edge, get nodes and node attributes and edge attributes, add to output_fragments

class MergeST:
    def __init__(self):
        self.target_fragments = []
        self.shared_nodes = []
        self.identifier_node_map = {}
        self.output_fragments = []
        self.output_gene_node_map = {}

    def add_target(self, target_input_stream):

    def add_source(self, source_input_stream):

    def do_merge(self):

    def emit_cx(self, output_stream):

    def index_target_nodes(self):




