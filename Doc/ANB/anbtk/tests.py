import ontology.ousia
from rdflib import Graph

import DSL.family.gramma

def test1():
    def parse_text(input):
        start_index = input.find('---')
        if start_index == -1:
            return {}

        lines = input[start_index + 3:].strip().split('\n')
        result = {}

        for line in lines:
            line = line.strip()
            if line and not line.startswith('-'):
                category_name, _, abbreviation = line.partition('(')
                category_name = category_name.strip()
                abbreviation = abbreviation.rstrip(')')
                if abbreviation.strip():
                    result[category_name] = abbreviation.strip()

        return result



    g = Graph()

    with open('universe.dgu') as universe:
        entities = parse_text(universe.read())
        print(entities)
    #ontology.ousia.dgu_base(entities,g)

import os
from pathlib import Path

def test2():
    def get_relative_path(path1, path2):
        relative_path = Path(path1).relative_to(path2)
        return relative_path

    path1 = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/fams/anb-family/Vitalina-Moreira-Martins"
    path2 = "anb-family/Vitalina-Moreira-Martins/h4-Pobreza.tex"

    relative_path = get_relative_path(path2, path1)
    print(relative_path)


dict1 = {'Pedro Esteves Cardoso+Luciana Abreu Loureiro': ['undiscovered_3', 'José Augusto Santos', 'Ana Sofia Mendes', 'Pedro Esteves']}
dict2 = {'total': 6, 'undiscovered': 1, 'Pedro Esteves Cardoso': {'birthDate': '?', 'deathDate': '?', 'id': 1}, 'Luciana Abreu Loureiro': {'birthDate': '1932', 'deathDate': '?', 'id': 2}, 'undiscovered_3': {'birthDate': '?', 'deathDate': '?'}, 'José Augusto Santos': {'birthDate': '1947', 'deathDate': '2019', 'id': 4}, 'Ana Sofia Mendes': {'birthDate': '1950', 'deathDate': '-', 'id': 5}, 'Pedro Esteves': {'birthDate': '?', 'deathDate': '?', 'id': 6}}

def dict_to_file(ids,block):
    del ids['total']
    del ids['undiscovered']
    string = ''
    for key,value in block.items():
        p1,p2 = key.split("+")
        if p1.startswith("undiscovered"):
            p1 = p1.split("_")[1]
        if p2.startswith("undiscovered"):
            p2 = p2.split("_")[1]
        bd_p1 = ids[p1]["birthDate"]
        dd_p1 = ids[p1]["deathDate"]
        bd_p2 = ids[p2]["birthDate"]
        dd_p2 = ids[p2]["deathDate"]
        if bd_p1 == dd_p1 and bd_p1 == "?":
            string = string + f"{p1} ? +"
        else:
            string = string + f"{p1} ({bd_p1} {dd_p1}) +"
        if bd_p2 == dd_p2 and bd_p2 == "?":
            string = string + f" {p2} ?\n"
        else:
            string = string + f" {p2} ({bd_p2} {dd_p2})\n"
        for child in value:
            if child.startswith("undiscovered"):
                string = string + '.#' + child.split("_")[1] + '\n'
            else:
                bd = ids[child]["birthDate"]
                dd = ids[child]["deathDate"]
                if bd == dd and bd == "?":
                    string = string + f".{child} ?\n"
                else:
                    string = string + f".{child} ({bd} {dd})\n"
    string += '\n'
    return string

#print(dict_to_file(dict2,dict1))
a = """Ricardo Esteves Cardoso ? + Luciana Abreu Loureiro (1932 ?)
.#3
.José Augusto Santos (1947 2019)
.Ana Sofia Mendes (1950 -)
.Pedro Esteves ?

José Augusto Santos (1947 2019)+ Susana Rodrigues  (1956 -)
.Rui Miguel Santos Ferreira (1970 -)
.Silvana Isabel Santos Ferreira (1973 -)

Rui Miguel Santos Ferreira (1970 -) + Mariana da Costa Almeida (1972 -)
.Silvestre Tiago Almeida Santos Ferreira (1995 -)
.Rodrigo Diogo Almeida Santos Ferreira (1998 -)

"""

b= """Luis Pedro Esteves Cardoso ? + Luciana Abreu Loureiro ?
.#3
.José Augusto Santos (1947 2019)
.Ana Sofia Mendes (1950 -)
.Pedro Esteves ?
"""

c= """
Ricardo Esteves Cardoso ? + Luciana Abreu Loureiro (1932 ?)
.#3
.José Augusto Santos (1947 2019)
.Ana Sofia Mendes (1950 -)
.Pedro Esteves ?
"""
# f_t,x = DSL.family.gramma.check_parsing(a)
# print(f_t)

def parents_kids(block):
    status = {'parents': [], 'children': []}
    for couple, kids in block.items():
        if status['parents'] == []:
            status['parents'] = couple.split("+")
        else:
            for elem in couple.split("+"):
                if elem not in status['parents']:
                    status['parents'].append(elem)
        status['children'] += kids

    return status


##############################3

dict1 = {
        'Pedro Esteves Cardoso+Luciana Abreu Loureiro': ['undiscovered_3', 'José Augusto Santos', 'Ana Sofia Mendes', 'Pedro Esteves']
    }
def print_family_tree(dict1):
    

    for key, value in dict1.items():
        print_family_member(key, value, "")

def print_family_member(parents, children, prefix):
    if "+" not in parents:
        print(prefix + parents)
        return

    parents = parents.split("+")
    father = parents[0]
    mother = parents[1]
    
    print(prefix + father + " ─┬─ " + mother)
    
    for i, child in enumerate(children):
        if i == len(children) - 1:
            new_prefix = prefix + "   "
            sub_prefix = prefix + "│  "
        else:
            new_prefix = prefix + "│  "
            sub_prefix = prefix + "│  "
        
        if child.startswith('undiscovered'):
            print(prefix + new_prefix + "└─" + child)
        else:
            print(prefix + new_prefix + "├─" + child)
        
        print_family_member(child, [], sub_prefix)

print_family_tree(dict1)