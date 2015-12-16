import merge
import json
from os import listdir, makedirs, path
from os.path import isfile, isdir, join, abspath, dirname, exists, basename, splitext

m = merge.MergeST()

parent_dir = dirname(abspath(__file__))

noi_file = join(parent_dir, "network_of_interest.cx")
network_c_file = join(parent_dir, "network_c.cx")
merged_file = ""
with open(noi_file, 'rb') as target:
    m.add_target(target)
    with open(network_c_file, 'rb') as source:
        m.add_source(source)
        m.do_merge()
        with open(merged_file, 'wb') as output:
            m.emit_cx(merged_file)





