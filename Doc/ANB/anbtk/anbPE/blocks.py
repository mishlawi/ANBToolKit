import subprocess
import os
import threading 

from ..DSL.family import gramma


def edit_block(config_data):
    """
    Edits the block of configuration data.

    This function opens a temporary file, writes the provided configuration data to it,
    and launches a text editor (Vim) for the user to modify the contents of the file.
    After the user saves and closes the editor, the modified block is read from the temporary file,
    the file is removed, and the modified block is returned.

    Args:
        config_data (str): The configuration data to be edited.

    Returns:
        str: The modified block of configuration data.
    """

    temp_filename = "temp_config.txt"
    with open(temp_filename, "w") as temp_file:
        temp_file.write(config_data)


    # editor_command = ["code", "--wait", temp_filename]
    # editor_command = ["vi", temp_filename]
    default_editor = os.environ.get('EDITOR', 'vim')
    editor_command = [default_editor, temp_filename]

    subprocess.run(editor_command)


    with open(temp_filename, "r") as temp_file:
        modified_block = temp_file.read()

    os.remove(temp_filename)

    return modified_block

# need to add error handling
def check_errors(modified_block):
    """
    Checks for parsing errors in the modified block.

    This function uses the 'gramma.check_parsing()' function to parse the modified block
    and raises an exception if there are any parsing errors.

    Args:
        modified_block (str): The modified block of configuration data.

    Raises:
        Exception: If there are parsing errors in the modified block.
    """
    gramma.check_parsing(modified_block)


def changed(dict1,dict2):
    """
    Compares two dictionaries and identifies the changes between them.

    This function compares the keys of the two dictionaries and identifies if there is a change in the key.
    If the keys are different, it determines the removed and added values between the two dictionaries.
    If the keys are the same, it only determines the removed and added values within the corresponding key.

    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.

    Returns:
        tuple: A tuple containing the changed values and the changed key.
            The changed values are a dictionary with 'removed' and 'added' keys, representing the removed and added values.
            The changed key is a dictionary with 'new' and 'old' keys, representing the new and old keys.
    """
    if len(dict1)>1:
        raise Exception("Something went wrong ")
    changed_values = {}

    if list(dict1.keys())[0]!=list(dict2.keys())[0]:
        changed_key = {'new': list(dict2.keys())[0], 'old' : list(dict1.keys())[0]}

        removed = [elem for elem in list(dict1.values())[0] if elem not in list(dict2.values())[0]] 
        added = [elem for elem in list(dict2.values())[0] if elem not in  list(dict1.values())[0]]
        #changed_values = { 'added':added, 'added':removed }
    else:
        changed_key = {}
        removed = [elem for elem in list(dict1.values())[0] if elem not in list(dict2.values())[0]] 
        added = [elem for elem in list(dict2.values())[0] if elem not in  list(dict1.values())[0]]
    changed_values['removed'] = removed
    changed_values['added'] = added
    return changed_values,changed_key




def updates(before_block, changed_ids, before_ids, values, keys):
    """
    Updates the block based on the changes made.

    This function takes in the original block that was going to be changed, the changed ids (db,dd,nickname) that were changed, the ids before the changes,
    the values that have changed and the keys that have changed.
    It determines the changes that were made to the block, either new parents, removed parents, updated parents, added children, removed children,
    and updated children.

    Args:
        before_block (dict): The original block.
        changed_ids (dict): The changed IDs.
        before_ids (dict): The IDs before the changes.
        values (dict): The values that have changed.
        keys (dict): The keys that have changed.

    Returns:
        tuple: A tuple containing the new parent, removed parent, updated parent,
            added children, removed children, and updated children.
            Each of these items is a list containing the relevant values or dictionaries.
    """

    new_parent = []
    updated_parent = []
    removed_parent = []
    if keys!={}:
        new_key = keys['new']
        old_key = keys['old']

        new_p1, new_p2 = new_key.split("+")
        old_p1 , old_p2 = old_key.split("+")
        if new_p1 == old_p1 and new_p2 != old_p2:
            new_parent = [(old_p2,{new_p2 : changed_ids[new_p2]})]
            removed_parent.append(old_p2)
        elif new_p1 != old_p1 and new_p2 == old_p2:
            new_parent = [(old_p1,{new_p1 : changed_ids[new_p1]})]
            removed_parent.append(old_p1)

        elif new_p1 != old_p1 and new_p2 != old_p2:
            new_parent = [(old_p1,{new_p1 : changed_ids[new_p1]}),(old_p2,{new_p2 : changed_ids[new_p2]})]
            removed_parent.append(old_p1)
            removed_parent.append(old_p2)

    else:
        p1,p2 = list(before_block.keys())[0].split("+")
        if before_ids[p1]!=changed_ids[p1]:
            updated_parent.append({p1:changed_ids[p1]})
        if before_ids[p2]!=changed_ids[p2]:
            updated_parent.append({p2:changed_ids[p2]})

    updated_children = [] 
    added_children = []
    removed_children = []
    if (added := values['added']) != []:
        for child in added:
            added_children.append({child:changed_ids[child]})
    if (removed := values['removed']) != []:
        for child in removed:
            removed_children.append(child)
    if (removed := values['removed']) == [] and (added := values['added']) == [] :
        for elem in list(before_block.values())[0]:
            if before_ids[elem] != changed_ids[elem]:
                updated_children.append({elem:changed_ids[elem]})

    return new_parent,removed_parent,updated_parent,added_children,removed_children,updated_children



