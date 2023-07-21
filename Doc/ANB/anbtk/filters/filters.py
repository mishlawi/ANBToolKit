import subprocess
import difflib
import os


from ..auxiliar import argsConfig
from ..auxiliar import dgu_helper
from .. import dataControl
from .. import genealogia
from . import view_sparql
from . import queries


def find_matching_names(input_name, name_list, threshold=0.6):
    """
    Returns the list of probable names by comparing the given argument input_name with the existing names that are referenced in the ontology.
    """
    matches = []
    
    input_words = input_name.lower().split()
    
    for name in name_list:
        name_lower = name.lower()
        is_match = True
        
        for word in input_words:
            if word not in name_lower:
                is_match = False
                break
        
        similarity_score = difflib.SequenceMatcher(None, input_name, name).ratio()
        if is_match or similarity_score >= threshold:
            matches.append(name)
    
    return matches

def individual_processing(path,g,args):
    """
    Defines the type of way that the individual's that is passed as an input  is processed, while also allowing 
    to show all the probable possibilities that the input might match, if it doesn't exist in the ontology.
    Also allows the user to choose the current folder '.' or other folders instead of names.
    
    """

    if hasattr(args, 'ordered_args'):
        inverted_args = args.ordered_args
    else:
        print("✗ You need to specify what flags you want. Use anbget -h for additional information.")
        exit()

    if len(args.individual) == 1 and args.individual[0] == ".":
        if path == dataControl.get_root():
            print("✗ Action not possible when in root folder.")
            exit()
        individual = os.path.basename(path)
        initial = individual.replace("-", " ")

    elif len(args.individual) == 1 and args.individual[0].endswith("/"):
        args.individual[0]=args.individual[0][:-1]
        individual = args.individual[0]
        initial = args.individual[0].replace("-", " ")
    else:
        individuals,folders = queries.lazy_search_names_folders(g)
        
        initial = ' '.join(args.individual)
        individual = initial
        if initial not in individuals and initial not in folders:
            if len(find_matching_names(initial,individuals)) == 0:
                print("✗ There isn't anyone that resembles that name.")
                exit()
                
            initial = view_sparql.select_names(find_matching_names(initial,individuals))
            individual = initial.replace(" ","-")

    inverted_args = inverted_args[::-1]
    header = view_sparql.compose_header(initial,args.ordered_args) 
    for i, (argument, _) in enumerate(inverted_args):
        if i == len(inverted_args) - 1:
            aux = {}

            if isinstance(individual,list):
                for elem in individual:
                    aux[elem] = queries.handle_queries(argument,elem,g)
            elif isinstance(individual,str):
                aux[individual] = queries.handle_queries(argument,individual,g)
            
            all_empty = all(val == [] for val in aux.values())
            if all_empty:
                print("✗ Non existing info regarding this relationship(s).")
                exit()
            
            unique = set()
            message = "Results come from:\n"
            print(aux)
            for person,relations in aux.items():
                for p in relations:
                    unique.add(p)
                if relations != []:
                    message += " " + person.replace("-"," ") + "\n"
            
        else:
            if isinstance(individual,list):
                aux = []
                for elem in individual:
                    aux.extend(queries.handle_queries(argument,elem,g))
                individual = aux
            elif isinstance(individual,str):
                aux = queries.handle_queries(argument,individual,g)
                individual = aux
    return unique,message,header



def anb_search():
    cwd = os.getcwd()
    dataControl.search_anbtk()
    g = genealogia.read_onto_file('anbsafeonto.rdf')
    args = argsConfig.a_search()
    # if not any([args.siblings, args.parents, args.unclesaunts, args.grandparents, args.children]):
    #     print("✗ At least one of the flags -s, -p, -ua, -gp, -c is required.")
    #     exit()
    unique,message,header = individual_processing(cwd,g,args)
    view_sparql.show_data(unique,message,header)


def anb_cd():
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

    
    unique,_,_ = individual_processing(cwd,g,args,True)
    possibilities = queries.folder_cd_composition(unique,g)
    selected_folder = view_sparql.select_path(possibilities)
    selected_folder = selected_folder.split("/")[1]
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
            os.chdir(cwd)
            g = genealogia.read_onto_file('anbsafeonto.rdf')
        except FileNotFoundError:
            print("No ontology was initialized.\nWas this ancestor notebook created from scratch? There doesn't seem to exist any .rdf file that defines the familiar connections.")
            exit()
        os.chdir(dataControl.get_root())
        
    args = argsConfig.a_cd()
    
    unique,_,_ = individual_processing(cwd,g,args)
    possibilities = queries.folder_cd_composition(unique,g)
    selected_folder = view_sparql.select_path(possibilities)
    selected_folder = selected_folder.split("/")[1]
    try:
        subprocess.check_call(f"ls {selected_folder} && exec $SHELL", shell=True)
    except subprocess.CalledProcessError:
            print("Some problem in finding the folder. Were any manual naming or structural changes made to the Ancestors Notebook folder?.")
            exit()

  

def search_by_about_files():
    g = genealogia.read_onto_file('anbsafeonto.rdf')
    root = dataControl.get_root()
    visited = set()
    for dirpath, _, filenames in os.walk(root):
        realpath = os.path.realpath(dirpath)

        if realpath in visited or os.path.basename(dirpath) == '.anbtk':
            continue
        visited.add(realpath)
        for filename in filenames:
            if filename.endswith(".dgu"):
                adgu = dgu_helper.parseAbstractDgu(filename)
                if adgu['about'] != '':
                    if isinstance(adgu['about'] , list):
                        for elem in adgu['about']:
                            if elem not in (name_list := queries.lazy_search_names_folders(g)[0]):
                                results = find_matching_names(elem,name_list)
                                if len(results) == 1:
                                    pass



        
