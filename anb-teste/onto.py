import os
from rdflib import Graph, Namespace, URIRef, Literal
import rdflib
from rdflib.namespace import RDF, RDFS, OWL, XSD

import sparql_queries 

def process_family(file):
    
    os.getcwd()
    couples = {}
    with open(file, 'r') as f:
        contents = f.read()
        lines = contents.splitlines()
    aux = []
    current = ''
    for line in lines:
        if '+' in line:
            couples[line] = []
            current = line
        elif line == '':
            couples[current]  = aux
            aux = []
        else:
            aux.append(line.strip())
    return couples


#! check n3 notation
#! owl
#! expressoes de pesquisa
#! gedcom 

def connections(couples, rel):
    individuals = []
    rels = []
    for couple, descendents in couples.items():
        p1, p2 = couple.split("+")
        i1 = URIRef(ns[p1])
        individuals.append(i1)
        i2 = URIRef(ns[p2])
        individuals.append(URIRef(ns[p2]))
        rels.append((i1, rel['married'], i2))
        rels.append((i2, rel['married'], i1))
        if descendents != []:
            siblings = []
            for child in descendents:
                c = URIRef(ns[child])
                siblings.append(c)
                individuals.append(c)
                rels.append((i1, rel['parent'], c))
                rels.append((i2, rel['parent'], c))
                rels.append((c, rel['child'], i1))
                rels.append((c, rel['child'], i2)) 
            for s in siblings:
                aux = siblings.copy()
                aux.remove(s)
                [rels.append((s,rel['sibling'],bro)) for bro in aux]
            
    print(rels)
    return individuals, rels


ns = Namespace("http://example.org/")

def genOntoclassic(filename):
    
    ft = process_family(filename)

    relationships={
    'married': URIRef(ns["married"]),
    'parent': URIRef(ns["parent"]),
    'child': URIRef(ns["child"]),
    'sibling': URIRef(ns["sibling"])
    }

    g = Graph()
    g.bind("", rdflib.Namespace(ns))

    _, relations = connections(ft,relationships)
    for elem in relations:
        g.add(elem)
    with open("family_relationships.n3", "wb") as f:
        f.write(g.serialize(format="n3").encode('u8'))

    return g


def genOnto(filename):
    ft = ft = process_family(filename)
    g =  defineOnto(ft)
    with open("ontology.n3", "wb") as f:
        f.write(g.serialize(format="n3").encode('u8'))
    with open("family.rdf", "wb") as f:
        f.write(g.serialize(format="xml").encode('u8'))


def addFolder(famNS, name, path):
    FAMILY = famNS
    individual = FAMILY[name]
    folder = Literal(os.path.realpath(path))
    return (individual, FAMILY['hasFolder'], folder)


def defineOnto(ft):
    g = Graph()

    # Define namespaces
    FAMILY = Namespace('http://example.org/family#')
    g.bind('family', FAMILY)
    RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
    g.bind('rdfs', RDFS)

    ont = FAMILY['family-ontology']
    g.add((ont, RDF.type, OWL.Ontology))
    g.add((ont, RDFS.label, Literal('Family Ontology')))

    family_class = FAMILY['Family']
    g.add((family_class, RDF.type, OWL.Class))
    g.add((family_class, RDFS.label, Literal('Family')))

    # Define the person class
    person_class = FAMILY['Person']
    g.add((person_class, RDF.type, OWL.Class))
    g.add((person_class, RDFS.label, Literal('Person')))

    # has parent
    has_parent_property = FAMILY['hasParent']
    g.add((has_parent_property, RDF.type, OWL.ObjectProperty))
    g.add((has_parent_property, RDFS.label,Literal( 'has parent')))
    g.add((has_parent_property, RDFS.domain, person_class))
    g.add((has_parent_property, RDFS.range, person_class))

    # has Child 
    has_child_property = FAMILY['hasChild']
    g.add((has_child_property, RDF.type, OWL.ObjectProperty))
    g.add((has_child_property, RDFS.label,Literal( 'has child')))
    g.add((has_child_property, RDFS.domain, person_class))
    g.add((has_child_property, RDFS.range, person_class))

    # has Spouse
    has_spouse_property = FAMILY['hasSpouse']
    g.add((has_spouse_property, RDF.type, OWL.ObjectProperty))
    g.add((has_spouse_property, RDFS.label,Literal( 'has spouse')))
    g.add((has_spouse_property, RDFS.domain, person_class))
    g.add((has_spouse_property, RDFS.range, person_class))

    has_folder_property = FAMILY['hasFolder']
    g.add((has_folder_property, RDF.type, OWL.DatatypeProperty))
    g.add((has_folder_property, RDFS.label, Literal('has folder')))
    g.add((has_folder_property, RDFS.domain, person_class))
    g.add((has_folder_property, RDFS.range, XSD.string))



    g.add((has_spouse_property, OWL.inverseOf, has_spouse_property))
    g.add((has_child_property, OWL.inverseOf, has_parent_property))
    g.add((has_parent_property, OWL.inverseOf, has_child_property))

    for couple, descendents in ft.items():
        p1, p2 = couple.split("+")
        i1 = FAMILY.term(p1)
        g.add((i1,RDF.type,person_class))
        g.add((i1, RDFS.label,Literal(p1)))
        i2 = FAMILY.term(p2)
        g.add((i2,RDF.type,person_class))
        g.add((i2, RDFS.label,Literal(p2)))
        g.add((i1,has_spouse_property,i2))
        g.add((i2,has_spouse_property,i1))
        if descendents != []:
            for child in descendents:
                c = FAMILY.term(child)
                g.add((c,RDF.type,person_class))
                g.add((c, RDFS.label,Literal(child)))
                g.add((i1, has_child_property, c))
                g.add((i2, has_child_property, c))
                g.add((c, has_parent_property, i1))
                g.add((c, has_parent_property, i2))

    return g


def queriesA(name):
    g = Graph()
    file = 'family.rdf'
    try:
        g.parse(file, format='xml')
        g.serialize(format='turtle')  # print the graph
    except Exception as e:
        print(e)

    

    # grandparents
    graparentQres = g.query(sparql_queries.grandparentsQres(name))
    unclesQres= g.query(sparql_queries.unclesQres(name))
    siblingsQres = g.query(sparql_queries.siblingsQres(name))


    for row in graparentQres:
        print(row)

    print("\n\n")
    for row in unclesQres:
        print(row)

    print("\n\n")
    for row in siblingsQres:
        print(row)


def main():
    #print( process_family('relations.txt'))
    ft = process_family('relations.txt')
    print(ft)
    #print(dict_to_gedcom(ft))
    #get_relations('relations.txt')

    genOnto('relations.txt')
    queriesA('Silvestre')







