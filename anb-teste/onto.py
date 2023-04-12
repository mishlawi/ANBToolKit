import os
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL

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
# def genOnto(filename):
    
#     ft = process_family(filename)

#     relationships={
#     'married': URIRef(ns["married"]),
#     'parent': URIRef(ns["parent"]),
#     'child': URIRef(ns["child"]),
#     'sibling': URIRef(ns["sibling"])
#     }

#     g = Graph()
#     g.bind("", rdflib.Namespace(ns))

#     _, relations = connections(ft,relationships)
#     for elem in relations:
#         g.add(elem)
#     with open("family_relationships.n3", "wb") as f:
#         f.write(g.serialize(format="n3").encode('u8'))

#     return g


def genOnto(filename):
    ft = ft = process_family(filename)
    g =  defineOnto(ft)
    with open("ontology.n3", "wb") as f:
        f.write(g.serialize(format="n3").encode('u8'))
    with open("family.rdf", "wb") as f:
        f.write(g.serialize(format="xml").encode('u8'))


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

    # has sibling
    has_sibling_property = FAMILY['hassibling']
    g.add((has_sibling_property, RDF.type, OWL.ObjectProperty))
    g.add((has_sibling_property, RDFS.label,Literal( 'has sibling')))
    g.add((has_sibling_property, RDFS.domain, person_class))
    g.add((has_sibling_property, RDFS.range, person_class))

    g.add((has_sibling_property, OWL.inverseOf, has_sibling_property))
    g.add((has_spouse_property, OWL.inverseOf, has_spouse_property))
    g.add((has_child_property, OWL.inverseOf, has_parent_property))
    g.add((has_parent_property, OWL.inverseOf, has_child_property))

    for couple, descendents in ft.items():
        p1, p2 = couple.split("+")
        i1 = FAMILY.term(p1)
        g.add((i1,RDF.type,person_class))
        g.add((i1, RDFS.label,Literal( p1)))
        i2 = FAMILY.term(p2)
        g.add((i2,RDF.type,person_class))
        g.add((i2, RDFS.label,Literal( p2)))
        g.add((i1,has_spouse_property,i2))
        g.add((i2,has_spouse_property,i1))
        if descendents != []:
            siblings = []
            for child in descendents:
                c = FAMILY.term(child)
                g.add((c,RDF.type,person_class))
                g.add((c, RDFS.label,Literal( child)))
                g.add((i1, has_child_property, c))
                g.add((i2, has_child_property, c))
            for s in siblings:
                aux = siblings.copy()
                aux.remove(s)
                for bro in aux: # todo: check if the derivation works
                    g.add((s,has_sibling_property,bro))

    return g


def queries():
    g = Graph()
    file = 'family.rdf'
    try:
        g.parse(file, format='xml')
        print(g.serialize(format='turtle'))  # print the graph
    except Exception as e:
        print(e)
    qres = g.query('''
    PREFIX family: <http://example.org/family#>
    SELECT ?grandparent
    WHERE {
        ?individual family:hasParent ?parent .
        ?parent family:hasParent ?grandparent .
        FILTER (?individual = family:Silvestre)
    }
''')
    print(qres)
    for row in qres:
        print(row)




def main():

    #print( process_family('relations.txt'))
    #ft = process_family('relations.txt')
    #print(dict_to_gedcom(ft))
    #get_relations('relations.txt')
    genOnto('relations.txt')
    queries()







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
    for parent_child, children in family_tree.items():
        parents = parent_child.split("+")
        individuals.extend(parents)
        individuals.extend(children)
    return list(set(individuals))

def get_relations(filename):
    family_tree = process_family(filename)
    individuals = get_unique_individuals(family_tree)
    connections = {}
    for person in individuals:
        connections[person] = get_familiar_relations(person,family_tree)

    print(len(connections))
    print(connections)
    return connections





main()

#for elem in individuals






