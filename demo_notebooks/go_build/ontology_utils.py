import csv

from ndex.networkn import NdexGraph


# Each row in the gene annotation file maps a gene to a GO term, plus data about the gene and the source of the annotation
#
# UniProtKB
# O14511
# NRG2
#
# GO:0007165
# PMID:9168114
# TAS
#
# P
# Pro-neuregulin-2, membrane-bound isoform
# NRG2_HUMAN|NTAK
# protein
# NCBITaxon:9606
# 20030904
# PINC

def create_term_map(annotation_file_path):
    header = ["id_type",
              "id",
              "gene_symbol",
              "x",
              "go_id",
              "reference_id",
              "evidence_type"]

    term_map = {}

    # Each row in the gene annotation file maps a gene to a GO term
    # plus data about the gene and the source of the annotation

    # We therefore first populate an inverse map: for each GO term id, a set of gene symbols
    # (this could be more sophisticated in the future, but first we will do the minimum work)

    gene_symbol_set = set()

    with open(annotation_file_path, 'rU') as tsvfile:
        reader = csv.DictReader(filter(lambda row: row[0] != '#', tsvfile), dialect='excel-tab', fieldnames=header)
        for row in reader:
            gene_symbol = row.get("gene_symbol")
            term_id = row.get("go_id")
           # print str(gene_symbol) + str(term_id)
            if gene_symbol and term_id:
                term_attributes = term_map.get(term_id)

                if not term_attributes:
                    term_attributes = {"my_genes": [], "term_ids": [term_id]}
                    term_map[term_id] = term_attributes

                my_genes = term_attributes["my_genes"]
                my_genes.append(gene_symbol)


    # remove duplicates
    for term_id in term_map:
        attributes = term_map[term_id]
        attributes["my_genes"] = list(set(attributes["my_genes"]))


    # for each term-genes annotation, we add that annotation to the
    # corresponding term in the ontology.

    # Note that in the case that the annotations
    # may only cover a subset of the ontology.

    # for term_id, genes in term_id_to_genes_map:
    #     term = ontology.get(term_id)
    #     if not term:
    #         print "term id not found in ontology: " + str(term_id)
    #     else:
    #         term["genes"] = genes

    print str(len(term_map)) + " terms annotated in term_map"
    return term_map


def propagate_ontology_under_root(ontology, root_term_id, term_map):
    root = ontology[root_term_id]
    if not root:
        raise "cannot find root term by id " + str(root_term_id)
    genes, term_ids = propagate(root, term_map)
    print str(len(term_ids)) + " term ids under root " + str(root_term_id)
    print str(len(genes)) + " genes annotated to terms"


