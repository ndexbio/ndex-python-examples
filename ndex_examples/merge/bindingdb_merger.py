
import copy

def create_alias_node_id_map(ndex_network):
    result = {}
    for node_id in ndex_network['nodes']:
        node = ndex_network['nodes'][node_id]
        for base_term_id in node['aliases']:
            base_term = ndex_network['baseTerms'][str(base_term_id)]
            base_term_name = base_term['name']
            if base_term_name not in result:
                result[base_term_name] = []
            alias_list = result[base_term_name]
            alias_list.append(node_id)
            x = 10
        # for alias in aliases:
        # node_name = node['name']
        # if not node_name:
        #     base_term_id = unicode( node['represents'] )
        #     node_name = ndex_network['baseTerms'][base_term_id]['name']
        # if node_name:
        #     result[node_name] = node_id
    return result

def find_max_id(ndex_network):
    max = 0
    for key, value in ndex_network.items():
        if isinstance(value, dict):
            for possible_id in value:
                if possible_id.isdigit():
                    id = int(possible_id)
                    if id > max:
                        max = id
    return max

def get_next_id(ndex_network):
    net_id = unicode( ndex_network['externalId'] )
    if net_id not in get_next_id.max_id:
        get_next_id.max_id[net_id] = find_max_id(ndex_network)
    get_next_id.max_id[net_id] += 1
    return unicode( get_next_id.max_id[net_id] )
get_next_id.max_id = {}

def handle_namespace(source_network, source_object, destination_network):
    namespace_id_string = 'namespaceId'
    namespace_id = unicode( source_object[namespace_id_string] )
    if namespace_id == '-1':
        return
    if namespace_id in handle_namespace.map:
        new_namespace_id = handle_namespace.map[namespace_id]
        source_object[namespace_id_string] = int( new_namespace_id )
        return
    namespaces = source_network['namespaces']
    namespace = namespaces[namespace_id]
    n = copy.deepcopy(namespace)
    new_namespace_id = get_next_id(destination_network)
    handle_namespace.map[namespace_id] = new_namespace_id
    n['id'] = int( new_namespace_id )
    source_object[namespace_id_string] = int( new_namespace_id )
    clean_object_properties(source_network, n, destination_network)
    destination_network['namespaces'][new_namespace_id] = n
handle_namespace.map = {}


def handle_represents(source_network, source_object, destination_network):
    if 'predicateId' in source_object:
        represents_string = 'predicateId'
    else:
        represents_string = 'represents'
    term_id = unicode( source_object[represents_string] )
    if term_id in handle_represents.map:
        new_term_id = handle_represents.map[term_id]
        source_object[represents_string] = int( new_term_id )
        return
    # Does not handle represents unless it is a baseTerm for now.
    terms = source_network['baseTerms']
    term = terms[term_id]
    t = copy.deepcopy(term)
    new_term_id = get_next_id(destination_network)
    handle_represents.map[term_id] = new_term_id
    t['id'] = new_term_id
    source_object[represents_string] = new_term_id
    handle_namespace(source_network, t, destination_network)
    destination_network['baseTerms'][new_term_id] = t
handle_represents.map = {}

def add_node(source_network, source_edge, destination_network):
    subject_id = unicode( source_edge['subjectId'] )
    if subject_id in add_node.subject_id_map:
        new_subject_id = add_node.subject_id_map[subject_id]
        source_edge['subjectId'] = int( new_subject_id )
        return
    subject_node = source_network['nodes'][subject_id]
    n = copy.deepcopy(subject_node)
    new_subject_id = get_next_id(destination_network)
    add_node.subject_id_map[subject_id] = new_subject_id
    n['id'] = int( new_subject_id )
    source_edge['subjectId'] = int( new_subject_id )
    clean_object_properties(source_network, n, destination_network)
    handle_citations(source_network, n, destination_network)
    handle_represents(source_network, n, destination_network)
    destination_network['nodes'][new_subject_id] = n

add_node.subject_id_map = {}

def clean_object_properties(source_network, propertied_object, destination_network):
    properties = propertied_object['properties']
    for property in properties:
        handle_represents(source_network, property, destination_network)

def handle_citations(source_network, source_object, destination_network):
    # print json.dumps(source_network['citations'], sort_keys=True, indent=4, separators=(',', ': '))
    citation_ids = source_object['citationIds']
    new_citation_ids = []
    for id in citation_ids:
        id = unicode(id)
        if id in handle_citations.citation_map:
            new_citation_id = handle_citations.citation_map[id]
            new_citation_ids.append( int(new_citation_id) )
        # Later use citation_map. For now, assign each citation a unique ID and add it to the destination_network
        else:
            citation = source_network['citations'][id]
            new_citation_id = get_next_id(destination_network)
            # Copy citation into destination network
            citation['id'] = new_citation_id
            destination_network['citations'][new_citation_id] = citation
            new_citation_ids.append( int(new_citation_id) )
            handle_citations.citation_map[id] = new_citation_id
            # print citation
    source_object['citationIds'] = new_citation_ids
handle_citations.citation_map = {}

def merge_node_properties(source_network, source_node, destination_network, destination_node):
    source_node_id = unicode(source_node['id'])
    if source_node_id in merge_node_properties.map:
        return
    source_node_properties = source_node['properties']
    for property in source_node_properties:
        p = copy.deepcopy(property)
        handle_represents(source_network, p, destination_network)
        destination_node['properties'].append(p)
merge_node_properties.map = {}

def match(source_network, edge, destination_network):


    aliases = destination_network['aliases']


def merge_network(source_network, destination_network):

    network_alias_node_id_map = create_alias_node_id_map(destination_network)

    # print network_name_node_id_map

    for edge_id in source_network['edges']:
        edge = source_network['edges'][edge_id]
        object_id = unicode(edge['objectId'])
        object_node = source_network['nodes'][object_id]
        base_term_id = unicode( object_node['represents'] )
        source_node_name = source_network['baseTerms'][base_term_id]['name']
        if source_node_name in network_alias_node_id_map:
            for node_id in network_alias_node_id_map[source_node_name]:
                e = copy.deepcopy(edge)
                new_edge_id = unicode( get_next_id(destination_network) )
                e['id'] = new_edge_id
                e['objectId'] = node_id
                add_node(source_network, e, destination_network)
                clean_object_properties(source_network, e, destination_network)
                handle_citations(source_network, e, destination_network)
                handle_represents(source_network, e, destination_network)
                destination_network['edges'][new_edge_id] = e

                destination_node = destination_network['nodes'][node_id]
                merge_node_properties(source_network, object_node, destination_network, destination_node)

def merge_provenance(src1_prov, src2_prov, upload_prov):
    result = copy.deepcopy(upload_prov)
    result['creationEvent']['eventType'] = unicode('Demo Merge')
    inputs = []
    inputs.append(src1_prov)
    inputs.append(src2_prov)
    result['creationEvent']['inputs'] = inputs
    return result
