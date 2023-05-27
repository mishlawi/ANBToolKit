import ontology.ousia
from rdflib import Graph

def test1():
    def parse_text(input):
        """
        
        Parses the universe file and returns a dictionary of the form:
        {'name1': ['item1', 'item2', ...], 'name2': ['item1', 'item2', ...], ...}

        """
        start_index = input.rfind('---')
        if start_index == -1:
            return {}
        
        lines = input[start_index + 3:].strip().split('\n')
        result = {}
        current_category = None
        
        for line in lines:
            line = line.strip()
            if line:
                if not line.startswith('-'):
                    current_category = line
                    result[current_category] = []
                else:
                    attribute = line[1:].strip()
                    if current_category:
                        result[current_category].append(attribute)

        return result


    g = Graph()

    with open('universe.dgu') as universe:
            entities = parse_text(universe.read())
    ontology.ousia.dgu_base(entities,g)

import os
from pathlib import Path

def test2():
    def get_relative_path(path1, path2):
        relative_path = Path(path1).relative_to(path2)
        return relative_path

    path1 = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/anb-family/Ana-Sofia-Mendes/foto2.png"
    path2 = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/anb-family"

    relative_path = get_relative_path(path1, path2)
    print(relative_path)
test2()