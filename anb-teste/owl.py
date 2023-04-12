from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, OWL


g = Graph()

family = Namespace("http://example.org/family#")

g.bind("familia",family)
g.add((family.Person, RDF.type, OWL.Class))
g.add((family.Parent, RDF.type, OWL.Class))
g.add((family.Parent, RDFS.subClassOf, family.Person))
g.add((family.Child, RDF.type, OWL.Class))
g.add((family.Child, RDFS.subClassOf, family.Person))
g.add((family.Sibling, RDF.type, OWL.Class))
g.add((family.Sibling, RDFS.subClassOf, family.Person))
g.add((family.Grandparent, RDF.type, OWL.Class))
g.add((family.Grandparent, RDFS.subClassOf, family.Person))
g.add((family.Grandchild, RDF.type, OWL.Class))
g.add((family.Grandchild, RDFS.subClassOf, family.Person))
g.add((family.Uncle, RDF.type, OWL.Class))
g.add((family.Uncle, RDFS.subClassOf, family.Person))
g.add((family.Cousin, RDF.type, OWL.Class))
g.add((family.Cousin, RDFS.subClassOf, family.Person))
g.add((family.Married, RDF.type, OWL.Class))
g.add((family.Married, RDFS.subClassOf, family.Person))