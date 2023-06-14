from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD

FAMILY = Namespace('http://example.org/family#')

def add_individual(individual,OgName, graph):

    individual = FAMILY[individual]
    
    graph.add((individual,RDF.type,FAMILY['Person']))
    graph.add((individual,RDFS.label,Literal(OgName)))


def delete_individual(individual, graph):
    
    individual = FAMILY[individual]
    
    graph.remove((individual, None, None))
    graph.remove((None,None,individual))