def dict_to_file(block,ids):
    """
    Converts a dictionary to the correct representation of an anb temp file.

    This function takes in an IDs dictionary and a block dictionary, and it converts them into a string
    representation of a file. The IDs and block information are formatted according to specific rules.

    Args:
        ids (dict): The IDs dictionary.
        block (dict): The block dictionary.

    Returns:
        str: The string representation of the file.
    """
    if 'total' in ids.keys():
        del ids['total']
    if 'undiscovered' in ids.keys():
        del ids['undiscovered']
    
    string = ''
    
    for key,value in block.items():
        p1,p2 = key.split("+")
        if p1.startswith("undiscovered"):
            p1 = p1.split("_")[1]
        if p2.startswith("undiscovered"):
            p2 = p2.split("_")[1]

        bd_p1 = ids[p1]["birthDate"]
        dd_p1 = ids[p1]["deathDate"]
        bd_p2 = ids[p2]["birthDate"]
        dd_p2 = ids[p2]["deathDate"]
        n_p1 = ids[p1]["nickname"]
        n_p2 = ids[p2]["nickname"]

        string += f"{p1} "
        
        if n_p1 != '':
            string += f"({n_p1}) "
        
        if bd_p1 == dd_p1 and bd_p1 == "?":
            string = string + f"? + "
        else:
            string = string + f"({bd_p1} {dd_p1}) +"

        string += f"{p2} "
        
        if n_p2 != '':
            string += f"({n_p2}) "

        if bd_p2 == dd_p2 and bd_p2 == "?":
            string = string + f"?\n"
        else:
            string = string + f"({bd_p2} {dd_p2})\n"
        for child in value:
            if child.startswith("undiscovered"):
                string = string + '.#' + child.split("_")[1] + '\n'
            else:
                bd = ids[child]["birthDate"]
                dd = ids[child]["deathDate"]
                nn = ids[child]["nickname"]
                string += f".{child} "
                if nn != '':
                    string += f"({nn}) "
                if bd == dd and bd == "?":
                    string = string + f"?\n"
                else:
                    string = string + f"({bd} {dd})\n"
        string += '\n'
    return string




def replace_updated_block_file(file, before, after):
    """
    Replaces the updated block in a file.

    This function takes in a file path, the original block, and the modified block.
    It reads the contents of the file, replaces the original block with the modified block,
    and writes the updated contents back to the file.

    Args:
        file (str): The file path.
        before (str): The original block.
        after (str): The modified block.
    """
    with open(file, 'r') as sf:
        text = sf.read()
    text = text.replace(before, after)

    with open(file, 'w') as sf:
        sf.write(text)


def add_new_dict_block_file(file,block,ids):
    with open(file, 'r') as sf:
        text = sf.read()

    text += dict_to_file(block,ids)

    with open(file, 'w') as sf:
        sf.write(text)



def remaining_blocks(structure_file_path,chosen_block):
    """
    Retrieves the remaining blocks after removing the chosen block.

    This function takes in the file path of a structure and a chosen block to remove.
    It parses the structure file using 'gramma.parsing()' and removes the chosen block
    from the parsed blocks. The remaining blocks are returned.

    Args:
        structure_file_path (str): The file path of the structure.
        chosen_block (dict): The chosen block to remove.

    Returns:
        dict: The remaining blocks.
    """

    blocks,ids = gramma.parsing(structure_file_path)
    block_couple = list(chosen_block.keys())[0]

    del blocks[block_couple]


    return blocks,ids

def new_block(unedited_geral_block,changed_block):
    """
    Determins the new block that was created by adding the changed block to the unedited block.

    This function takes in an unedited block and a changed block. It adds the changed block
    to the unedited block and returns the new block.

    Args:
        unedited_geral_block (dict): The unedited block.
        changed_block (dict): The changed block.

    Returns:
        dict: The new block.
    """

    couple_name = list(changed_block.keys())[0]
    couple_children = changed_block[couple_name]
    unedited_geral_block[couple_name] = couple_children

    
    return unedited_geral_block


def add_newlines(string):
    """
    Adds newlines at the end of the string to guarantee a correct parsing always.

    Args:
        string (str): The input string.

    Returns:
        str: The string with newlines added.
    """
    string = string.rstrip('\n')
    return string + '\n\n'