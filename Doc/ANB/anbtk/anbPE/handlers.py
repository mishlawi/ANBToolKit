import os

from pathlib import Path
from ..ontology import ousia

from .. import dataControl
from .. import genealogia


"""
===============================================================
======================= HANDLERS FUNCTIONS ====================
===============================================================
"""

def handler_new_parents(new_parent,g):
    """
    Handle the addition of new parents in the genealogical graph.

    Parameters:
        new_parent (list): List of new parent information.
        g: The genealogical graph object.

    This function adds new parent individuals to the genealogical graph and updates their attributes.
    """
    for parent in new_parent:
        old = genealogia.adapt_name(parent[0])
        new  = parent[1]
        parent_name = list(new.keys())[0]
        parent_bd = new[parent_name]['birthDate']
        parent_dd = new[parent_name]['deathDate']

        ousia.switch_individual(old,genealogia.adapt_name(parent_name),parent_name,parent_bd,parent_dd,g)


def handler_children(removed_children,added_children,changed_block,og_block,g):
    """
    Handle changes in child individuals and their relationships in the genealogical graph.

    Parameters:
        removed_children (list): List of removed child individuals.
        added_children (list): List of added child individuals.
        changed_block (dict): Changed data block.
        og_block (dict): Original data block.
        g: The genealogical graph object.

    This function handles removed child individuals, adds new child individuals, and updates their attributes and
    relationships within the genealogical graph.
    """
    
    cwd = os.getcwd()
    path = dataControl.get_root()
    os.chdir(path)
    p_k = parents_kids(changed_block)
    for elem in removed_children:
        ousia.delete_children_individual(genealogia.adapt_name(elem),g)     
        parents = get_parents(elem,og_block)
        p1,p2 = parents
        p1 = genealogia.adapt_name(p1)
        p2 = genealogia.adapt_name(p2)
        if not elem.startswith("undiscovered"):
            if os.path.exists(f".{p1}+{p2}"):
                elem = genealogia.adapt_name(elem)
                os.unlink(f".{p1}+{p2}/{elem}") 
            if elem not in p_k['parents']:
                warning(genealogia.adapt_name(elem))
                os.rmdir(genealogia.adapt_name(elem))     
    # é preciso encontrar os pais do filho caso nao existam filhos removidos.
    if removed_children == []:
        parents = list(changed_block.keys())[0]    
        p1,p2 = parents.split("+")
        p1 = genealogia.adapt_name(p1)
        p2 = genealogia.adapt_name(p2)
    for elem in added_children:
        og_name = list(elem.keys())[0]
        bd = elem[og_name]['birthDate']
        dd = elem[og_name]['deathDate']
        individual = genealogia.adapt_name(og_name)
        ousia.add_complete_individual(individual,og_name,bd,dd,g)
        ousia.add_parent_children(p1,p2,individual,g)
        if not os.path.exists(individual):
            os.mkdir(individual)
            path=os.path.basename(path)
            relpath = os.path.join(path,individual)

            ousia.add_folder(individual,relpath,g)
            os.symlink(f'../{individual}',f'.{p1}+{p2}/{individual}')

    os.chdir(cwd)


def handler_add_new_parent_folders(new_parents,updated_block,g):
    """
    Handle the addition of new parent folders to the project structure.

    Parameters:
        new_parents (list): List of new parent information.
        updated_block (dict): Updated data block.
        g: The genealogical graph object.

    This function generates parent folders for newly added parents based on the updated data block.
    """
    path = dataControl.get_root()
    cwd = os.getcwd()
    os.chdir(path)
    for new_parent in new_parents:
        for couple in updated_block.keys():
            if list(new_parent[1].keys())[0] in couple:
                genealogia.gen_parents_folders(couple,updated_block[couple],g,path)
    if os.path.exists(cwd):
        os.chdir(cwd)    



