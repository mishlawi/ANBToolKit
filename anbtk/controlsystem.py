import os
import json
import yaml
import re
from .ontology import ousia
from . import genealogia
from . import dataControl
from .DSL.entities import gramLogic
from .auxiliar import dgu_helper
from rdflib.term import Literal



def check_file_structure(path):
    """
    Analyze the directory structure and contents at the specified path.

    This function explores the directory structure at the given 'path' and collects
    information about directories and their contents. It creates a dictionary
    representing the directory structure with directory names as keys and lists of
    contained files or subdirectories as values.

    Args:
        path (str): The path to the directory whose structure you want to analyze.

    Returns:
        dict: A dictionary representing the directory structure, with directory names
              as keys and lists of files or subdirectories as values.
    """
    dirs = []
    dir_dicts = {}  # create a new list to store directory dictionaries
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)) and not item.startswith("."):
            dirs.append(item)
    for directory in dirs:
        folder_contents = []
        # adds the filepath as a node property of the individual, which is given by its name
        for elem in os.listdir(os.path.join(path, directory)):
            if not os.path.islink(os.path.join(path, directory, elem)):
                if os.path.isdir(os.path.join(path,directory, elem)):
                    folder_contents.append(get_folder_info(os.path.join(path,directory, elem)))
                else:
                    folder_contents.append(os.path.join(path, directory, elem))
            
        value = {directory : folder_contents}
        dir_dicts.update(value)  # append the directory dictionary to the new list
    return dir_dicts

def get_folder_info(path):
    """
    Retrieve information about the contents of a folder recursively.

    This function explores the contents of a folder specified by 'path' and
    recursively collects information about files and subdirectories. It returns
    a dictionary where the keys are file or directory paths, and the values are
    lists containing further information about the contents of subdirectories.

    Args:
        path (str): The path to the folder whose contents you want to retrieve.

    Returns:
        dict: A dictionary representing the folder's contents and subdirectory structures.
    """
    info = []
    for elem in os.listdir(path):
        if os.path.isdir(os.path.join(path,elem)):
            info.append(get_folder_info(os.path.join(path,elem)))
        else:
            info.append(elem)
    return {path: info}


def populate_onto(dict_graph,graph):
    """
    Populate an ontology graph with directory structure information.

    This function populates an ontology graph with information from a directory structure
    represented by 'dict_graph'. It traverses the dictionary, adding subfolders and files
    to the ontology graph. For files, it also adds ontology-related information, such as
    DGU (Data Generation Unit) metadata.

    Args:
        dict_graph (dict): A dictionary representing the directory structure.
        graph: The ontology graph to which directory structure information will be added.

    Note:
        This function assumes the existence of a global 'ousia' object for ontology-related
        operations.

    Returns:
        None
    """

    for individual,files in dict_graph.items():
        for file in files:
            if isinstance(file,dict):
                populate_onto(file,graph)               
                ousia.add_subfolder(os.path.basename(list(file.keys())[0]),individual,list(file.keys())[0],graph)
            else:
                # here will be the ontology addition of dgus
                with open('myfile.yaml', 'r') as file:
                    yaml_header = yaml.safe_load(file)
                
                ousia.add_file(os.path.basename(individual),file,graph)
                

def create_vc_file(path,dir_dicts):
    """
    Create a version control file to store directory structure information.

    This function writes the directory structure information, provided in 'dir_dicts',
    to a JSON file named 'anbvc.json'. The JSON file can serve as a version control
    record of the directory structure.

    Args:
        path (str): The path where the 'anbvc.json' file will be created.
        dir_dicts (dict): A dictionary representing the directory structure.

    Returns:
        None
    """
    
    json_str = json.dumps(dir_dicts,indent=4)

    os.chdir(path)
    with open('anbvc.json', 'w') as file:
        file.write(json_str)


def compare_file_structure(path,graph):
    """
    Compare the current directory structure with a previous version and update an ontology graph.

    This function performs a comparison between the current directory structure and a previously
    recorded version (stored in 'anbvc.json'). It identifies added and removed files and directories,
    updates the ontology graph accordingly, and prints messages about these changes.

    Args:
        path (str): The path to the directory whose structure you want to compare.
        graph: The ontology graph to be updated with directory structure changes.

    Returns:
        dict: A dictionary representing the current directory structure after the comparison.
    """

    os.chdir(path)
    with open(os.path.join(path,'.anbtk/anbvc.json'), 'r') as file:
        old_dict = json.load(file)

    new_dict = check_file_structure(path)
    diff = compare_files_directories(old_dict,new_dict,path)
    

    for added_dir in diff['added_dirs']:

        parent_folder = os.path.basename(os.path.abspath(os.path.join(added_dir, os.pardir)))
        current_folder = os.path.basename(added_dir)
        ousia.add_subfolder(parent_folder,current_folder,added_dir,graph)
        print(f"* A new folder {added_dir} was recognized.")
    
    for removed_dir in diff['removed_dirs']:
        
        parent_folder = os.path.basename(os.path.abspath(os.path.join(removed_dir, os.pardir)))
        current_folder = os.path.basename(removed_dir)
        ousia.remove_subfolder(parent_folder,current_folder,graph)
        print(f"* {removed_dir} was removed.")

    for added_file in diff['added_files']:
        parent_folder = os.path.basename(os.path.dirname(added_file))
        if " " in os.path.basename(added_file):
            print(f"Filenames with spaces are not accepted, please rename it.\nInfo: {os.path.basename(added_file)}")
            exit()
             
        ousia.add_file(parent_folder,added_file,graph)

    
        if added_file.endswith(".dgu"):
            with open(added_file, 'r') as file:
                x = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",file.read()).group()
                yaml_header = yaml.full_load(x)

            ousia.add_dgu_file(yaml_header['path'],yaml_header,graph)
            print(f"* {added_file} was added.")
            

    for removed_file in diff['removed_files']:
        parent_folder = os.path.basename(os.path.dirname(removed_file))                  
        ousia.remove_file(parent_folder,removed_file,graph)
        ousia.remove_file_special(removed_file,graph)
        print(f"* {removed_file} was removed.")

    return new_dict



