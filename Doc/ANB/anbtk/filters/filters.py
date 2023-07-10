import inquirer
import subprocess
import os

from rdflib.plugins.sparql import prepareQuery

from ..auxiliar import argsConfig
from . import sparql_queries
from .. import dataControl
from .. import genealogia


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
    if not any([args.siblings, args.parents, args.unclesaunts, args.grandparents, args.children]):
        print("✗ At least one of the flags -s, -p, -ua, -gp, -c is required.")
        exit()
    unique,message,header = query_composition(cwd,g,args)
    show_data(unique,message,header)



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
    print("alkjglakjg")
    cwd = os.getcwd()
    if not dataControl.search_anbtk():
        print("✗ You are not in an Ancestors Notebook." )
        exit()
    else:
        try:
            g = genealogia.read_onto_file('anbsafeonto.rdf')
        except FileNotFoundError:
            print("No ontology was initialized.\nWas this ancestor notebook created from scratch? There doesn't seem to exist any .rdf file that defines the familiar connections.")
            exit()
        os.chdir(dataControl.get_root())
    print("klajhgkajshgj")    
    args = argsConfig.a_cd()
    if not any([args.siblings, args.parents, args.unclesaunts, args.grandparents, args.children]):
        print("✗ At least one of the flags -s, -p, -ua, -gp, -c is required.")
        exit()
    print("asjkghakjghkajghk")
    unique,_,_ = query_composition(cwd,g,args)
    possibilities = folder_cd_composition(unique,g)
    selected_folder = select_path(possibilities)
    selected_folder = selected_folder.split("/")[1]
    print("alkjgslakjglakjg")
    try:
        subprocess.check_call(f"cd {selected_folder} && exec $SHELL", shell=True)
    except subprocess.CalledProcessError:
            print("Some problem in finding the folder. Were any manual naming changes made to the Ancestors Notebook folder?.")
            exit()


def anb_ls():
    cwd = os.getcwd()
    if not dataControl.search_anbtk():
        print("✗ You are not in an Ancestors Notebook." )
        exit()
    else:
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
        subprocess.check_call(f"ls {selected_folder} && exec $SHELL", shell=True)
    except subprocess.CalledProcessError:
            print("Some problem in finding the folder. Were any manual naming changes made to the Ancestors Notebook folder?.")
            exit()

    
def lazy_search(names,search_name): 
    """
    Search for individuals in the list of names whose second or third name starts with the given search term.

    Parameters:
        names (list): A list of names to search through.
        search_name (str): The search term to match against the second or third name of individuals.

    Returns:
        list: A list of individuals whose second or third name starts with the search term.
    """
    matching_individuals = []
    for name in names:
        name_parts = name.split('-')
        if len(name_parts) >= 3 and (search_name.lower() == name_parts[1].lower()[:len(search_name)] or
                                     search_name.lower() == name_parts[2].lower()[:len(search_name)]):
            matching_individuals.append(name)
    return matching_individuals
        
