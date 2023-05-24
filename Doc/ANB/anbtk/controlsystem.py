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
                print(yaml_header)
                ousia.add_file(os.path.basename(individual),file,graph)
                


def create_vc_file(path,dir_dicts): 
        
    json_str = json.dumps(dir_dicts,indent=4)
    print(path)
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
        # add correspondence between the folder and the file
        ousia.add_file(parent_folder,added_file,graph)
        
        with open(added_file, 'r') as file:
            x = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",file.read()).group()
            yaml_header = yaml.full_load(x)



        # create the file spec in the ontology
        if yaml_header['type'] == 'Biography':
            ousia.add_fileBio(yaml_header['id'],yaml_header['Birthdate'],yaml_header['Deathdate'],added_file,"",graph)
        
        elif yaml_header['type'] == 'Story':
            ousia.add_fileStory(yaml_header['id'],yaml_header['title'],added_file,yaml_header['author'],yaml_header['date'],"",graph)
        
        elif yaml_header['type'] == 'Picture':
            ousia.add_Picture(yaml_header['id'],added_file,yaml_header['format'],"",graph)
        print(f"    * {added_file} was added.")

    for removed_file in diff['removed_files']:  
        parent_folder = os.path.basename(os.path.dirname(removed_file))                  
        ousia.remove_file(parent_folder,removed_file,graph)
        ousia.remove_file_special(removed_file,graph)
        print(f"    * {removed_file} was removed.")

    return new_dict

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
        print("Version Control file reviewed.")
        new_dict = compare_file_structure(path,graph)

    else:
        print("Version Control file created.")
        new_dict = check_file_structure(path)
    
    create_vc_file(f'{path}/.anbtk', new_dict)