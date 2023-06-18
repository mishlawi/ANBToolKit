import subprocess
import shutil 
import os 

from pathlib import Path



from .DSL.family import gramma
from .ontology import ousia
from . import dataControl
from . import genealogia


# dbfile for db 




def list_and_num_families(dictionary):
    
    for i, key in enumerate(dictionary, start=1):
        print(f"{i}.     {key}")
        for element in dictionary[key]:
            print(f"        * {element}")
        print("\n")
    print("0. Leave\n")


  

def interaction(og_family):

    length = len(og_family.keys())
    while True:
        try:
            list_and_num_families(og_family)
            number = int(input(f"Choose a block to be edited: "))
            if 0 < number <= length:
                return number
            elif number == 0:
                exit(0)
            else:
                print(f"Number should be between 0 and {length}. Try again.")
        except ValueError:

            print("\n> Invalid input. Please enter a number.")
    
def visual_dictionary_simple(dictionary):
    string = ''
    for key, values in dictionary.items():
        string += key
        for value in values:
            string += value
    return string



def retrieve_content_by_name(file_path, name):
    name1,name2 = name.split("+")
    with open(file_path, 'r') as file:
        lines = file.readlines()
        found = False
        content = {}
        children = []
        for line in lines:
            if name1 in line and name2 in line:
                found = True
                save = line
            elif found and line.startswith('.'):
                children.append(line)
            elif found:
                content[save] = children
                return visual_dictionary_simple(content)
                 
    return 


def check_errors(modified_block):
    gramma.check_parsing(modified_block)

def changed(dict1,dict2):
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



def add_newlines(string):
    string = string.rstrip('\n')
    return string + '\n\n'

def handle_new_parents(new_parent,removed_parent,unedited_block,g):
    # add checker for existing kids as parents, ask if it is worth it to overwrite
    for parent in new_parent:
        old = genealogia.adapt_name(parent[0])
        new  = parent[1]
        parent_name = list(new.keys())[0]
        parent_bd = new[parent_name]['birthDate']
        parent_dd = new[parent_name]['deathDate']

        ousia.switch_individual(old,genealogia.adapt_name(parent_name),parent_name,parent_bd,parent_dd,g)

#falta atualizar pastas, no filesystem e nas ontologias

def handle_children(removed_children,added_children,changed_block,g):
    p1,p2 = list(changed_block.keys())[0].split("+")

    for elem in removed_children:
        ousia.delete_children_individual(genealogia.adapt_name(elem),g)
    for elem in added_children:
        og_name = list(elem.keys())[0]
        bd = elem[og_name]['birthDate']
        dd = elem[og_name]['deathDate']
        individual = genealogia.adapt_name(og_name)
        ousia.add_individual(individual,og_name,g)
        ousia.add_birthdate(individual,bd,g)
        ousia.add_deathdate(individual,dd,g)
        ousia.add_parent_children(genealogia.adapt_name(p1),genealogia.adapt_name(p2),individual,g)




def update_dates(elem,g):
    og_name = list(elem.keys())[0]
    bd = elem[og_name]['birthDate']
    dd = elem[og_name]['deathDate']
    individual = genealogia.adapt_name(og_name)
    ousia.update_birthdate(individual,bd,g)
    ousia.update_deathdate(individual,dd,g)

def handle_updates(updated_parents, updated_children, g):
    for elem in updated_parents:
        update_dates(elem,g)
    for elem in updated_children:
        update_dates(elem,g)


def dict_to_file(ids,block):
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
        if bd_p1 == dd_p1 and bd_p1 == "?":
            string = string + f"{p1} ? +"
        else:
            string = string + f"{p1} ({bd_p1} {dd_p1}) +"
        if bd_p2 == dd_p2 and bd_p2 == "?":
            string = string + f" {p2} ?\n"
        else:
            string = string + f" {p2} ({bd_p2} {dd_p2})\n"
        for child in value:
            if child.startswith("undiscovered"):
                string = string + '.#' + child.split("_")[1] + '\n'
            else:
                bd = ids[child]["birthDate"]
                dd = ids[child]["deathDate"]
                if bd == dd and bd == "?":
                    string = string + f".{child} ?\n"
                else:
                    string = string + f".{child} ({bd} {dd})\n"
        string += '\n'
    return string

