import os
import sparql_queries 
import rdflib

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD



#              TODO:

#              ? check n3 notation
#              ? owl
#              ? expressoes de pesquisa
#              ? gedcom 


#####################################


FAMILY = Namespace('http://example.org/family#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
ns = Namespace("http://example.org/") # to be removed


#*       classical way of defining relations . might be useful for gedcom conversion

def get_familiar_relations(name, family_tree):
    relations = {
        "parents": [],
        "children": [],
        "siblings": [],
        "spouse": [],
        "nieces": [],
        "grandparents": [],
        "cousins": [],
        "uncles" : []
    }
    
    for parent_child, children in family_tree.items():
        parents = parent_child.split("+")
        if name in parents:
            if parents[0] == name:
                if relations['spouse'] != []:
                    relations['ex-spouses'] = relations['spouse'] 
                relations['spouse'] = parents[1]            
            elif parents[1] == name:
                if relations['spouse'] != []:
                    relations['ex-spouses'] = relations['spouse'] 
                relations['spouse'] = parents[0]
            if children != []:
                relations['children'].append(children)
        if name in children:
            relations['parents'] = parents
            siblings = []
            for sibling in children:
                if sibling != name:
                    siblings.append(sibling)
            relations['siblings'] = siblings
            if (grandparents := get_familiar_relations(parents[0],family_tree)['parents']) != []:
                relations['grandparents'] = grandparents
            elif (grandparents := get_familiar_relations(parents[1],family_tree)['parents']) != []:
                relations['grandparents'] = grandparents
            if (uncles := get_familiar_relations(parents[0],family_tree)['siblings']) != []:
                relations['uncles'] = uncles
            elif (uncles := get_familiar_relations(parents[0],family_tree)['siblings']) != []:
                relations['uncles'] = uncles
            
    return relations


def get_unique_individuals(family_tree):
    individuals = [] 
    for couple, children in family_tree.items():
        parents = couple.split("+")
        individuals.extend(parents)
        individuals.extend(children)
    return list(set(individuals))

def get_relations(filename):
    family_tree = process_family(filename)
    individuals = get_unique_individuals(family_tree)
    relations = {}
    for person in individuals:
        relations[person] = get_familiar_relations(person,family_tree)

    return relations

#
#          * classical rdf; no owl
#
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
            
    return individuals, rels


def genOntoclassic(filename):
    
    family_tree = process_family(filename)

    relationships={
    'married': URIRef(ns["married"]),
    'parent': URIRef(ns["parent"]),
    'child': URIRef(ns["child"]),
    'sibling': URIRef(ns["sibling"])
    }

    g = Graph()
    g.bind("", rdflib.Namespace(ns))

    _, relations = connections(family_tree,relationships)
    for elem in relations:
        g.add(elem)
    with open("family_relationships.n3", "wb") as f:
        f.write(g.serialize(format="n3").encode('u8'))

    return g



def process_family(file):
    
    os.getcwd()
    family_structure = {}
    with open(file, 'r') as f:
        contents = f.read()
        lines = contents.splitlines()
    aux = []
    current_individual = ''
    for line in lines:
        if '+' in line:
            family_structure[line] = []
            current_individual = line
        elif line == '':
            family_structure[current_individual]  = aux
            aux = []
        else:
            aux.append(line.strip())


    return family_structure



#
#           * owl ontology
#

def defineOnto(family_tree):
    g = Graph()

    # Define namespaces
    g.bind('family', FAMILY)

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

    # has Path 
    has_path_property = FAMILY['hasFolder']
    g.add((has_path_property, RDF.type, OWL.DatatypeProperty))
    g.add((has_path_property, RDFS.label, Literal( 'has path')))
    g.add((has_path_property, RDFS.domain, person_class))
    g.add((has_path_property, RDFS.range, XSD.string))


    # inverse properties
    g.add((has_spouse_property, OWL.inverseOf, has_spouse_property))
    g.add((has_child_property, OWL.inverseOf, has_parent_property))
    g.add((has_parent_property, OWL.inverseOf, has_child_property))

    for couple, descendents in family_tree.items():
        parent1, parent2 = couple.split("+")
        individual1 = FAMILY.term(parent1)
        g.add((individual1,RDF.type,person_class))
        g.add((individual1, RDFS.label,Literal(parent1)))
        individual2 = FAMILY.term(parent2)
        g.add(( individual2, RDF.type , person_class ))
        g.add(( individual2, RDFS.label , Literal(parent2) ))
        g.add (( individual1, has_spouse_property , individual2 ))
        g.add (( individual2, has_spouse_property , individual1 ))
        if descendents != []:
            for child in descendents:
                c = FAMILY.term(child)
                g.add((c,RDF.type,person_class))
                g.add((c, RDFS.label,Literal(child)))
                g.add((individual1, has_child_property, c))
                g.add((individual2, has_child_property, c))
                g.add((c, has_parent_property, individual1))
                g.add((c, has_parent_property, individual2))

    return g




def add_folder(name, path):

    return (FAMILY[name], FAMILY['hasFolder'], Literal(path, datatype=XSD.string))


def onto_folders_correspondence(file):
    
    family_structure = process_family(file)
    cwd = os.getcwd()
    if not os.path.exists("anb-family"): # this name should be personalizable
        os.mkdir("anb-family")
    os.chdir("anb-family")

    g = defineOnto(family_structure)

    for couple,children in family_structure.items():
        if not os.path.exists(couple):
            os.mkdir(couple)
        if not os.path.exists(parent1:=couple.split('+')[0]):
            os.mkdir(parent1)    
            g.add(add_folder(parent1,os.path.abspath(parent1)))
            os.symlink(f'../{couple}',f'{parent1}/{couple}')
        if not os.path.exists(parent2:=couple.split('+')[1]):
            os.mkdir(parent2)
            g.add(add_folder(parent1,os.path.abspath(parent2)))
            os.symlink(f'../{couple}',f'{parent2}/{couple}')
        for son in children:
            if not os.path.exists(son):
                os.mkdir(son)
                g.add(add_folder(parent1,os.path.abspath(son)))
                os.symlink(f'../{son}',f'{couple}/{son}')
   
    os.chdir(cwd)
   
    return g


def gen_onto_file(g):

    with open("ontology.n3", "wb") as f:
        f.write(g.serialize(format="n3").encode('u8'))
    with open("family.rdf", "wb") as f:
        f.write(g.serialize(format="xml").encode('u8'))


def queriesA(individual):
    g = Graph()
    file = 'family.rdf'
    try:
        g.parse(file, format='xml')
        g.serialize(format='turtle')  # print the graph
    except Exception as e:
        print(e)

    graparentQres = g.query(sparql_queries.grandparentsQres(individual))
    unclesQres= g.query(sparql_queries.unclesQres(individual))
    siblingsQres = g.query(sparql_queries.siblingsQres(individual))


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
    # ft = process_family('relations.txt')
    # print(ft)
    #get_relations('relations.txt')
    g = onto_folders_correspondence('relations.txt')
    gen_onto_file(g)
    #queriesA('Silvestre')



main()



