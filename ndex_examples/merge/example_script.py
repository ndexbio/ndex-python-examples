import ndex.client as nc
import ndex_examples.merge.bindingdb_merger as merger

my_ndex = nc.Ndex("http://public.ndexbio.org", "hypm", "antman")
my_ndex.set_debug_mode(True)

bindingdb_id = 'de27b0e6-2025-11e5-ab9b-06603eb7f303'
my_network_id = 'af32057b-2033-11e5-ab9b-06603eb7f303'
my_network = my_ndex.get_complete_network(my_network_id)
bindingdb_network = my_ndex.get_complete_network(bindingdb_id)

print "Node Count before merge : " + str(my_network.get('nodeCount'))
merged_network = merger.merge_network(bindingdb_network, my_network)
print "Node Count after merge : " + str(merged_network.get('nodeCount'))
ns = my_ndex.save_new_network(merged_network)
merged_network_id = ns.get('externalId')

bindingdb_provenance = my_ndex.get_provenance(bindingdb_id)
my_provenance = my_ndex.get_provenance(my_network_id)
new_network_provenance = my_ndex.get_provenance(merged_network_id)
merged_provenance = merger.merge_provenance(my_provenance, bindingdb_provenance, new_network_provenance)
my_ndex.set_provenance(merged_network_id, merged_provenance)

# reactome_network = devNdex.get_complete_network('f8cddf73-1c49-11e5-8169-0aa4c1de39d1')
# bindingdb_network = devNdex.get_complete_network('5cf1ae26-1c1d-11e5-8169-0aa4c1de39d1')
#
# merger.merge_network(bindingdb_network, reactome_network)
#
# reactome_network['name'] = "My Network"
# reactome_network['description'] = "My Network Description"
#
# reactome_id = reactome_network['externalId']
# bindingdb_id = bindingdb_network['externalId']
#
# reactome_provenance = devNdex.get_provenance(reactome_id)
# bindingdb_provenance = devNdex.get_provenance(bindingdb_id)
#
# new_network_summary = devNdex.save_new_network(reactome_network)
#
# new_network_id = new_network_summary['externalId']
#
# new_network_provenance = devNdex.get_provenance(new_network_id)
#
# merged_provenance = merger.merge_provenance(reactome_provenance, bindingdb_provenance, new_network_provenance)
#
# devNdex.set_provenance(new_network_id, merged_provenance)

