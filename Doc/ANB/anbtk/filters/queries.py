from . import sparql_queries

from rdflib.plugins.sparql import prepareQuery


def handle_namespace(namespace):
    return namespace.split('#')[1]


def execute_sparql_query(query_string, graph):
    query = prepareQuery(query_string)
    result = graph.query(query)
    return result



def lazy_search_names_folders(g): 
    """
    Search for individuals in the list of names whose second or third name starts with the given search term.

    Parameters:
        names (list): A list of names to search through.
        search_name (str): The search term to match against the second or third name of individuals.

    Returns:
        list: A list of individuals whose second or third name starts with the search term.
    """

    sparql_qry = sparql_queries.all_individuals_folderPath_Qres()
    result = execute_sparql_query(sparql_qry,g)
    individuals = []
    folders = []
    for row in result:
        name = row[0].value
        folder = row[1].value
        individuals.append(name)
        folders.append(folder)
    folders = [elem.split("/")[-1] for elem in folders]
    return individuals, folders





def folder_cd_composition(unique,g):
    possibilities = []
    for value in unique:
        sparql_qry = sparql_queries.individual_folderPath_Qres(value)
        result = execute_sparql_query(sparql_qry,g)
        if not result:
            print("✗ Non-existing folderpath.")
        else:
            for row in result:
                possibilities.append(str(row["folderPath"].toPython()))
    return possibilities



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

def handle_queries(type, individual, g):
    try:
        if type == 'siblings':
            return apply_querie(sparql_queries.siblingsQres, individual, g)
        elif type == 'grandparents':
            return apply_querie(sparql_queries.grandparentsQres, individual, g)
        elif type == 'parents':
            return apply_querie(sparql_queries.parentsQres, individual, g)
        elif type == 'unclesaunts':
            return apply_querie(sparql_queries.unclesauntsQres, individual, g)
        elif type == 'children':
            return apply_querie(sparql_queries.childrenQres, individual, g)
    except Exception as e:
        # Handle the ParseException here
        print(f"✗ Some error occurred. Individual might not exist.")
        return None
    