import os
import json
import yaml
import re
from .ontology import ousia


#todo:
# about is being passed as none in the yaml, that should be changed

def check_file_structure(path):
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
    info = []
    for elem in os.listdir(path):
        if os.path.isdir(os.path.join(path,elem)):
            info.append(get_folder_info(os.path.join(path,elem)))
        else:
            info.append(elem)
    return {path: info}


def populate_onto(dict_graph,graph):
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
        
    json_str = json.dumps(dir_dicts,indent=4)

    os.chdir(path)
    with open('anbvc.json', 'w') as file:
        file.write(json_str)


def compare_file_structure(path,graph):

    os.chdir(path)
    with open(os.path.join(path,'.anbtk/anbvc.json'), 'r') as file:
        old_dict = json.load(file)

    new_dict = check_file_structure(path)
    diff = compare_files_directories(old_dict,new_dict,path)

    for added_dir in diff['added_dirs']:

        parent_folder = os.path.basename(os.path.abspath(os.path.join(added_dir, os.pardir)))
        current_folder = os.path.basename(added_dir)
        ousia.add_subfolder(parent_folder,current_folder,added_dir,graph)
        print(f"    * A new folder {added_dir} was recognized.")
    
    for removed_dir in diff['removed_dirs']:
        
        parent_folder = os.path.basename(os.path.abspath(os.path.join(removed_dir, os.pardir)))
        current_folder = os.path.basename(removed_dir)
        ousia.remove_subfolder(parent_folder,current_folder,graph)
        print(f"    * {removed_dir} was removed.")

    for added_file in diff['added_files']:
        parent_folder = os.path.basename(os.path.dirname(added_file))
        if " " in os.path.basename(added_file):
            print(f"Filenames with spaces are not accepted, please rename it.\nInfo: {os.path.basename(added_file)}")
            exit()
            
        
        # add correspondence between the folder and the file
    
        ousia.add_file(parent_folder,added_file,graph)
        # it is only adding dgus
    
        if added_file.endswith(".dgu"):
            with open(added_file, 'r') as file:
                x = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",file.read()).group()
                yaml_header = yaml.full_load(x)

            ousia.add_dgu_file(yaml_header['path'],yaml_header,graph)
            print(f"    * {added_file} was added.")
            

    for removed_file in diff['removed_files']:
        parent_folder = os.path.basename(os.path.dirname(removed_file))                  
        ousia.remove_file(parent_folder,removed_file,graph)
        ousia.remove_file_special(removed_file,graph)
        print(f"    * {removed_file} was removed.")

    return new_dict

from .DSL.entities import gramLogic
from .auxiliar import dgu_helper

from rdflib.term import Literal, URIRef

def update_headers(path,graph):
    path = os.path.dirname(dataControl.find_anb())
    files = gramLogic.retrieve_all_dgu_files(path)
    for file in files:
        adgu = dgu_helper.parseAbstractDgu(file)
        att = ousia.get_dgu_attributes(adgu['path'],graph)
        att = [str(item) for item in att if isinstance(item, Literal)]
        if dataControl.relative_to_anbtk(adgu['path']) != file and not dgu_helper.isDguImage(adgu['path']):
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
    if os.path.isfile(os.path.join(path,'.anbtk/anbvc.json')):
        new_dict = compare_file_structure(path,graph)
        update_headers(path,graph)
        print(" ✓ Version Control file reviewed.")

    else:
        print(" ✓ Version Control file created.")
        new_dict = check_file_structure(path)
    
    create_vc_file(f'{path}/.anbtk', new_dict)

from . import genealogia
from . import dataControl


def auto_sync():
    path = dataControl.find_anb()
       
    if path != None:
        path = os.path.dirname(path)
        ontofile = os.path.join(path,".anbtk/anbsafeonto.rdf")
        g = genealogia.read_onto_file(ontofile)
        version_control(path,g)
        genealogia.gen_onto_file(g,'anbsafeonto')
    else:
        print("✗ Not in any initialized ANB folder.")