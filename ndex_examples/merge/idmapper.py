__author__ = 'dexter'

import requests, json

#IDMAP_URL = 'http://ec2-52-34-209-69.us-west-2.compute.amazonaws.com:3000/idmapping'

#IDMAP_URL = 'http://54.200.201.85:3000'

IDMAP_URL = 'http://192.168.99.100:3000/'

def get_genes(identifiers):
    payload = {'ids':identifiers, 'idTypes': ['Symbol']}

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Cache-Control': 'no-cache',
               }
    url = IDMAP_URL + "map"
    print("url = " + url)
    print("payload = " + json.dumps(payload))
    r = requests.post(url , data=json.dumps(payload), headers=headers)
    r.raise_for_status()
    result_dictionary = r.json()
    return result_dictionary


def get_labels(identifiers):
    payload = {'ids':identifiers}

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Cache-Control': 'no-cache',
               }

    url = IDMAP_URL + "labels"
    print("url = " + url)
    print("payload = " + json.dumps(payload))
    r = requests.post(url , data=json.dumps(payload), headers=headers)
    r.raise_for_status()
    result_dictionary = r.json()
    return result_dictionary