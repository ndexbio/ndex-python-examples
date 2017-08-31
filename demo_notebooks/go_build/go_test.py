import pronto
import json

ontology = pronto.Ontology("http://purl.obolibrary.org/obo/go/go-basic.obo")

print("loaded go-basic")

biological_process = ontology["GO:0008150"]
print(biological_process.name)