        
import inquirer
import subprocess
import os

from rdflib.plugins.sparql import prepareQuery

from ..auxiliar import argsConfig
from .. import dataControl
from .. import genealogia



def unclesauntsQres(individual):
      
    """
    Returns a SPARQL query as a string to find all aunts/uncles of a given individual in an RDF graph using the family ontology.
    
    Parameters:
    individual (str): The name of the individual to find aunts/uncles for.
    
    Returns:
    str: A SPARQL query string.
    """

    return f"""PREFIX family: <http://example.org/family#>

SELECT DISTINCT ?auntuncle WHERE {{
  ?parent family:hasChild family:{individual} .
  ?grandparent family:hasChild ?parent .
  ?grandparent family:hasChild ?auntuncle .
  FILTER(?auntuncle != family:{individual})
  FILTER(?auntuncle != ?parent)
}}"""


def grandparentsQres(individual):
      
    """
    Returns a SPARQL query as a string to find all grandparents of a given individual in an RDF graph using the family ontology.
    
    Parameters:
    individual (str): The name of the individual to find grandparents for.
    
    Returns:
    str: A SPARQL query string.
    """

    return f"""
PREFIX family: <http://example.org/family#>

SELECT ?grandparent WHERE {{
  family:{individual} family:hasParent ?parent .
  ?parent family:hasParent ?grandparent .
  ?grandparent a family:Person .
}}

"""

def parentsQres(individual):
    """
    Returns a SPARQL query as a string to find all parents of a given individual in an RDF graph using the family ontology.
    
    Parameters:
    individual (str): The name of the individual to find parents for.
    
    Returns:
    str: A SPARQL query string.
    """

    return f"""
PREFIX family: <http://example.org/family#>

SELECT ?parent WHERE {{
  family:{individual} family:hasParent ?parent .
  ?parent a family:Person .
}}
"""


def childrenQres(individual):
    """
    Returns a SPARQL query as a string to find all children of a given individual in an RDF graph using the family ontology.
    
    Parameters:
    individual (str): The name of the individual to find children for.
    
    Returns:
    str: A SPARQL query string.
    """

    return f"""
    PREFIX family: <http://example.org/family#>

SELECT DISTINCT ?child
WHERE {{
  ?child family:hasParent family:{individual} .
}}
"""



def siblingsQres(individual):
    
    """
    Returns a SPARQL query as a string to find all siblings of a given individual in an RDF graph using the family ontology.
    
    Parameters:
    individual (str): The name of the individual to find siblings for.
    
    Returns:
    str: A SPARQL query string.
    """

    return f"""
    PREFIX family: <http://example.org/family#>

SELECT DISTINCT ?sibling
WHERE {{
  
  family:{individual} family:hasParent ?parent .
  

  ?sibling family:hasParent ?parent .
  
  FILTER (?sibling != family:{individual})
}}
"""


def gp_folderPath_Qres(individual):
    """
    Returns a SPARQL query that retrieves the folders of the grandparents of an individual in a family RDF graph.
    
    Args:
        individual (str): The name of the individual whose grandparents' folders should be retrieved.
        
    Returns:
        str: A string representing the constructed SPARQL query.
    """


    return f"""
PREFIX family: <http://example.org/family#>

SELECT ?folder
WHERE {{
  ?person family:hasChild family:{individual} .
  ?parent family:hasChild ?person .
  ?parent family:hasFolderPath ?folder .
}}

"""


def parents_folderPath_Qres(individual):
    """
    Returns a SPARQL query that retrieves the folders of the parents of an individual in a family RDF graph.

    Parameters:
        individual (str): The name of the individual whose parents' folders should be retrieved.

    Returns:
        str: A string representing the constructed SPARQL query.
    """
    return f"""
    PREFIX family: <http://example.org/family#>

    SELECT ?folder
    WHERE {{
        family:{individual} family:hasParent ?parent .
        ?parent family:hasFolderPath ?folder .
    }}
    """


def children_folderPath_Qres(individual):
    """
    Returns a SPARQL query that retrieves the folders of the children of an individual in a family RDF graph.

    Parameters:
        individual (str): The name of the individual whose children's folders should be retrieved.

    Returns:
        str: A string representing the constructed SPARQL query.
    """
    return f"""
    PREFIX family: <http://example.org/family#>

    SELECT ?folder
    WHERE {{
        ?child family:hasParent family:{individual} .
        ?child family:hasFolderPath ?folder .
    }}
    """





def siblings_folderPath_Qres(individual):
    """
    Returns a SPARQL query that retrieves the folders of the siblings of an individual in a family RDF graph.

    Parameters:
        individual (str): The name of the individual whose siblings' folders should be retrieved.

    Returns:
        str: A string representing the constructed SPARQL query.
    """
    return f"""
    PREFIX family: <http://example.org/family#>

    SELECT DISTINCT ?folder
    WHERE {{
        ?sibling family:hasParent ?parent .
        ?sibling family:hasFolderPath ?folder .
        FILTER (?sibling != family:{individual})
        FILTER EXISTS {{
            family:{individual} family:hasParent ?parent .
        }}
    }}
    """


def individual_folderPath_Qres(individual):
    """
    Returns a SPARQL query that retrieves the folder path of a specific individual in a family RDF graph.

    Parameters:
        individual (str): The name of the individual whose folder path should be retrieved.

    Returns:
        str: A string representing the constructed SPARQL query.
    """
    return f"""
    PREFIX family: <http://example.org/family#>

    SELECT ?folderPath
    WHERE {{
        family:{individual} family:hasFolderPath ?folderPath .
    }}
    """



def handle_namespace(namespace):
    return namespace.split('#')[1]



