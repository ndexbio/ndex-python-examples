__author__ = 'aarongary'

import unittest
#from qca_module import QCA_Module
#from qca import QCA
#from qca import EdgeRanking, EdgeEnum
import ndex.client as nc
#import io
import requests
from ndex.beta.path_scoring import PathScoring
import json
from os import path
from ndex.networkn import NdexGraph
from causal_paths.src.causpaths import DirectedPaths

class MyTestCase(unittest.TestCase):
    def test_something(self):
        #qca = QCA()
        #  source_names = ["CALM3"]
        #  target_names = ["NFATC2"]

        ndex_graph = NdexGraph(server="http://public.ndexbio.org", uuid="76ce8073-002a-11e6-b550-06603eb7f303")  # Ras Machine
        directedPaths = DirectedPaths()

        source_target = [
            {"id": "1234", "source": ["KSR1"], "targets": [["MARK2"], ["MARK3"], ["LIMA1"], ["STAT1"], ["Cyclin"], ["PRSS27"], ["PRKCG"], ["ITGAV"], ["ITGB3"], ["ERG"], ["EIF2AK3"]]}
        ]

        return_paths = directedPaths.findDirectedPathsBatch(ndex_graph, source_target, npaths=50)

        mystr = ""
        '''
        here = path.abspath(path.dirname(__file__))

        # Get the long description from the relevant file
        with open(path.join(here, 'rasmachine.cx')) as f:
            long_description = f.read()
        '''

        #f = io.BytesIO()
        #f.write(reference_network_cx.content)
        #f.seek(0)
        #r = requests.post(url, files={'network_cx': f})

        self.assertTrue(True)