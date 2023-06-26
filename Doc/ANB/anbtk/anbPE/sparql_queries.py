from .. import genealogia
from .. import dataControl
from rdflib.plugins.sparql import prepareQuery




def unclesQres(individual):
      
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

def execute_sparql_query(query_string, graph):
    query = prepareQuery(query_string)
    result = graph.query(query)
    return result

def apply_query():
    dataControl.search_anbtk()
    g = genealogia.read_onto_file('anbsafeonto.rdf')
    uncles_aunts_query  = unclesQres('Rui-Miguel-Santos-Ferreira')
    result = execute_sparql_query(uncles_aunts_query,g)
    if not result:
          print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    for row in result:
      print(row)

    print("**1 tios**")
    grandparents_query = grandparentsQres('Rui-Miguel-Santos-Ferreira')
    result = execute_sparql_query(grandparents_query,g)
    if not result:
          print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    for row in result:
      print(row)
    print("**2 irmaos**")
    siblings_query = siblingsQres('Rui-Miguel-Santos-Ferreira')
    result = execute_sparql_query(siblings_query,g)
    if not result:
          print("The individual does not exist in this Ancestors Notebook or it does not have any siblings.")
    for row in result:
      print(row)
    print("**3 pasta avos**")
    gp_folder_query = gp_folderPath_Qres('Rui-Miguel-Santos-Ferreira')
    result = execute_sparql_query(gp_folder_query,g)
    if not result:
          print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    for row in result:
      print(row[0].value)
    print("**4 pasta pais**")
    parents_folder_query = parents_folderPath_Qres('Rui-Miguel-Santos-Ferreira')
    result = execute_sparql_query(parents_folder_query,g)
    if not result:
          print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    for row in result:
      print(row[0].value)
    print("**5 pasta filhos**")

    
    children_folder_query = children_folderPath_Qres('Rui-Miguel-Santos-Ferreira')
    result = execute_sparql_query(children_folder_query,g)
    if not result:
          print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    for row in result:
      print(row[0].value)
    print("**6 pasta irmaos**")

    siblings_folderPath_Qres
    siblings_folder_query = siblings_folderPath_Qres('Rui-Miguel-Santos-Ferreira')
    result = execute_sparql_query(siblings_folder_query,g)
    if not result:
          print("The individual does not exist in this Ancestors Notebook or it does not have any aunts/uncles.")
    for row in result:
      print(row[0].value)
    print("****")

    
    

        


