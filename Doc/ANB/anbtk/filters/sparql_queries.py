
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

'============================ATTRIBUTES================================='

def individual_label_Qres(individual):
    """
    Returns a SPARQL query that retrieves the label of an individual in a family RDF graph.

    Parameters:
        individual (str): The name of the individual whose label should be retrieved.

    Returns:
        str: A string representing the constructed SPARQL query.
    """
    return f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://example.org/family#>

    SELECT ?label
    WHERE {{
        :{individual} rdfs:label ?label .
    }}
    """

'''
============================FOLDERS=====================================
'''


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



def all_individuals_folderPath_Qres():
    """
    Returns a SPARQL query that retrieves the names and folder paths of all individuals in a family RDF graph.

    Returns:
        str: A string representing the constructed SPARQL query.
    """
    return """
    PREFIX family: <http://example.org/family#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?name ?folderPath
    WHERE {
        ?individual rdf:type family:Person .
        ?individual rdfs:label ?name .
        ?individual family:hasFolderPath ?folderPath .
    }
    """
