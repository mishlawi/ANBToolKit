import os 

from pathlib import Path

from ..DSL.family import gramma
from ..ontology import ousia
from .. import dataControl
from .. import genealogia
from . import blocks
from . import view

# dbfile for db 

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

def parents_kids(block):
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
            
def get_parents(individual,block):
    for parents,children in block.items():
        if individual in children:
            return parents.split("+")


def handle_new_parents(new_parent,g):
    for parent in new_parent:
        old = genealogia.adapt_name(parent[0])
        new  = parent[1]
        parent_name = list(new.keys())[0]
        parent_bd = new[parent_name]['birthDate']
        parent_dd = new[parent_name]['deathDate']

        ousia.switch_individual(old,genealogia.adapt_name(parent_name),parent_name,parent_bd,parent_dd,g)

# add folders
# remove folders from removed children and symlinks
#
def handle_children(removed_children,added_children,changed_block,og_block,g):
    
    cwd = os.getcwd()
    os.chdir(dataControl.get_root())
    p1,p2 = list(changed_block.keys())[0].split("+")

    p_k = parents_kids(changed_block)
    for elem in removed_children:
        ousia.delete_children_individual(genealogia.adapt_name(elem),g)

        if elem not in p_k['parents']:
            print("not a parent")
            warning(genealogia.adapt_name(elem))
            os.rmdir(genealogia.adapt_name(elem))
        parents = get_parents(elem,og_block)
        p1,p2 = parents
        p1 = genealogia.adapt_name(p1)
        p2 = genealogia.adapt_name(p2)
        if os.path.exists(f".{p1}+{p2}"):
            elem = genealogia.adapt_name(elem)
            os.unlink(f".{p1}+{p2}/{elem}")
        
            

    for elem in added_children:
        og_name = list(elem.keys())[0]
        bd = elem[og_name]['birthDate']
        dd = elem[og_name]['deathDate']
        individual = genealogia.adapt_name(og_name)
        ousia.add_individual(individual,og_name,g)
        ousia.add_birthdate(individual,bd,g)
        ousia.add_deathdate(individual,dd,g)
        ousia.add_parent_children(genealogia.adapt_name(p1),genealogia.adapt_name(p2),individual,g)
        # add folder
    os.chdir(cwd)
def handle_add_new_parent_folders(new_parents,updated_block,g):
    path = dataControl.get_root()
    cwd = os.getcwd()
    os.chdir(path)
    for new_parent in new_parents:
        for couple in updated_block.keys():
            if list(new_parent[1].keys())[0] in couple:
                genealogia.gen_parents_folders(couple,updated_block[couple],g,path)

    os.chdir(cwd)    


def is_folder_empty(folder_path):
    folder = Path(folder_path)
    for entry in folder.iterdir():
        if entry.is_file() or entry.is_dir():
            return False
    return True

def warning(folder_path):
    if not is_folder_empty(folder_path):
        print(f"There is still data in {folder_path} folder. Please move or remove it and manually delete the folder.") 
        exit()


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
                print("yess")
                p1,p2 = parents.split("+")
                p1 = genealogia.adapt_name(p1)
                p2 = genealogia.adapt_name(p2)
                os.unlink(genealogia.adapt_name(rm_parent)+'/'+ f'.{p1}+{p2}')
                os.unlink(p2+'/'+ f'.{p1}+{p2}')
                for child in children:
                    if not child.startswith("undiscovered"):
                        os.unlink(f".{p1}+{p2}"+'/'+genealogia.adapt_name(child))
                os.rmdir(f".{p1}+{p2}")
        if not is_child:
            path = genealogia.adapt_name(rm_parent)
            warning(path)
            os.rmdir(genealogia.adapt_name(rm_parent))
    os.chdir(cwd)
        
            

