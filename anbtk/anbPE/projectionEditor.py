import os
import subprocess


from ..DSL.family import gramma
from ..ontology import ousia
from .. import dataControl
from .. import genealogia
from . import blocks
from . import view
from . import handlers



def unique_parent_creation(p1, p2, og_name_p1, og_name_p2, parents, children, block, ids, path, g):
    """
    Create unique parent entities in the genealogical graph and establish relationships.
    
    Parameters:
        p1 (str): Identifier of the first parent entity.
        p2 (str): Identifier of the second parent entity.
        og_name_p1 (str): Original name of the first parent entity.
        og_name_p2 (str): Original name of the second parent entity.
        parents (list): List of parent identifiers.
        children (list): List of child identifiers.
        block (dict): Dictionary containing data blocks for individuals.
        ids (dict): Dictionary containing identifier-to-data mappings.
        path (str): Path to the project data.
        g: The genealogical graph object.
        
    This function creates unique parent entities in the genealogical graph, adds attributes like birthdate, deathdate,
    and nickname to parents and children, and establishes relationships between spouses and parents and children.
    """

    genealogia.populate_graph(block, g)
    p1_bd = ids[og_name_p1]['birthDate']
    p1_dd = ids[og_name_p1]['deathDate']
    p1_nn = ids[og_name_p1]['nickname']
    p2_bd = ids[og_name_p2]['birthDate']
    p2_dd = ids[og_name_p2]['deathDate']
    p2_nn = ids[og_name_p2]['nickname']

    ousia.add_hasSpouse(p1, p2, g)
    ousia.add_birthdate(p1, p1_bd, g)
    ousia.add_deathdate(p1, p1_dd, g)
    ousia.add_nickname(p1, p1_nn, g)
    ousia.add_birthdate(p2, p2_bd, g)
    ousia.add_deathdate(p2, p2_dd, g)
    ousia.add_nickname(p2, p2_nn, g)

    genealogia.gen_parents_folders(parents, children, g, path)

    for og_child in children:
        child = genealogia.adapt_name(og_child)
        bd = ids[og_child]['birthDate']
        dd = ids[og_child]['deathDate']
        ousia.add_birthdate(child, bd, g)
        ousia.add_deathdate(child, dd, g)


def child_to_parent(individual1, og_name1, individual2, og_name2, ids, og_ids, g):
    """
    Update child-to-parent relationship and attributes based on differences in birthdate and deathdate.
    
    Parameters:
        individual1 (str): Identifier of the child individual.
        og_name1 (str): Original name of the child individual.
        individual2 (str): Identifier of the parent individual.
        og_name2 (str): Original name of the parent individual.
        ids (dict): Dictionary containing identifier-to-data mappings for the current data.
        og_ids (dict): Dictionary containing identifier-to-data mappings for the original data.
        g: The genealogical graph object.
        
    This function updates the child-to-parent relationship in the genealogical graph based on differences in birthdate
    and deathdate between the current data and original data. It also adds attributes to the parent individual.
    """
    if ids[og_name1]['birthDate'] != og_ids[og_name1]['birthDate'] or ids[og_name1]['deathDate'] != og_ids[og_name1]['deathDate']:
        print(
            f"There are year differences for {og_name1}, the original birthdate and deathdate will be preserved. To change use the projection editor - anbpe.")
        print("parent 1 is a child")
        bd = ids[og_name2]['birthDate']
        dd = ids[og_name2]['deathDate']
        ousia.add_complete_individual(individual2, og_name2, bd, dd, g)
        ousia.add_hasSpouse(individual1, individual2, g)

# check for existing parents


def anb_raw_init(block, id, root):
    """
    Initialize an Ancestors Notebook (ANB) project with raw data and create an ontology.
    
    Parameters:
        block (dict): Dictionary containing data blocks for individuals.
        id (str): Identifier for the current data.
        root (str): Root directory path for the ANB project.
        
    This function initializes an Ancestors Notebook project with raw data from the given data block and identifier.
    It creates an ANB temporary file, performs raw initialization of the genealogical graph, and generates an ontology.
    """

    new_couple_str = blocks.dict_to_file(block, id)
    dot_anbtk = dataControl.find_anb()

    with open(f'{dot_anbtk}/anbtemp.txt', 'w') as anbtemp:
        anbtemp.write(new_couple_str)
    os.chdir(root)
    root = os.path.basename(root)
    g = genealogia.raw_initialization('anbtemp.txt', root)

    dataControl.search_anbtk()
    genealogia.gen_onto_file(g, 'anbsafeonto')


