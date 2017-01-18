import argparse
from os.path import join
from ndex.networkn import NdexGraph
import ndex.client as nc
import json

parser = argparse.ArgumentParser(description='load a CX file to an NDExGraph, then upload to NDEx')

parser.add_argument('username', action='store')
parser.add_argument('password', action='store')
parser.add_argument('server', action='store')
parser.add_argument('directory', action='store')
parser.add_argument('filename', action='store')

args = parser.parse_args()

ndex = nc.Ndex(args.server, args.username, args.password)

path = join(args.directory, args.filename)

with open(path, 'rU') as cxfile:
    cx = json.load(cxfile)
    network = NdexGraph(cx)
    ndex.save_new_network(network.to_cx())
