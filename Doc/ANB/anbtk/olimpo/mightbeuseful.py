
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
