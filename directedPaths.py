__author__ = 'aarongary'

__author__ = 'decarlin'

import sys
import logging
import json
import argparse
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

from ndex.networkn import NdexGraph
from causal_paths.src.causpaths import DirectedPaths

parser = argparse.ArgumentParser(description='run the enrichment server')

parser.add_argument('-n','--networkid', default='1234', help='network id from public.ndex.org')
parser.add_argument('-s','--sourcenames', default='MEK', help='String of source nodes')
parser.add_argument('-t','--targetnames', default='MAP2K2', help='String of target nodes')
parser.add_argument('-p','--styletemplate', default='4321', help='network id of style template')

args = parser.parse_args()

def networkNToCX(networkN):
    """Converts networkN into CX terms"""
    return networkN.to_cx()

def main():
    """Accepts a single input, CX as a string, and outputs CX as a string"""
    logging.basicConfig(level=logging.INFO)
    print args.networkid
    print args.sourcenames
    print args.targetnames
    print args.styletemplate

    logging.info('Writing reply...')
    #print(json.dumps(cx))
    return "success"