def propagate(term, term_map):
    my_genes = []
    term_attributes = {}
    if term.id in term_map:
        term_attributes = term_map[term.id]
        if len(term.children) is 0:
            # leaf node
            term_attributes["genes"] = term_attributes["my_genes"]
            return check_returned_values(term_attributes["genes"], term_attributes["term_ids"])

        if "p" in term_attributes:
            # Non-leaf node that has already been propagated
            # just return the genes and term_ids attributes already computed
            return check_returned_values(term_attributes["genes"], term_attributes["term_ids"])
    # leaf node that is not annotated:
    # return empty genes and term_ids
    # NOT used in the network that we will later create from the ontology
    if len(term.children) is 0:
        return check_returned_values([], [])

    # Now handling the cases where there ARE children to be examined
    # AND the term has not already been propagated
    all_propagated_genes = []
    all_propagated_term_ids = []
    child_term_ids = []

    for child in term.children:
        propagated_genes, propagated_term_ids = propagate(child, term_map)
        all_propagated_term_ids = all_propagated_term_ids + propagated_term_ids
        all_propagated_genes = all_propagated_genes + propagated_genes

    if len(all_propagated_genes) is 0:
        # no annotated terms below,
        if "my_genes" in term_attributes:
            # this term has annotations, even if its children do not
            term_attributes["genes"] = term_attributes["my_genes"]
            term_attributes["p"] = True
            return check_returned_values(term_attributes["genes"], term_attributes["term_ids"])
        else:
            # no annotations, mark it as propagated but don't include its term id in its attributes
            # this enables the network creation code to skip this term and not add a node to the network
            term_attributes = {"genes": [], "term_ids": [], "p": True}
            term_map[term.id] = term_attributes
            return check_returned_values(term_attributes["genes"], term_attributes["term_ids"])

    # there ARE annotated genes in terms below
    # AND the term is not marked as propagated
    if "term_ids" in "term_attributes":
        # add the propagated term ids and genes to existing map entry
        term_attributes["term_ids"]= list(set(all_propagated_term_ids + term_attributes["term_ids"]))
        term_attributes["genes"] = list(set(all_propagated_genes + term_attributes["my_genes"]))
        term_attributes["p"] = True
        return check_returned_values(term_attributes["genes"], term_attributes["term_ids"])
    else:
        # add a new map entry with propagated term ids + term.id and propagated genes
        ret_term_ids = list(set(all_propagated_term_ids + [term.id]))
        ret_genes = list(set(all_propagated_genes))
        term_attributes["genes"] = ret_genes
        term_attributes["term_ids"] = ret_term_ids
        term_attributes["p"] = True
        term_map[term.id] = term_attributes
        return check_returned_values(term_attributes["genes"], term_attributes["term_ids"])

def check_returned_values(genes, term_ids):
    if type(genes) is not list:
        raise "propagate failed - no genes"
    if type(term_ids) is not list:
        raise "propagate failed - no term ids"
    return genes, term_ids

def ontology2NdexGraph(ontology, term_map, root_term_id):

    root = ontology[root_term_id]
    if not root:
        raise "cannot find root term by id " + str(root_term_id)

    term_id_to_node_id_map = {}
    G = NdexGraph()

    print "adding nodes"
    # create all the nodes under root in ontology and add attributes, if any
    add_nodes(root, G, term_map, term_id_to_node_id_map)

    print "added " + str(len(term_id_to_node_id_map)) + " nodes"
    print "network now has  " + str(len(G.nodes())) + " nodes"

    print "adding edges"
    add_edges(root, G, term_id_to_node_id_map)
    print "network now has  " + str(len(G.edges())) + " edges"
    return G

def add_nodes(parent_term, network, term_map, term_id_to_node_id_map):

    # check to see if this term has already been added to the id->node_id map
    if parent_term.id in term_id_to_node_id_map:
        return

    # only traverse nodes in the term_map
    if parent_term.id not in term_map:
        return

    attributes = term_map[parent_term.id]

    # dont include this term if it has no propagated or directly annotated genes
    if "genes" not in attributes or len(attributes["genes"]) is 0:
        return

    att_dict = {}
    att_dict["represents"] = parent_term.id
    # prune empty lists from attributes
    for att in attributes:
        val = attributes[att]
        if not (type(val) is list and len(val) is 0):
            att_dict[att] = val
    node_id = network.add_new_node(parent_term.name, att_dict)
    term_id_to_node_id_map[parent_term.id] = node_id

    for child_term in parent_term.children:
        add_nodes(child_term, network, term_map, term_id_to_node_id_map)

def add_edges(parent_term, network, term_id_to_node_id_map):
    if parent_term.id in term_id_to_node_id_map:
        parent_node_id = term_id_to_node_id_map.get(parent_term.id)
        for child_term in parent_term.children:
            if child_term.id in term_id_to_node_id_map:
                child_node_id = term_id_to_node_id_map.get(child_term.id)
                if child_node_id == parent_node_id:
                    print "self loop : " + parent_term.name
                else:
                    edge_count = network.number_of_edges(child_node_id, parent_node_id)
                    if edge_count is 0:
                        network.add_edge_between(child_node_id, parent_node_id, "hasParent")
                        # print child_term.name + " -> " + parent_term.name
                    add_edges(child_term, network, term_id_to_node_id_map)