def add_couple():
    """
    Add a new couple to the Ancestors Notebook project.
    
    This function handles the addition of a new couple to the genealogical graph of the Ancestors Notebook project.
    It checks if the project is initialized, reads existing data if available, and handles various cases such as
    adding new parents, linking existing parents, or adding children. It also updates data blocks and ontology files.
    """
    if dataControl.find_anb() is None:
        print("You are not in an initialized Ancestors Notebook.")
        exit()
    root = dataControl.get_root()
    os.chdir(root)
    path = os.path.basename(root)

    verify_anbtemp = False
    if os.path.exists(os.path.join(root, '.anbtk/anbtemp.txt')):
        structure_file_path = os.path.join(root, '.anbtk/anbtemp.txt')
        verify_anbtemp = True
    if os.path.exists(os.path.join(root, '.anbtk/anbsafeonto.rdf')):
        onto_file_path = os.path.join(root, '.anbtk/anbsafeonto.rdf')

    new_couple_block = blocks.edit_block('')
    new_couple_block = blocks.add_newlines(new_couple_block)
    block, ids = gramma.check_parsing(new_couple_block)
    if block is None:
        exit()

    if not verify_anbtemp:
        anb_raw_init(block, ids, root)

    else:
        g = genealogia.read_onto_file(onto_file_path)

        parents = list(block.keys())[0]
        children = list(block.values())[0]

        og_name_p1, og_name_p2 = parents.split("+")
        og_family, og_ids = gramma.parsing(structure_file_path)
        all_parents = list(og_family.keys())
        p1_is_child, p2_is_child, p1_is_parent, p2_is_parent = False, False, False, False

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
            unique_parent_creation(
                p1, p2, og_name_p1, og_name_p2, parents, children, block, ids, path, g)
        else:
            if not p2_is_child and not p2_is_parent:
                if not all([p1_is_child, p1_is_parent]):
                    child_to_parent(p1, og_name_p1, p2,
                                    og_name_p2, ids, og_ids, g)
            elif not p1_is_child and not p1_is_parent:
                if not all([p2_is_child, p2_is_parent]):
                    child_to_parent(p2, og_name_p2, p1,
                                    og_name_p1, ids, og_ids, g)
            elif not all([p1_is_child, p1_is_parent]) and not all([p2_is_child, p2_is_parent]):

                if og_name_p2 in handlers.get_children_parent(og_family, og_name_p1) or og_name_p1 in handlers.get_children_parent(og_family, og_name_p2):
                    print("It's not possible from a child and a parent to marry!")
                    exit()

                ousia.add_hasSpouse(p1, p2, g)
                if ids[og_name_p1]['birthDate'] != og_ids[og_name_p1]['birthDate']:
                    print(
                        f"Warning: different dates specified for {og_name_p1}")
                if ids[og_name_p2]['birthDate'] != og_ids[og_name_p2]['birthDate']:
                    print(
                        f"Warning: different dates specified for {og_name_p2}")

            genealogia.gen_parents_folders(parents, children, g, path)
            for og_child in children:
                if og_child in parent_children['children']:
                    print(
                        f"{og_child} is already referenced as someone's child before.")
                    exit()
                child = genealogia.adapt_name(og_child)
                bd = ids[og_child]['birthDate']
                dd = ids[og_child]['deathDate']
                ousia.add_complete_individual(child, og_child, bd, dd, g)
                ousia.add_parent_children(p1, p2, child, g)

        blocks.add_new_dict_block_file(structure_file_path, block, ids)
        genealogia.gen_onto_file(g, dataControl.find_anb() + '/anbsafeonto')


