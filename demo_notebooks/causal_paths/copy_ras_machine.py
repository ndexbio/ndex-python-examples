from ndex.networkn import NdexGraph
import argparse

parser = argparse.ArgumentParser(description='copy ras machine')

parser.add_argument('ndex_input', action='store')

parser.add_argument('ndex_output', action='store')
parser.add_argument('username', action='store')
parser.add_argument('password', action='store')

arg = parser.parse_args()

rm_username="test"
rm_password="test"

# Get the RAS machine
network_id='50e3dff7-133e-11e6-a039-06603eb7f303'
G = NdexGraph(server=arg.ndex_input, uuid=network_id, username=rm_username, password=rm_password)

G.upload_to(arg.ndex_server, arg.username, arg.password)