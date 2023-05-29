import ontology.ousia
from rdflib import Graph

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

    path1 = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/anb-family/Ana-Sofia-Mendes/foto2.png"
    path2 = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/anb-family"

    relative_path = get_relative_path(path1, path2)
    print(relative_path)
test1()