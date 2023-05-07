import sparql_queries 

import os
from rdflib import Graph

#! check tests 
#! relacao entre pastas dentro de individuos (se pasta esta pedurada no elemento, ha um about entre a pasta e o elemento) ; estas pastas terem um ficheiro metadados com info que contemple a relacao
#! add pai e filho relacoes automatica na geracao das pastas 
#! convert to gedcom
'''

genealogia == γενεαλογία 

.greek

'''


def process_family(file):
    """
    Reads the seed file and processes it to create a dictionary of family members and their relationships.

    Args:
    - file (str): The path of the seed file containing the family structure data.

    Returns:
    - family_structure (dict): A dictionary where the keys are the names of family members and the values are lists of their relatives.
    """
    
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


def populate_graph(family_tree,g):
    
    """
    Populates the RDF graph with family members and their relationships based on the given family tree data.

    Args:
    - family_tree (dict): A dictionary containing family members and their relationships.
    - g (rdflib.Graph): An RDF graph to which the family members and relationships will be added.

    Returns:
    - None
    """

    for couple, descendents in family_tree.items():
        parent1, parent2 = couple.split("+")
        ousia.add_individual(adapt_name(parent1),parent1,g)
        ousia.add_individual(adapt_name(parent2),parent2,g)
        ousia.add_hasSpouse(adapt_name(parent1),adapt_name(parent2),g)
        if descendents != []:
            for child in descendents:
                ousia.add_individual(adapt_name(child),child,g)
                ousia.add_parent_children(adapt_name(parent1),adapt_name(parent2),adapt_name(child),g)


def adapt_name(name):
    name = name.replace(" ","-")
    return name
    


def add_dates_onto(ages,g):

    del ages['total'] # might be useful to change this way, for now it works
    del ages['undiscovered']


    for individual in ages.items():
        name,dates = individual
        ousia.add_birthdate(adapt_name(name),dates['birthDate'],g)
        ousia.add_deathdate(adapt_name(name),dates['deathDate'],g)



def gen_onto_file(g,filename):
    
    with open(f"{filename}.n3", "wb") as f:
        f.write(g.serialize(format="n3").encode('u8'))
    with open(f"{filename}.rdf", "wb") as f:
        f.write(g.serialize(format="xml").encode('u8'))
    print(f"\nSuccessfully generated the ontology files.\n Info: {filename} generated.")
def read_onto_file(filename):
    g = Graph()
    g.parse(filename,format="xml")

    return g 


def defineOnto(family_structure,ages):
    
    g = ousia.ontology() # create graph
    populate_graph(family_structure,g) # add individuals and imediate relations
    add_dates_onto(ages,g) # adds born and death dates
    
    return g


def onto_folders_correspondence(file,family="anb-family"):    
    family_structure,ages = gramma.parsing(file)
    print("Successfully parsed the seed file.")
    cwd = os.getcwd()
    if not os.path.exists(family):
        os.mkdir(family)
    os.chdir(family)

    g = defineOnto(family_structure,ages)
    
    for couple,children in family_structure.items():
        
        gen_parents_folders(couple,children,g,family)
    os.chdir(cwd)
    controlsystem.version_control(family,g)
    
    return g


def gen_parents_folders(couple,children,graph,path):
 
    """
    Generates folders for the given couple and their children, and creates symbolic links
    between the folders to represent the family relationships. Also adds the
    folders to the given rdf graph.

    Args:
        couple (str): A string representing the parents of the children,
        children (List[str]): A list of strings representing the names of the children.
        graph (Graph): A rdflib graph object

    Returns:
        None
    """

    p1,p2 = couple.split("+")
    
    p1 = adapt_name(p1)
    p2 = adapt_name(p2)
       

    if not os.path.exists(f'.{p1}+{p2}'):
        os.mkdir(f'.{p1}+{p2}')

    if not os.path.exists(p1) and not p1.startswith('undiscovered'):
        gen_parental_folder_connections(p1,couple,graph,path)

    if not os.path.exists(p2) and not p2.startswith('undiscovered'):
        gen_parental_folder_connections(p2,couple,graph,path)
        
    for son in children:           
        son = adapt_name(son)     
        if not os.path.exists(son) and not son.startswith('undiscovered'):
            os.mkdir(son)
            
            # ousia.add_folder(son,os.path.relpath(son, f'.{couple}'),graph)
            relpath = os.path.join(path,son)
            ousia.add_folder(son,relpath,graph)
            os.symlink(f'../{son}',f'.{p1}+{p2}/{son}')



# here the change of abs to rel
def gen_parental_folder_connections(individual,couple,graph,path):
    os.mkdir(individual)  
    relpath = os.path.join(path,individual)
    ousia.add_folder(individual,relpath,graph)
    os.symlink(f'../.{couple}',f'{individual}/.{couple}')
 



def queriesA(individual,file):
    # must be rdf
    if file.endswith()!= 'rdf':
        raise Exception("Must be a rdf file")
    else:

        g = Graph()
        
        try:
            g.parse(file, format='xml')
            g.serialize(format='turtle')  # print the graph
        except Exception as e:
            print(e)

        graparentQres = g.query(sparql_queries.grandparentsQres(individual))
        unclesQres = g.query(sparql_queries.unclesQres(individual))
        siblingsQres = g.query(sparql_queries.siblingsQres(individual))
        gpFoldersQres = g.query(sparql_queries.gp_folderPath_Qres(individual))

        for row in graparentQres:
            print(row)

        print("\n\n")
        for row in unclesQres:
            print(row)

        print("\n\n")
        for row in siblingsQres:
            print(row)

        print("\n\n")
        for row in gpFoldersQres:
            print(row[0])



def generate_family_file(directory_name, family_file):
    
    family_structure = {}
    for root, dirs, _ in os.walk(directory_name):
        
        parents = os.path.basename(root)
        if '+' not in parents:
            continue
        # parent1, parent2 = parents.split('+')
        children = []
        for d in dirs:
            
            if '+' in d:
                continue
            children.append(d)
        # Add the family to the family structure dictionary
        family_structure[parents] = children

    # Write the family file
    with open(family_file, 'w') as f:
        for parents, children in family_structure.items():
            p1,p2 = parents.split(r"\+")
            f.write(f"{p1} ? + {p2} ?\n")
            for child in children:
                f.write(f".{child} ?")




