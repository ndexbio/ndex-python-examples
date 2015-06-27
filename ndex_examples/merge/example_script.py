import ndex.client as nc
import ndex_examples.merge.bindingdb_merger as merger

devNdex = nc.Ndex("http://dev.ndexbio.org", "drh", "drh")

reactome_network = devNdex.get_complete_network('f8cddf73-1c49-11e5-8169-0aa4c1de39d1')

# large 54,877
# bindingdb_network = devNdex.get_complete_network('13f083ad-1c32-11e5-8169-0aa4c1de39d1')

# small 201
bindingdb_network = devNdex.get_complete_network('5cf1ae26-1c1d-11e5-8169-0aa4c1de39d1')

merger.merge_network(bindingdb_network, reactome_network)

reactome_network['name'] = "merge_demo 80"
reactome_network['description'] = "merge_demo 77"

localNdex = nc.Ndex("http://localhost:8080", "test", "ndex")

localNdex.save_new_network(reactome_network)