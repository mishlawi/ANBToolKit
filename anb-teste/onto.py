
import os

from rdflib import Graph, Namespace, URIRef

from rdflib.tools.rdf2dot import rdf2dot



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

ns = Namespace("http://example.org/")


def connections(couples, rel):
    individuals = []
    rels = []
    for couple, descendents in couples.items():
        if '*' in couple:
            couple = couple.replace('*', '')
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




from graphviz import Source

def genOnto(filename):

    ft = process_family(filename)

    relationships={
    'married': URIRef(ns["married"]),
    'parent': URIRef(ns["parent"]),
    'child': URIRef(ns["child"]),
    'sibling': URIRef(ns["sibling"]),
    'grandparent': URIRef(ns["grandparent"]),
    'grandchild': URIRef(ns["grandchild"])
}

    g = Graph()

    _, relations = connections(ft,relationships)
    for elem in relations:
        g.add(elem)
    with open("family_relationships.ttl", "wb") as f:
        f.write(g.serialize(format="ttl").encode('u8'))


 


        
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

def get_relations(family_tree):
    individuals = get_unique_individuals(family_tree)
    connections = {}
    for person in individuals:
        connections[person] = get_familiar_relations(person,family_tree)

    print(len(connections))
    print(connections)
    return connections




#genOnto('relations.txt')

ft = process_family('relations.txt')
get_relations(ft)    




#for elem in individuals






