# from .DSL.family import gramma
# from . import dataControl

def create_family_tree():
    # with open(f"{dataControl.find_anb()}") as anbtemp:
    #     dict_tree , ids = gramma.check_parsing(anbtemp.read())
    dict1 = {'Pedro Esteves Cardoso+Luciana Abreu Loureiro': ['undiscovered_3', 'José Augusto Santos', 'Ana Sofia Mendes', 'Pedro Esteves']}
    dict2 = {'total': 6, 'undiscovered': 1, 'Pedro Esteves Cardoso': {'birthDate': '?', 'deathDate': '?', 'id': 1}, 'Luciana Abreu Loureiro': {'birthDate': '1932', 'deathDate': '?', 'id': 2}, 'undiscovered_3': {'birthDate': '?', 'deathDate': '?'}, 'José Augusto Santos': {'birthDate': '1947', 'deathDate': '2019', 'id': 4}, 'Ana Sofia Mendes': {'birthDate': '1950', 'deathDate': '-', 'id': 5}, 'Pedro Esteves': {'birthDate': '?', 'deathDate': '?', 'id': 6}}
    for couple,children in dict1.items():

        print(couple)
        print(children)

def get_genealogical_order(couple):
    for value in dict1.values():
        for child in value:
            if couple[0] in child or couple[1] in child:
                return -1
    return 1


# Example usage
dict1 = {
    'Pedro Esteves Cardoso+Luciana Abreu Loureiro': ['undiscovered_3', 'José Augusto Santos', 'Ana Sofia Mendes', 'Pedro Esteves'],
    'Lucas + Susana': ['Pedro Esteves Cardoso', 'Ruben Dias'],
    'rica + luis' : ['Jcr'],
    'Ruben Dias + Jcr': ['Felizardo', 'Bonifácio','Lucas']
}

def get_genealogical_order(couple):
    for value in dict1.values():
        for child in value:
            if couple.split('+')[0] == child or couple.split('+')[1] == child:
                return -1
    return 1

sorted_dict = sorted(dict1.keys(), key=get_genealogical_order)

for couple in sorted_dict:
    children = dict1[couple]
    print(couple + ": " + str(children))