def handler_removed_parent_folders(removed_parents,og_family):
    """
    Handle the removal of parent folders from the project structure.

    Parameters:
        removed_parents (list): List of removed parent individuals.
        og_family (dict): Original family data.

    This function removes parent folders and associated symbolic links from the project structure.
    """
    path = dataControl.get_root()
    cwd = os.getcwd()
    is_child = False
    os.chdir(path)
    for rm_parent in removed_parents:
        for parents,children in og_family.items():
            if rm_parent in children:
                is_child = True
            if rm_parent in parents:
                print("yess")
                p1,p2 = parents.split("+")
                p1 = genealogia.adapt_name(p1)
                p2 = genealogia.adapt_name(p2)
                os.unlink(genealogia.adapt_name(rm_parent)+'/'+ f'.{p1}+{p2}')
                if genealogia.adapt_name(rm_parent) == p1:
                    os.unlink(p2+'/'+ f'.{p1}+{p2}')
                elif genealogia.adapt_name(rm_parent) == p2:
                    os.unlink(p1+'/'+ f'.{p1}+{p2}')                
                for child in children:
                    if not child.startswith("undiscovered"):
                        os.unlink(f".{p1}+{p2}"+'/'+genealogia.adapt_name(child))
                os.rmdir(f".{p1}+{p2}")
        if not is_child:
            path = genealogia.adapt_name(rm_parent)
            warning(path)
            os.rmdir(genealogia.adapt_name(rm_parent))
    os.chdir(cwd)


def update_data(elem,g):
    """
    Update individual attributes in the genealogical graph.

    Parameters:
        elem: Data element to update.
        g: The genealogical graph object.

    This function updates individual attributes such as birthdate, deathdate, and nickname in the genealogical graph.
    """
    og_name = list(elem.keys())[0]
    bd = elem[og_name]['birthDate']
    dd = elem[og_name]['deathDate']
    nickname = elem[og_name]['nickname']
    individual = genealogia.adapt_name(og_name)
    ousia.update_birthdate(individual,bd,g)
    ousia.update_deathdate(individual,dd,g)
    ousia.update_nickname(individual,nickname,g)

def handler_updates(updated_parents, updated_children, g):
    """
    Handle updates to individual attributes in the genealogical graph.

    Parameters:
        updated_parents (list): List of updated parent information.
        updated_children (list): List of updated child information.
        g: The genealogical graph object.

    This function handles updates to individual attributes such as birthdate, deathdate, and nickname in the
    genealogical graph.
    """
    for elem in updated_parents:
        update_data(elem,g)

    for elem in updated_children:
        update_data(elem,g)



"""
===============================================================
=====================  AUXILIAR FUNCTIONS  ====================
===============================================================
"""

            
def get_parents(individual,block):
    """
    Get the parents of an individual from the data block.

    Parameters:
        individual (str): The individual's name.
        block (dict): The data block containing parent-child relationships.

    Returns:
        tuple: A tuple containing the names of the parents.

    This function retrieves the parents of the given individual from the data block.
    """
    for parents,children in block.items():
        if individual in children:
            return parents.split("+")

def is_folder_empty(folder_path):
    """
    Check if a folder is empty.

    Parameters:
        folder_path (str): The path to the folder.

    Returns:
        bool: True if the folder is empty, False otherwise.

    This function checks if a given folder is empty by iterating through its contents.
    """
    folder = Path(folder_path)
    for entry in folder.iterdir():
        if entry.is_file() or entry.is_dir():
            return False
    return True

def warning(folder_path):
    """
    Display a warning message if a folder is not empty.

    Parameters:
        folder_path (str): The path to the folder.

    This function displays a warning message if the specified folder is not empty, prompting manual deletion or relocation of its contents.
    """
    if os.path.exists(folder_path):
        if not is_folder_empty(folder_path):
            print(f"There is still data in {folder_path} folder. Please move or remove it and manually delete the folder.") 
            exit()


def parents_kids(block):
    """
    Extract parent and children data from a data block.

    Parameters:
        block (dict): The data block containing parent-child relationships.

    Returns:
        dict: A dictionary with parent and children data.

    This function extracts and organizes parent and children data from the given data block.
    """
    status = {'parents': [], 'children': []}
    for couple, kids in block.items():
        if status['parents'] == []:
            status['parents'] = couple.split("+")
        else:
            for elem in couple.split("+"):
                if elem not in status['parents']:
                    status['parents'].append(elem)
        status['children'] += kids

    return status


def get_children_parent(block,parent):
    """
    Get the children of a parent from the data block.

    Parameters:
        block (dict): The data block containing parent-child relationships.
        parent (str): The parent's name.

    Returns:
        list: A list of children names associated with the parent.

    This function retrieves the children of the specified parent from the data block.
    """
    for parents,children in block.items():
        if parent in parents:
            return children


def get_parents_child(block,child):
    """
    Get the parents of a child from the data block.

    Parameters:
        block (dict): The data block containing parent-child relationships.
        child (str): The child's name.

    Returns:
        dict or None: A dictionary with parent-child relationship if found, None otherwise.

    This function retrieves the parents of the specified child from the data block.
    """
    for parents,children in block.items():
        if child in children:
            return {parents:children}
    return None