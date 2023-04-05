import os
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS

# Create the graph object
g = Graph()

# Define the namespaces
ns = {
    "rel": URIRef("http://example.org/relationships#"),
    "owl": RDF,
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


# Define the classes
g.add((ns["rel"].Individual, RDF.type, RDFS.Class))
g.add((ns["rel"].Family, RDF.type, RDFS.Class))
g.add((ns["rel"].Parent, RDF.type, RDFS.Class))
g.add((ns["rel"].Child, RDF.type, RDFS.Class))
g.add((ns["rel"].Spouse, RDF.type, RDFS.Class))

# Define the object properties
g.add((ns["rel"].hasChild, RDF.type, RDF.Property))
g.add((ns["rel"].hasChild, RDFS.domain, ns["rel"].Parent))
g.add((ns["rel"].hasChild, RDFS.range, ns["rel"].Child))
g.add((ns["rel"].hasChild, RDF.type, RDF.Property))
g.add((ns["rel"].hasParent, RDFS.domain, ns["rel"].Child))
g.add((ns["rel"].hasParent, RDFS.range, ns["rel"].Parent))
g.add((ns["rel"].hasSpouse, RDFS.domain, ns["rel"].Individual))
g.add((ns["rel"].hasSpouse, RDFS.range, ns["rel"].Individual))

# Iterate over the directory structure and add individuals and families to the ontology
def add_individuals_to_graph(path, parent_uri=None):
    # Get the basename of the path
    basename = os.path.basename(path)

    # Create a URI for the individual
    uri = URIRef(ns["rel"] + basename)

    # Add the individual to the graph
    g.add((uri, RDF.type, ns["rel"].Individual))

    # If the individual has a parent, add a relationship to the parent
    if parent_uri:
        g.add((uri, ns["rel"].hasParent, parent_uri))
        g.add((parent_uri, ns["rel"].hasChild, uri))

    # Recursively add any children
    for name in os.listdir(path):
        child_path = os.path.join(path, name)
        if os.path.isdir(child_path):
            add_individuals_to_graph(child_path, uri)

# Call the function to add individuals to the graph starting at the root directory
root_dir = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/anb-teste"
add_individuals_to_graph(root_dir)

# Serialize the graph to a file
g.serialize(destination="relationships.rdf", format="xml")
