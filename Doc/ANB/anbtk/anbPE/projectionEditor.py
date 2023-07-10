import os 


from ..DSL.family import gramma
from ..ontology import ousia
from .. import dataControl
from .. import genealogia
from . import blocks
from . import view
from . import handlers

# dbfile for db 
       
#! CLEAR OS.CHDIR
#! elements that already exist are still not handled, except when they are children of someone
#! do a changer that checks the dates for "inconsistencias" if they are, change for the originals, as it is intended

def unique_parent_creation(p1,p2,og_name_p1,og_name_p2,parents,children,block,ids,path,g):
    print("unique parents")
    genealogia.populate_graph(block,g)
    p1_bd = ids[og_name_p1]['birthDate']
    p1_dd = ids[og_name_p1]['deathDate']
    p1_nn = ids[og_name_p1]['nickname']
    p2_bd = ids[og_name_p2]['birthDate']
    p2_dd = ids[og_name_p2]['deathDate']
    p2_nn = ids[og_name_p2]['nickname']
    
    ousia.add_hasSpouse(p1,p2,g)
    ousia.add_birthdate(p1,p1_bd,g)
    ousia.add_deathdate(p1,p1_dd,g)
    ousia.add_nickname(p1,p1_nn,g)
    ousia.add_birthdate(p2,p2_bd,g)
    ousia.add_deathdate(p2,p2_dd,g)
    ousia.add_nickname(p2,p2_nn,g)

    genealogia.gen_parents_folders(parents,children,g,path)

    for og_child in children:
            child = genealogia.adapt_name(og_child)
            bd = ids[og_child]['birthDate']
            dd = ids[og_child]['deathDate']
            ousia.add_birthdate(child,bd,g)
            ousia.add_deathdate(child,dd,g) 

def child_to_parent(individual1,og_name1,individual2,og_name2,ids,og_ids,g):
    if ids[og_name1]['birthDate']!=og_ids[og_name1]['birthDate'] or ids[og_name1]['deathDate']!=og_ids[og_name1]['deathDate']:
            print(f"There are year differences for {og_name1}, the original birthdate and deathdate will be preserved. To change use the projection editor - anbpe.")
            print("parent 1 is a child")
            bd = ids[og_name2]['birthDate']
            dd = ids[og_name2]['deathDate']
            ousia.add_complete_individual(individual2,og_name2,bd,dd,g)
            ousia.add_hasSpouse(individual1,individual2,g)

# check for existing parents


def anb_raw_init(block,id,root):
    new_couple_str = blocks.dict_to_file(block,id)
    dot_anbtk = dataControl.find_anb()

    with open(f'{dot_anbtk}/anbtemp.txt','w') as anbtemp:
        anbtemp.write(new_couple_str)
    os.chdir(root)
    g = genealogia.raw_initialization('anbtemp.txt',root)

    dataControl.search_anbtk()
    genealogia.gen_onto_file(g,'anbsafeonto')