def update_headers(path,graph):
    """
    Update YAML headers of DGU (Data Generation Unit) files and their ontology representation.

    This function iterates through DGU files in the specified 'path', updates their YAML headers,
    and synchronizes the changes with the ontology graph. It ensures that the ontology reflects
    the updated information from the DGU files.

    Args:
        path (str): The path to the directory containing DGU files to be updated.
        graph: The ontology graph to be synchronized with the changes.

    Returns:
        None
    """
    path = os.path.dirname(dataControl.find_anb())
    files = gramLogic.retrieve_all_dgu_files(path)
    for file in files:
        adgu = dgu_helper.parseAbstractDgu(file)
        att = ousia.get_dgu_attributes(adgu['path'],graph)
        att = [str(item) for item in att if isinstance(item, Literal)]
        if dataControl.relative_to_anbtk(adgu['path']) != file and not dgu_helper.isDguImage(file):
            adgu['path'] = file
            body = adgu['body']
            del(adgu['body'])
            with open(file, 'w') as f:
                f.write("---\n")
                yaml.dump(adgu, f, default_flow_style=False, sort_keys=False)
                f.write("---\n")
                f.write(body)
        if 'body' in adgu.keys():
            del(adgu['body'])
        adu_path = adgu['path']
        del adgu['path']
        adgu_attributes = list(adgu.values())
        for i in range(len(adgu_attributes)):
            elem = adgu_attributes[i]
            if isinstance(elem, list):
                adgu_attributes[i] = ousia.format_names(elem)
        if adgu_attributes != att:
            ousia.remove_dgu_file(adu_path,graph)
            ousia.add_dgu_file(adu_path,adgu,graph) 
            print(f"✓ Yaml header changes in {os.path.basename(file)} verified.\nOntology updated.")




def compare_files_directories(dir1, dir2, base_dir=''):
    """Compares two directories and returns the added files, removed files, added directories, and removed directories.

    Args:
        dir1 (dict): The directory structure of the first directory.
        dir2 (dict): The directory structure of the second directory.
        base_dir (str, optional): The base directory path. Defaults to ''.

    Returns:
        dict: A dictionary containing the added files, removed files, added directories, and removed directories.
    """
    def get_files_and_dirs(d, path=''):
        files = set()
        dirs = set()
        for key, value in d.items():
            if isinstance(value, list):
                dirs.add(key)
                for item in value:
                    if isinstance(item, str):
                        files.add(os.path.join(key,item))
                    elif isinstance(item, dict):
                        sub_files, sub_dirs = get_files_and_dirs(item,key)
                        files.update(sub_files)
                        dirs.update(sub_dirs)
            elif isinstance(value, str):
                files.add(path + key)
        return files, dirs

    dir1_files, dir1_dirs = get_files_and_dirs(dir1)
    dir2_files, dir2_dirs = get_files_and_dirs(dir2)

    added_files = dir2_files - dir1_files
    removed_files = dir1_files - dir2_files
    added_dirs = dir2_dirs - dir1_dirs
    removed_dirs = dir1_dirs - dir2_dirs

    def relative_paths(paths):
        return set(os.path.relpath(path, base_dir) for path in paths)

    added_files = relative_paths(added_files)
    removed_files = relative_paths(removed_files)
    added_dirs = relative_paths(added_dirs)
    removed_dirs = relative_paths(removed_dirs)

    return {'added_files': added_files, 'removed_files': removed_files,
            'added_dirs': added_dirs, 'removed_dirs': removed_dirs}

    
def version_control(path,graph):
    """
    Manage version control for the directory structure and ontology.

    This function performs version control operations for the specified 'path'. It checks
    the current directory structure against a previously recorded version (if available),
    updates the ontology graph and YAML headers as needed, and creates or updates the
    'anbvc.json' version control file.

    Args:
        path (str): The path to the directory where version control will be managed.
        graph: The ontology graph to be synchronized with the directory structure changes.

    Returns:
        None
    """
    print("AnbTk status: Checking version control file...\n")
    if os.path.isfile(os.path.join(path,'.anbtk/anbvc.json')):
        new_dict = compare_file_structure(path,graph)
        update_headers(path,graph)
        print("✓ Version Control file reviewed.")

    else:
        print("✓ Version Control file created.")
        new_dict = check_file_structure(path)
    
    create_vc_file(f'{path}/.anbtk', new_dict)
    print("✓ Version Control file updated.")




def auto_sync():
    """
    Automatically synchronize directory structure and ontology within an ANB folder.

    This function is responsible for automatic synchronization within an ANB (presumably a project or
    folder). It identifies the ANB folder using 'dataControl.find_anb()', reads the ontology graph
    from 'anbsafeonto.rdf', and performs version control using 'version_control'. Finally, it generates
    an ontology file named 'anbsafeonto' if applicable.

    Args:
        None

    Returns:
        None
    """
    path = dataControl.find_anb()
       
    if path != None:
        path = os.path.dirname(path)
        ontofile = os.path.join(path,".anbtk/anbsafeonto.rdf")
        g = genealogia.read_onto_file(ontofile)
        version_control(path,g)
        genealogia.gen_onto_file(g,'anbsafeonto')
    else:
        print("✗ Not in any initialized ANB folder.")