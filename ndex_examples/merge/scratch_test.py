import ndex.client as nc
import ndex_examples.merge.bindingdb_merger as merger

ndex = nc.Ndex("http://dev.ndexbio.org", "test", "ndex")
ndex.set_debug_mode(True)

provA = ndex.get_provenance('523b0ecb-2007-11e5-8169-0aa4c1de39d1')
provB = ndex.get_provenance('52456f0c-2007-11e5-8169-0aa4c1de39d1')
provC = ndex.get_provenance('524f0bfd-2007-11e5-8169-0aa4c1de39d1')

merged_prov = merger.merge_provenance(provA, provB, provC)

ndex.set_provenance('524f0bfd-2007-11e5-8169-0aa4c1de39d1', merged_prov)

