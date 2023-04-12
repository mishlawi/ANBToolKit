import os

from rdflib import Namespace
import onto

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
    print(couples)
    return couples


def gen_structure(file):
    print("alskjgalksjg")
    FAMILY = Namespace('http://example.org/family#')

    ft = process_family(file)

    if not os.path.exists("anb-family"):
        os.mkdir("anb-family")
    os.chdir("anb-family")
    g = onto.defineOnto(ft)
    for couple,children in ft.items():
        if not os.path.exists(couple):
            os.mkdir(couple)
        if not os.path.exists(p1:=couple.split('+')[0]):
            os.mkdir(p1)    
            g.add(onto.addFolder(FAMILY,p1,os.path.abspath(p1)))
            os.symlink(f'../{couple}',f'{p1}/{couple}')
        if not os.path.exists(p2:=couple.split('+')[1]):
            os.mkdir(p2)
            g.add(onto.addFolder(FAMILY,p1,os.path.abspath(p2)))
            os.symlink(f'../{couple}',f'{p2}/{couple}')
        for filho in children:
            if not os.path.exists(filho):
                os.mkdir(filho)
                g.add(onto.addFolder(FAMILY,p1,os.path.abspath(filho)))
                os.symlink(f'../{filho}',f'{couple}/{filho}')
    
    return g


###### classical way of defining relations

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


g = gen_structure('relations.txt')
print(g)
print("here")
with open("ontology.n3", "wb") as f:
        f.write(g.serialize(format="n3").encode('u8'))