#! elements that already exist are still not handled, except when they are children of someone
#! do a changer that checks the dates for "inconsistencias" if they are, change for the originals, as it is intended
def add_couple():
    path = dataControl.get_root()
    cwd = os.getcwd()
    os.chdir(path)
    path = os.path.basename(path)

    onto_file_path = os.path.join(dataControl.get_root(),'.anbtk/anbsafeonto.rdf')
    structure_file_path = os.path.join(dataControl.get_root(),'.anbtk/anbtemp.txt')
    g = genealogia.read_onto_file(onto_file_path)

    new_couple_block = blocks.edit_block('')
    new_couple_block = blocks.add_newlines(new_couple_block)
    block, ids = gramma.check_parsing(new_couple_block)
    
    if block == None :
        exit()
        
    parents = list(block.keys())[0]
    children = list(block.values())[0]

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
        p1_bd = ids[og_name_p1]['birthDate']
        p1_dd = ids[og_name_p1]['deathDate']
        p2_bd = ids[og_name_p2]['birthDate']
        p2_dd = ids[og_name_p2]['deathDate']
        
        ousia.add_birthdate(p1,p1_bd,g)
        ousia.add_deathdate(p1,p1_dd,g)
        ousia.add_birthdate(p2,p2_bd,g)
        ousia.add_deathdate(p2,p2_dd,g)
        genealogia.gen_parents_folders(parents,children,g,path)

        for og_child in children:
                child = genealogia.adapt_name(og_child)
                bd = ids[og_child]['birthDate']
                dd = ids[og_child]['deathDate']
                ousia.add_birthdate(child,bd,g)
                ousia.add_deathdate(child,dd,g)              
    else:
        if p1_is_child:
            if ids[og_name_p1]['birthDate']!=og_dates[og_name_p1]['birthDate'] or ids[og_name_p1]['deathDate']!=og_dates[og_name_p1]['deathDate']:
                print(f"There are some date differences for {og_name_p1}, the original birthdate and deathdate will be preserved. To change use the projection editor - anbpe.")
            print("parent 1 is a child")
            bd = ids[og_name_p2]['birthDate']
            dd = ids[og_name_p2]['deathDate']
            ousia.add_complete_individual(p2,og_name_p2,bd,dd,g)
            ousia.add_hasSpouse(p1,p2,g)
            
        elif p2_is_child:
            if ids[og_name_p1]['birthDate']!=og_dates[og_name_p1]['birthDate'] or ids[og_name_p1]['deathDate']!=og_dates[og_name_p1]['deathDate']:
                print(f"There are some date differences for {og_name_p1}, the original birthdate and deathdate will be preserved. To change use the projection editor - anbpe.")

            print("parent 2 is a child")
            bd = ids[og_name_p1]['birthDate']
            dd = ids[og_name_p1]['deathDate']
            ousia.add_complete_individual(p1,og_name_p1,bd,dd,g)
            ousia.add_hasSpouse(p2,p1,g)

        genealogia.gen_parents_folders(parents,children,g,path)        
        for og_child in children:
                child = genealogia.adapt_name(og_child)
                bd = ids[og_child]['birthDate']
                dd = ids[og_child]['deathDate']
                ousia.add_complete_individual(child,og_child,bd,dd,g)
                ousia.add_parent_children(p1,p2,child,g)

    blocks.add_new_dict_block_file(structure_file_path,block,ids)
    cwd = os.getcwd()
    os.chdir(dataControl.find_anb())
    genealogia.gen_onto_file(g,'anbsafeonto')
    os.chdir(cwd)


#! needs more testing
def action():
    onto_file_path = os.path.join(dataControl.get_root(),'.anbtk/anbsafeonto.rdf')
    structure_file_path = os.path.join(dataControl.get_root(),'.anbtk/anbtemp.txt')
    
    og_family, og_dates = gramma.parsing(structure_file_path)


    block_number = view.interaction(og_family)
    key = list(og_family.keys())[block_number-1]
    block = view.retrieve_content_by_name(structure_file_path,key)
    before_block,before_ids = gramma.check_parsing(blocks.add_newlines(block))
    modified_block = blocks.edit_block(block)
    modified_block = blocks.add_newlines(modified_block)
    changed_block,changed_ids = gramma.check_parsing(modified_block)

    
    values,keys = blocks.changed(before_block,changed_block)
    new_parent,removed_parent,updated_parents, added_children, removed_children, updated_children = blocks.updates(before_block,changed_ids,before_ids,values,keys)
    
    unedited_geral_block = blocks.remaining_blocks(structure_file_path,before_block)
    updated_geral_block = blocks.new_block(unedited_geral_block,changed_block)

    print("****** new parents ***********")
    print(new_parent)
    print("*******removed parents`*******")
    print(removed_parent)
    print("*****updated parents******")
    print(updated_parents)
    print("*****added children******")
    print(added_children)
    print("****** removed children ******")
    print(removed_children)
    print("****** updated children ******")
    print(updated_children)

    if new_parent != [] or updated_parents!= [] or added_children != [] or removed_children != [] or updated_children!=[]:
        

        g = genealogia.read_onto_file(onto_file_path)
        

        handle_new_parents(new_parent,g)
        handle_add_new_parent_folders(new_parent,updated_geral_block,g)
        handle_removed_parent_folders(removed_parent,og_family)

        handle_children(removed_children,added_children,changed_block,og_family,g)        
        handle_updates(updated_parents,updated_children,g)

        block_before = blocks.dict_to_file(before_ids,before_block)
        block_after = blocks.dict_to_file(changed_ids,changed_block)

        blocks.replace_updated_block_file(structure_file_path,block_before,block_after)

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