def execute_sparql_query(query_string, graph):
    query = prepareQuery(query_string)
    result = graph.query(query)
    return result

def apply_querie(function_type,individual,g):
    res = []
    if isinstance(individual,str): 
        sparql_qry = function_type(individual)
        result = execute_sparql_query(sparql_qry,g)
        if not result:
            res = []
    
        else:
            for row in result:
                row[0].toPython()
                res.append(handle_namespace(row[0].toPython()))
    
        return res


def compose_header(initial,arguments):
    header = "The "
    for (elem,_) in arguments[:-1]:
        if elem == 'unclesaunts':
            header += "uncles and aunts of the "
        else:
            header += elem + " of the "
    elem,_ = arguments[-1]
    if elem == 'unclesaunts':
        header += f"uncles and aunts of {initial}:"
    else:
        header += elem + f" of {initial}:"
    return header  


def handle_queries(type, individual, g):
    try:
        if type == 'siblings':
            return apply_querie(siblingsQres, individual, g)
        elif type == 'grandparents':
            return apply_querie(grandparentsQres, individual, g)
        elif type == 'parents':
            return apply_querie(parentsQres, individual, g)
        elif type == 'unclesaunts':
            return apply_querie(unclesauntsQres, individual, g)
        elif type == 'children':
            return apply_querie(childrenQres, individual, g)
    except Exception as e:
        # Handle the ParseException here
        print(f"✗ Some error occurred. Individual might not exist.")
        return None

def query_composition(path,g,args):
    if hasattr(args, 'ordered_args'):
        inverted_args = args.ordered_args
    else:
        print("✗ You need to specify what flags you want. Use anbget -h for additional information.")
        exit()

    inverted_args = inverted_args[::-1]
    if args.individual[0] == ".":
        individual = os.path.basename(path)
        initial = individual.replace("-", " ")
    else:
        if args.individual[0].endswith("/"):
            args.individual[0]=args.individual[0][:-1]
        individual = args.individual[0]
        initial = args.individual[0].replace("-", " ")

    header = compose_header(initial,args.ordered_args) 
    for i, (argument, _) in enumerate(inverted_args):
        if i == len(inverted_args) - 1:
            aux = {}

            if isinstance(individual,list):
                for elem in individual:
                    aux[elem] = handle_queries(argument,elem,g)
            elif isinstance(individual,str):
                aux[individual] = handle_queries(argument,individual,g)
            
            all_empty = all(val == [] for val in aux.values())
            if all_empty:
                print("✗ Non existing info regarding this relationship(s).")
                exit()
            
            unique = set()
            message = "Results come from:\n"
            
            for person,relations in aux.items():
                for p in relations:
                    unique.add(p)
                if relations != []:
                    message += " " + person.replace("-"," ") + "\n"
        
        else:
            if isinstance(individual,list):
                aux = []
                for elem in individual:
                    aux.extend(handle_queries(argument,elem,g))
                individual = aux
            elif isinstance(individual,str):
                aux = handle_queries(argument,individual,g)
                individual = aux
    return unique,message,header


# def show_data(unique,message,header):

#     print(header)
#     for elem in unique:
#         print("*", elem.replace("-"," "))
#     print("\n",message)

from prettytable import PrettyTable

def show_data(unique, message, header):
    table = PrettyTable([header])
    for elem in unique:
        table.add_row(["* " + elem.replace("-", " ")])
    print(table)
    print("\n" + message)


def anb_search():
    cwd = os.getcwd()
    dataControl.search_anbtk()
    g = genealogia.read_onto_file('anbsafeonto.rdf')
    args = argsConfig.a_search()
    unique,message,header = query_composition(cwd,g,args)
    show_data(unique,message,header)



def folder_cd_composition(unique,g):
    possibilities = []
    for value in unique:
        sparql_qry = individual_folderPath_Qres(value)
        result = execute_sparql_query(sparql_qry,g)
        if not result:
            print("✗ Non-existing folderpath.")
        else:
            for row in result:
                possibilities.append(str(row["folderPath"].toPython()))
    return possibilities



def select_path(paths):
    folder_names = [os.path.basename(path) for path in paths]
    folder_names.append("Leave")

    questions = [
        inquirer.List('path',
                      message="Select a folder:",
                      choices=folder_names,
                      ),
    ]
    answers = inquirer.prompt(questions)
    selected_folder_name = answers['path']

    if selected_folder_name == "Leave":
        exit()

    # Get the corresponding full path for the selected folder name
    selected_path = next(path for path in paths if os.path.basename(path) == selected_folder_name)

    return selected_path


def anb_cd():
    cwd = os.getcwd()
    if not dataControl.search_anbtk():
        print("✗ You are not in an Ancestors Notebook." )
        exit()
    else:
        # dataControl.search_anbtk()
        try:
            g = genealogia.read_onto_file('anbsafeonto.rdf')
        except FileNotFoundError:
            print("No ontology was initialized.\nWas this ancestor notebook created from scratch? There doesn't seem to exist any .rdf file that defines the familiar connections.")
            exit()
        os.chdir(dataControl.get_root())
        
    args = argsConfig.a_cd()
    unique,_,_ = query_composition(cwd,g,args)
    possibilities = folder_cd_composition(unique,g)
    selected_folder = select_path(possibilities)
    selected_folder = selected_folder.split("/")[1]
    try:
        subprocess.check_call(f"cd {selected_folder} && exec $SHELL", shell=True)
    except subprocess.CalledProcessError:
            print("Some problem in finding the folder. Were any manual naming changes made to the Ancestors Notebook folder?.")
            exit()
    
    
    

        


