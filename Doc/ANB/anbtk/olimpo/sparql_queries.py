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
  ?parent family:hasFolder ?folder .
}}

"""


