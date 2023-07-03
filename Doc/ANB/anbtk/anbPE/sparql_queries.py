from .. import genealogia
from .. import dataControl
from ..auxiliar import argsConfig
from rdflib.plugins.sparql import prepareQuery
import os


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

def handle_namespace(namespace):
    return namespace.split('#')[1]


def apply_querie(function_type,individual,g,type):
    res = []
    if isinstance(individual,str): 
        sparql_qry = function_type(individual)
        result = execute_sparql_query(sparql_qry,g)
        if not result:
            res = []
            # pass
        else:
            for row in result:
                row[0].toPython()
                res.append(handle_namespace(row[0].toPython()))
    
        return res
    # elif isinstance(individual,list):
    #     for elem in individual:
    #         res.extend(handle_queries(type,elem,g))
    # return res



def handle_queries(type, individual, g):
    if type == 'siblings':
        return apply_querie(siblingsQres, individual, g, type)
    elif type == 'grandparents':
        return apply_querie(grandparentsQres, individual, g, type)
    elif type == 'parents':
        return apply_querie(parentsQres, individual, g, type)
    elif type == 'unclesaunts':
        return apply_querie(unclesauntsQres, individual, g, type)
    elif type == 'children':
        return apply_querie(childrenQres, individual, g, type)

            

def query_composition(path,g):
    args = argsConfig.a_foldercd()
    inverted_args = args.ordered_args
    inverted_args = inverted_args[::-1]
    # initial = individual.replace("-"," ")
    if args.individual[0] == ".":
        individual = os.path.basename(path)
        print(individual)
        initial = individual.replace("-", " ")
    else:
        initial = args.individual[0].replace("-", " ")

    header = "The "
    for i, (argument, _) in enumerate(inverted_args):
        if i == len(inverted_args) - 1:
            if argument == 'unclesaunts':
                header += f" uncles and aunts of {initial}:"
            else:
                header += argument + f" of {initial}:"    
            
            aux = {}

            if isinstance(individual,list):
                for elem in individual:
                    aux[elem] = handle_queries(argument,elem,g)
            elif isinstance(individual,str):
                aux[individual] = handle_queries(argument,individual,g)
            
            if len(aux.keys())== 1 and list(aux.values())[0] == []:
                print("Non existing info regarding this relationships.")
                exit()
            
            print(header)
            unique = set()
            message = "Results come from:\n"
            
            
            for person,relations in aux.items():
                for p in relations:
                    unique.add(p)
                if relations != []:
                    message += " " + person.replace("-"," ") + "\n"
            for elem in unique:
                print("*", elem.replace("-"," "))
            
            print("\n",message)
        
        else:
            if argument == 'unclesaunts':
                header += "uncles and aunts of the "
            else:
                header += argument + " of the "
            if isinstance(individual,list):
                aux = []
                for elem in individual:
                    aux.extend(handle_queries(argument,elem,g))
                individual = aux
            elif isinstance(individual,str):
                aux = handle_queries(argument,individual,g)
                individual = aux


        

      




def execute_sparql_query(query_string, graph):
    query = prepareQuery(query_string)
    result = graph.query(query)
    return result

def apply_query():
    cwd =os.getcwd()
    dataControl.search_anbtk()
    g = genealogia.read_onto_file('anbsafeonto.rdf')
    query_composition(cwd,g)
    # uncles_aunts_query  = unclesauntsQres('Rui-Miguel-Santos-Ferreira')
    # result = execute_sparql_query(uncles_aunts_query,g)
    # if not result:
    #       print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    # for row in result:
    #   print(row[0].toPython())
    

    # print("**1 tios**")
    # grandparents_query = grandparentsQres('Rui-Miguel-Santos-Ferreira')
    # result = execute_sparql_query(grandparents_query,g)
    # if not result:
    #       print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    # for row in result:
    #   print(row)
    # print("**2 irmaos**")
    # siblings_query = siblingsQres('Rui-Miguel-Santos-Ferreira')
    # result = execute_sparql_query(siblings_query,g)
    # if not result:
    #       print("The individual does not exist in this Ancestors Notebook or it does not have any siblings.")
    # for row in result:
    #   print(row)
    # print("**3 pasta avos**")
    # gp_folder_query = gp_folderPath_Qres('Rui-Miguel-Santos-Ferreira')
    # result = execute_sparql_query(gp_folder_query,g)
    # if not result:
    #       print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    # for row in result:
    #   print(row[0].value)
    # print("**4 pasta pais**")
    # parents_folder_query = parents_folderPath_Qres('Rui-Miguel-Santos-Ferreira')
    # result = execute_sparql_query(parents_folder_query,g)
    # if not result:
    #       print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    # for row in result:
    #   print(row[0].value)
    # print("**5 pasta filhos**")

    # children_folder_query = children_folderPath_Qres('Rui-Miguel-Santos-Ferreira')
    # result = execute_sparql_query(children_folder_query,g)
    # if not result:
    #       print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    # for row in result:
    #   print(row[0].value)
    # print("**6 pasta irmaos**")

    
    # siblings_folder_query = siblings_folderPath_Qres('Rui-Miguel-Santos-Ferreira')
    # result = execute_sparql_query(siblings_folder_query,g)
    # if not result:
    #       print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    # for row in result:
    #   print(row[0].value)
    # print("**that one**")
  

    
    

        