def add_couple():
    if dataControl.find_anb() == None:
        print("You are not in an initialized Ancestors Notebook.")
        exit()
    root = dataControl.get_root()
    os.chdir(root)
    path = os.path.basename(root)

    verify_anbtemp = False
    if os.path.exists(os.path.join(root,'.anbtk/anbtemp.txt')):
        structure_file_path = os.path.join(root,'.anbtk/anbtemp.txt')
        verify_anbtemp = True
    if os.path.exists(os.path.join(root,'.anbtk/anbsafeonto.rdf')):
        onto_file_path = os.path.join(root,'.anbtk/anbsafeonto.rdf')
    
    new_couple_block = blocks.edit_block('')
    new_couple_block = blocks.add_newlines(new_couple_block)
    block, ids = gramma.check_parsing(new_couple_block)    
    if block == None :
        exit()        
    
    if not verify_anbtemp:
        anb_raw_init(block,ids,root)


    else:
        g = genealogia.read_onto_file(onto_file_path)
    
        parents = list(block.keys())[0]
        children = list(block.values())[0]

        og_name_p1,og_name_p2 = parents.split("+")
        og_family, og_ids = gramma.parsing(structure_file_path)
        all_parents = list(og_family.keys())
        p1_is_child,p2_is_child,p1_is_parent,p2_is_parent = False,False,False,False

        parent_children = handlers.parents_kids(og_family)

        if og_name_p1 in parent_children['parents']:
            p1_is_parent = True
        if og_name_p1 in parent_children['children']:
            p1_is_child = True
        if og_name_p2 in parent_children['parents']:
            p2_is_parent = True
        if og_name_p2 in parent_children['children']:
            p2_is_child = True
    
        p1 = genealogia.adapt_name(og_name_p1)
        p2 = genealogia.adapt_name(og_name_p2)


        if f"{og_name_p1}+{og_name_p2}" in all_parents or f"{og_name_p2}+{og_name_p1}" in all_parents:
            print(f"The couple '{og_name_p1} + {og_name_p2} ' already exists!")
            exit()

        if not p1_is_child and not p2_is_child and not p1_is_parent and not p2_is_parent:
            #both parents didnt exist
            unique_parent_creation(p1,p2,og_name_p1,og_name_p2,parents,children,block,ids,path,g)             
        else:
            if not p2_is_child and not p2_is_parent:
                # if p1 is either a child or a parent, meaning that it exists; note : all[True,False] = False
                if not all([p1_is_child,p1_is_parent]):
                    child_to_parent(p1,og_name_p1,p2,og_name_p2,ids,og_ids,g)          
            elif not p1_is_child and not p1_is_parent:
                if not all([p2_is_child,p2_is_parent]):
                    child_to_parent(p2,og_name_p2,p1,og_name_p1,ids,og_ids,g)
            elif not all([p1_is_child,p1_is_parent]) and not all([p2_is_child,p2_is_parent]):
                
                if og_name_p2 in handlers.get_children_parent(og_family,og_name_p1) or og_name_p1 in handlers.get_children_parent(og_family,og_name_p2) :
                    print("It's not possible from a child and a parent to marry!")
                    exit()
                print("just newly created couple")                
                
                #both exist like kids
                ousia.add_hasSpouse(p1,p2,g)
                if ids[og_name_p1]['birthDate'] != og_ids[og_name_p1]['birthDate']:
                    print(f"Warning: different dates specified for {og_name_p1}")
                if ids[og_name_p2]['birthDate'] != og_ids[og_name_p2]['birthDate']:
                    print(f"Warning: different dates specified for {og_name_p2}")
                
            

            genealogia.gen_parents_folders(parents,children,g,path)        
            for og_child in children:
                if og_child in parent_children['children']:
                    print(f"{og_child} is already referenced as someone's child before.")
                    exit()
                child = genealogia.adapt_name(og_child)
                bd = ids[og_child]['birthDate']
                dd = ids[og_child]['deathDate']
                ousia.add_complete_individual(child,og_child,bd,dd,g)
                ousia.add_parent_children(p1,p2,child,g)

        blocks.add_new_dict_block_file(structure_file_path,block,ids)
        # cwd = os.getcwd()
        # os.chdir(dataControl.find_anb())
        genealogia.gen_onto_file(g,dataControl.find_anb() + '/anbsafeonto')
        # os.chdir(cwd)

def handle_changes(new_parent,removed_parent,updated_parents,added_children,removed_children,updated_children,updated_geral_block,changed_block,og_family,g):
    if new_parent != []:
        handlers.handler_new_parents(new_parent,g)
        handlers.handler_add_new_parent_folders(new_parent,updated_geral_block,g)
    if removed_parent!=[]:
        handlers.handler_removed_parent_folders(removed_parent,og_family)
    if added_children != [] or removed_children!=[]:    
        handlers.handler_children(removed_children,added_children,changed_block,og_family,g)        
    if updated_parents != [] or updated_children != []:
        handlers.handler_updates(updated_parents,updated_children,g)

#! needs more testing
import subprocess

def action():
    onto_file_path = os.path.join(dataControl.get_root(),'.anbtk/anbsafeonto.rdf')
    structure_file_path = os.path.join(dataControl.get_root(),'.anbtk/anbtemp.txt')
    

    
    while True:
        subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)
        og_family, og_ids = gramma.parsing(structure_file_path)
        block_number = view.interaction(og_family)
        key = list(og_family.keys())[block_number-1]
        block = view.retrieve_content_by_name(structure_file_path,key)
        before_block,before_ids = gramma.check_parsing(blocks.add_newlines(block))
        modified_block = blocks.edit_block(block)
        modified_block = blocks.add_newlines(modified_block)
        changed_block,changed_ids = gramma.check_parsing(modified_block)
        # print(changed_block)
        # print(changed_ids)

        
        values,keys = blocks.changed(before_block,changed_block)
        new_parent,removed_parent,updated_parents, added_children, removed_children, updated_children = blocks.updates(before_block,changed_ids,before_ids,values,keys)
        
        unedited_geral_block = blocks.remaining_blocks(structure_file_path,before_block)
        updated_geral_block = blocks.new_block(unedited_geral_block,changed_block)

        # print("****** new parents ***********")
        # print(new_parent)
        # print("*******removed parents`*******")
        # print(removed_parent)
        # print("*****updated parents******")
        # print(updated_parents)
        # print("*****added children******")
        # print(added_children)
        # print("****** removed children ******")
        # print(removed_children)
        # print("****** updated children ******")
        # print(updated_children)
        
        g = genealogia.read_onto_file(onto_file_path)
        handle_changes(new_parent,removed_parent,updated_parents,added_children,removed_children,updated_children,updated_geral_block,changed_block,og_family,g)

        block_before = blocks.dict_to_file(before_block,before_ids)
        block_after = blocks.dict_to_file(changed_block,changed_ids)

        blocks.replace_updated_block_file(structure_file_path,block_before,block_after)

        
        if new_parent!=[] or removed_parent!=[] or updated_parents!=[] or added_children!=[] or removed_children!=[] or updated_children !=[]:
            genealogia.gen_onto_file(g,dataControl.find_anb()+'/anbsafeonto')


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