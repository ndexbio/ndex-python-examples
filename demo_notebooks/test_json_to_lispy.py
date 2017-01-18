__author__ = 'aarongary'

import unittest
import json
from pylisp import *
import numpy as np
from lispify import Lispify

class MyTestCase(unittest.TestCase):
    def test_something(self):

        with open("directed_path_results.json", "rb") as f:
            network = json.load(f)

            lisp_this = Lispify(network.get("forward_english"))
            print lisp_this.to_lisp()


            '''for path in network.get("forward_english"):
                for element in path:
                    if type(element) is str:
                        print "lisp str "
                        print lispify(element)
                    elif type(element) is unicode:
                        print "lisp unicode "
                        print lispify(str(element))
                    elif type(element) is dict:
                        print "lisp dict "
                        print lispify(element)
                        xxcc = ""
                    else:
                        xxcc = ""
                        '''

        self.assertEqual(True, True)

def lispify(L, indra_statement=False):
    "Convert a Python object L to a lisp representation."
    if (isinstance(L, str)
        or isinstance(L, float)
        or isinstance(L, int)):

        if(indra_statement):
            return '"%s"' % L
        else:
            return L

    elif (isinstance(L, list)
          or isinstance(L, tuple)
          or isinstance(L, np.ndarray)):
        s = []
        for element in L:
            s += [lispify(element)]
        return '(' + ' '.join(s) + ')'
    elif isinstance(L, dict):
        s = []
        for key in L:
            #print "key: " + key
            #print L[key]
            tmp_key = str(key)
            if not tmp_key.isalnum():
                tmp_key = '"%s"' % tmp_key
            if(key == "INDRA statement"):
                s += [":{0} {1}".format(tmp_key, lispify(L[key], True))]
            else:
                s += [":{0} {1}".format(tmp_key, lispify(L[key], False))]
        return '(' + ' '.join(s) + ')'
    elif isinstance(L, unicode):
        if(indra_statement):
            return '"%s"' % str(L)
        else:
            return str(L)
    else:
        return L



if __name__ == '__main__':
    unittest.main()