def handle_changes(new_parent, removed_parent, updated_parents, added_children, removed_children, updated_children, updated_geral_block, changed_block, og_family, g):
    """
    Handle changes in parent-child relationships and individual attributes within a family.
    
    Parameters:
        new_parent (list): List of new parent entities.
        removed_parent (list): List of removed parent entities.
        updated_parents (list): List of updated parent entities.
        added_children (list): List of added child entities.
        removed_children (list): List of removed child entities.
        updated_children (list): List of updated child entities.
        updated_geral_block (dict): Updated general data block.
        changed_block (dict): Dictionary containing changed data blocks.
        og_family (dict): Original family data.
        g: The genealogical graph object.
        
    This function handles various changes within a family structure, including adding new parents and child entities,
    removing parents and children, updating parent and child attributes, and updating the general data block. It
    updates the genealogical graph accordingly.
    """
    if new_parent != []:
        handlers.handler_new_parents(new_parent, g)
        handlers.handler_add_new_parent_folders(
            new_parent, updated_geral_block, g)
    if removed_parent != []:
        handlers.handler_removed_parent_folders(removed_parent, og_family)
    if added_children != [] or removed_children != []:
        handlers.handler_children(
            removed_children, added_children, changed_block, og_family, g)
    if updated_parents != [] or updated_children != []:
        handlers.handler_updates(updated_parents, updated_children, g)
        for parent in updated_parents:
            print(parent)


def handle_changes_other_references(updated_parents, updated_children, og_family, og_ids):
    if updated_parents != [] or updated_children != []:
        if updated_parents != []:
            for parent_dic in updated_parents:
                parent_name = list(parent_dic.keys())[0]
                og_ids[parent_name]['birthDate'] = parent_dic[parent_name]['birthDate']
                og_ids[parent_name]['deathDate'] = parent_dic[parent_name]['deathDate']
                og_ids[parent_name]['nickname'] = parent_dic[parent_name]['nickname']
        if updated_children != []:
            for child_dic in updated_children:
                child_name = list(child_dic.keys())[0]
                og_ids[child_name]['birthDate'] = child_dic[child_name]['birthDate']
                og_ids[child_name]['deathDate'] = child_dic[child_name]['deathDate']
                og_ids[child_name]['nickname'] = child_dic[child_name]['nickname']

        existing_ids_update = blocks.dict_to_file(og_family, og_ids)

        with open(dataControl.find_anb() + '/anbtemp.txt', 'w') as anbtemp:
            anbtemp.write(existing_ids_update)


def action():
    """
    Perform the editing action within the Ancestors Notebook project.
    
    This function is responsible for handling interactions and changes within the Ancestors Notebook project.
    It allows users to interactively edit and modify data blocks, handles changes in parents and children, updates
    the genealogical graph while updating the ontology file accordingly.
    """

    onto_file_path = os.path.join(
        dataControl.get_root(), '.anbtk/anbsafeonto.rdf')
    anbtemp_path = os.path.join(dataControl.get_root(), '.anbtk/anbtemp.txt')

    while True:
        subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)
        og_family, og_ids = gramma.parsing(anbtemp_path)
        block_number = view.interaction(og_family)
        selected_key = list(og_family.keys())[block_number-1]
        block = view.retrieve_content_by_name(anbtemp_path, selected_key)
        before_block, before_ids = gramma.check_parsing(blocks.add_newlines(block))
        modified_block = blocks.edit_block(block)
        modified_block = blocks.add_newlines(modified_block)
        changed_block, changed_ids = gramma.check_parsing(modified_block)

        changed_block_values, changed_block_keys = blocks.changed(
            before_block, changed_block)
        new_parent, removed_parent, updated_parents, added_children, removed_children, updated_children = blocks.updates(
            before_block, changed_ids, before_ids, changed_block_values, changed_block_keys)

        unedited_geral_block, unedited_geral_ids = blocks.remaining_blocks(
            anbtemp_path, before_block)
        updated_geral_block = blocks.new_block(unedited_geral_block, changed_block)

        g = genealogia.read_onto_file(onto_file_path)
        handle_changes(new_parent, removed_parent, updated_parents, added_children,
                    removed_children, updated_children, updated_geral_block, changed_block, og_family, g)
        handle_changes_other_references(
            updated_parents, updated_children, og_family, og_ids)

        block_before = blocks.dict_to_file(before_block, before_ids)

        block_after = blocks.dict_to_file(changed_block, changed_ids)

        blocks.replace_updated_block_file(anbtemp_path, block_before, block_after)

        if new_parent != [] or removed_parent != [] or updated_parents != [] or added_children != [] or removed_children != [] or updated_children != []:
            genealogia.gen_onto_file(g, dataControl.find_anb()+'/anbsafeonto')