def replace_updated_block_file(file, before, after):
    with open(file, 'r') as sf:
        text = sf.read()
    text = text.replace(before, after)

    with open(file, 'w') as sf:
        sf.write(text)


def remaining_blocks(structure_file_path,chosen_block):

    blocks,_ = gramma.parsing(structure_file_path)
    block_couple = list(chosen_block.keys())[0]

    del blocks[block_couple]


    return blocks

def new_block(unedited_geral_block,changed_block):

    couple_name = list(changed_block.keys())[0]
    couple_children = changed_block[couple_name]
    unedited_geral_block[couple_name] = couple_children

    
    return unedited_geral_block


def handle_add_new_parent_folders(new_parents,updated_block,g):
    path = dataControl.get_root()
    cwd = os.getcwd()
    os.chdir(path)
    for new_parent in new_parents:
        for couple in updated_block.keys():
            if list(new_parent[1].keys())[0] in couple:
                genealogia.gen_parents_folders(couple,updated_block[couple],g,path)
    os.chdir(cwd)    



def move_files_and_folders(source_dir, destination_dir):
    shutil.move(source_dir, destination_dir)

def is_folder_empty(folder_path):
    folder = Path(folder_path)
    for entry in folder.iterdir():
        if entry.is_file() or entry.is_dir():
            return False
    return True

def warning(folder_path):
    if not is_folder_empty(folder_path):
        print(f"There is still data in {folder_path} folder. Please move or remove it and manually delete the folder.") 


def handle_removed_parent_folders(removed_parents,og_family):
    path = dataControl.get_root()
    cwd = os.getcwd()
    is_child = False
    os.chdir(path)
    for rm_parent in removed_parents:
        for parents,children in og_family.items():
            if rm_parent in children:
                is_child = True
            if rm_parent in parents:
                p1,p2 = parents.split("+")
                p1 = genealogia.adapt_name(p1)
                p2 = genealogia.adapt_name(p2)
                os.unlink(genealogia.adapt_name(rm_parent)+'/'+ f'.{p1}+{p2}')
                os.unlink(p2+'/'+ f'.{p1}+{p2}')
                for child in children:
                    os.unlink(f".{p1}+{p2}"+'/'+genealogia.adapt_name(child))
                os.rmdir(f".{p1}+{p2}")
        if not is_child:
            path = genealogia.adapt_name(rm_parent)
            warning(path)
        
            

def edit_block(config_data):

    temp_filename = "temp_config.txt"
    with open(temp_filename, "w") as temp_file:
        temp_file.write(config_data)


    # editor_command = ["code", "--wait", temp_filename]
    # editor_command = ["vi", temp_filename]
    editor_command = ["vim", temp_filename]

    subprocess.run(editor_command)

    # Read the modified config data from the temporary file

    with open(temp_filename, "r") as temp_file:
        modified_block = temp_file.read()

    # Remove the temporary file
    os.remove(temp_filename)

    return modified_block

