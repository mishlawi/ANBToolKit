from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

# Define namespaces for the ontology
FAMILY = Namespace("http://example.com/family#")

# Create a new RDF graph
graph = Graph()

# Define classes
graph.add((FAMILY.Person, RDF.type, RDFS.Class))
graph.add((FAMILY.Child, RDF.type, RDFS.Class))
graph.add((FAMILY.Parent, RDF.type, RDFS.Class))
graph.add((FAMILY.Grandparent, RDF.type, RDFS.Class))
graph.add((FAMILY.Grandmother, RDF.type, RDFS.Class))
graph.add((FAMILY.Grandfather, RDF.type, RDFS.Class))
graph.add((FAMILY.Grandchild, RDF.type, RDFS.Class))
graph.add((FAMILY.Granddaughter, RDF.type, RDFS.Class))
graph.add((FAMILY.Grandson, RDF.type, RDFS.Class))

# Define object properties
graph.add((FAMILY.hasChild, RDF.type, RDF.Property))
graph.add((FAMILY.hasChild, RDFS.domain, FAMILY.Parent))
graph.add((FAMILY.hasChild, RDFS.range, FAMILY.Child))

graph.add((FAMILY.hasParent, RDF.type, RDF.Property))
graph.add((FAMILY.hasParent, RDFS.domain, FAMILY.Child))
graph.add((FAMILY.hasParent, RDFS.range, FAMILY.Parent))

graph.add((FAMILY.hasSpouse, RDF.type, RDF.Property))
graph.add((FAMILY.hasSpouse, RDFS.domain, FAMILY.Person))
graph.add((FAMILY.hasSpouse, RDFS.range, FAMILY.Person))
graph.add((FAMILY.hasSpouse, RDF.type, RDF.FunctionalProperty))

graph.add((FAMILY.hasGrandchild, RDF.type, RDF.Property))
graph.add((FAMILY.hasGrandchild, RDFS.domain, FAMILY.Grandparent))
graph.add((FAMILY.hasGrandchild, RDFS.range, FAMILY.Grandchild))

graph.add((FAMILY.hasGrandparent, RDF.type, RDF.Property))
graph.add((FAMILY.hasGrandparent, RDFS.domain, FAMILY.Grandchild))
graph.add((FAMILY.hasGrandparent, RDFS.range, FAMILY.Grandparent))

graph.add((FAMILY.hasGrandson, RDF.type, RDF.Property))
graph.add((FAMILY.hasGrandson, RDFS.domain, FAMILY.Grandparent))
graph.add((FAMILY.hasGrandson, RDFS.range, FAMILY.Grandson))

graph.add((FAMILY.hasGranddaughter, RDF.type, RDF.Property))
graph.add((FAMILY.hasGranddaughter, RDFS.domain, FAMILY.Grandparent))
graph.add((FAMILY.hasGranddaughter, RDFS.range, FAMILY.Granddaughter))

graph.add((FAMILY.hasGrandmother, RDF.type, RDF.Property))
graph.add((FAMILY.hasGrandmother, RDFS.domain, FAMILY.Grandchild))
graph.add((FAMILY.hasGrandmother, RDFS.range, FAMILY.Grandmother))

graph.add((FAMILY.hasGrandfather, RDF.type, RDF.Property))
graph.add((FAMILY.hasGrandfather, RDFS.domain, FAMILY.Grandchild))
graph.add((FAMILY.hasGrandfather, RDFS.range, FAMILY.Grandfather))
