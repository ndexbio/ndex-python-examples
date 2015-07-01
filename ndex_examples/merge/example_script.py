import ndex.client as nc
import ndex_examples.merge.bindingdb_merger as merger

devNdex = nc.Ndex("http://dev.ndexbio.org", "drh", "drh")
devNdex.set_debug_mode(True)

reactome_network = devNdex.get_complete_network('f8cddf73-1c49-11e5-8169-0aa4c1de39d1')
bindingdb_network = devNdex.get_complete_network('5cf1ae26-1c1d-11e5-8169-0aa4c1de39d1')

merger.merge_network(bindingdb_network, reactome_network)

reactome_network['name'] = "My Network"
reactome_network['description'] = "My Network Description"

reactome_id = reactome_network['externalId']
bindingdb_id = bindingdb_network['externalId']

reactome_provenance = devNdex.get_provenance(reactome_id)
bindingdb_provenance = devNdex.get_provenance(bindingdb_id)

new_network_summary = devNdex.save_new_network(reactome_network)

new_network_id = new_network_summary['externalId']

new_network_provenance = devNdex.get_provenance(new_network_id)

merged_provenance = merger.merge_provenance(reactome_provenance, bindingdb_provenance, new_network_provenance)

devNdex.set_provenance(new_network_id, merged_provenance)