def add_couple():
    # arranjar forma de por este path com o nome da familia
    path = dataControl.get_root()
    cwd = os.getcwd()
    os.chdir(path)
    onto_file_path = os.path.join(dataControl.get_root(),'.anbtk/anbsafeonto.rdf')
    structure_file_path = os.path.join(dataControl.get_root(),'.anbtk/anbtemp.txt')
    g = genealogia.read_onto_file(onto_file_path)

    new_couple_block = edit_block('')
    new_couple_block = add_newlines(new_couple_block)
    block, ids = gramma.check_parsing(new_couple_block)
    
    if block == None :
        exit()
        
    parents = list(block.keys())[0]
    children = list(block.values())[0]
    print(children)
    og_name_p1,og_name_p2 = parents.split("+")
   
    og_family, og_dates = gramma.parsing(structure_file_path)
    p1_is_child = False
    p2_is_child = False

    for _,og_children in og_family.items():
        if og_name_p1 in og_children:
            p1_is_child = True
            
        elif og_name_p2 in og_children:
            p2_is_child = True
        if og_name_p1 in parents:
            pass
        elif og_name_p2 in parents:
            pass

    
    p1 = genealogia.adapt_name(og_name_p1)
    p2 = genealogia.adapt_name(og_name_p2)

    if not p1_is_child and not p2_is_child:
        print("unique parents")    
        genealogia.populate_graph(block,g)
        genealogia.gen_parents_folders(parents,children,g,path)
    else:
        if p1_is_child:
            print("parent 1 is a child")
            ousia.add_individual(p2,og_name_p2,g)
            ousia.add_hasSpouse(p1,p2,g)
            genealogia.gen_parents_folders(parents,children,g,path)
            
        elif p2_is_child:
            print("parent 2 is a child")
            ousia.add_individual(p1,og_name_p1,g)
            ousia.add_hasSpouse(p2,p1,g)
            genealogia.gen_parents_folders(parents,children,g,path)

        
        for child in children:
                child = genealogia.adapt_name(child)
                ousia.add_parent_children(p1,p2,child,g)
        
        cwd = os.getcwd()
        os.chdir(dataControl.find_anb())
        genealogia.gen_onto_file(g,'anbsafeonto')
        os.chdir(cwd)


# paths are not okay; should be relative
# 




def action():
    onto_file_path = os.path.join(dataControl.get_root(),'.anbtk/anbsafeonto.rdf')
    structure_file_path = os.path.join(dataControl.get_root(),'.anbtk/anbtemp.txt')
    
    og_family, og_dates = gramma.parsing(structure_file_path)


    block_number = interaction(og_family)
    key = list(og_family.keys())[block_number-1]
    block = retrieve_content_by_name(structure_file_path,key)
    before_block,before_ids = gramma.check_parsing(add_newlines(block))
    modified_block = edit_block(block)
    modified_block = add_newlines(modified_block)
    changed_block,changed_ids = gramma.check_parsing(modified_block)

    
    values,keys = changed(before_block,changed_block)
    new_parent,removed_parent,updated_parents, added_children, removed_children, updated_children = updates(before_block,changed_ids,before_ids,values,keys)
    
    unedited_geral_block = remaining_blocks(structure_file_path,before_block)
    updated_geral_block = new_block(unedited_geral_block,changed_block)


    if new_parent != [] or updated_parents!= [] or added_children != [] or removed_children != [] or updated_children!=[]:
        

        g = genealogia.read_onto_file(onto_file_path)
        

        handle_new_parents(new_parent,removed_parent,unedited_geral_block,g)
        handle_add_new_parent_folders(new_parent,updated_geral_block,g)
        handle_removed_parent_folders(removed_parent,og_family)

        handle_children(removed_children,added_children,changed_block,g)        
        handle_updates(updated_parents,updated_children,g)

        block_before = dict_to_file(before_ids,before_block)
        block_after = dict_to_file(changed_ids,changed_block)

        replace_updated_block_file(structure_file_path,block_before,block_after)

        cwd = os.getcwd()
        os.chdir(dataControl.find_anb())
        genealogia.gen_onto_file(g,'anbsafeonto')
        os.chdir(cwd)


### NOTES:

# get the family structure from the anbtemp file
# from there dispose the couples as blocks for the user
# enabling the user to chose a block to be changed
# verify if the block is valid
# get the block structure from the user modified block
# compare the block that was changed with the original block
# alter the anbtemp file
# alter the ontology
# alter the file system configuration

# ontology changes:
# necessary to update the children's ontology reference when they are removed and be careful cuz they can be parents in other instance of the anbtemp file
# necessary to update the parents's ontology reference  when they are removed and also be careful cuz they can be child in other instance of the anbtemp file