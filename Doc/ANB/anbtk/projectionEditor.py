import subprocess
import os 

from rdflib import Graph
import DSL.family.gramma


def get_file():
    #change to the seed file
    #with open(os.path.join(get_root(),'anbtemplate.txt')) as template:
    with open('complexfam.txt') as template:
        file = template.read()
    print(file)

def list_and_num_families(dictionary):
    
    for i, key in enumerate(dictionary, start=1):
        print(f"{i}.     {key}")
        for element in dictionary[key]:
            print(f"        * {element}")
        print("\n")
    print("0. Leave\n")




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
        modified_config_data = temp_file.read()

    # Remove the temporary file
    os.remove(temp_filename)

    return modified_config_data

def check_errors(modified_config_data):
    DSL.family.gramma.check_parsing(modified_config_data)

def changed(dict1,dict2):
    if len(dict1)>1:
        raise Exception("Something went wrong")
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
    
def write_dictionary_to_file(dictionary):
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
                return write_dictionary_to_file(content)
                
    
    return 


def id_changes(dict1,dict2):
    
    removed = list(set(dict1.keys()) - set(dict2.keys()))

# Find keys present in dict2 but not in dict1
    added = list(set(dict2.keys()) - set(dict1.keys()))

    # Find keys present in both dictionaries
    common = list(set(dict1.keys()).intersection(dict2.keys()))

    # Find differences in values for common keys
    differences = {}
    for key in common:
        if dict1[key] != dict2[key]:
            differences[key] = (dict1[key], dict2[key])
    return {'added': added, 'removed' : removed , 'common' : common, 'differences' : differences }
    return added,removed, common, differences
    


# José Augusto Santos (1947 2019) + Susana Rodrigues  (1956 -)
# .Rui Miguel Santos Ferreira (1970 -)
# .Silvana Isabel Santos Ferreira (1973 -)


#{'added': ['Esteves Cardoso', 'Bordalo Santos'], 'removed': ['undiscovered_3', 'Ricardo Esteves Cardoso'], 'common': ['Pedro Esteves', 'José Augusto Santos', 'Ana Sofia Mendes', 'Luciana Abreu Loureiro'], 'differences': {}}

# {'removed': ['undiscovered_3'], 'added': ['Bordalo Santos']}
# {'new': 'Esteves Cardoso+Luciana Abreu Loureiro', 'old': 'Ricardo Esteves Cardoso+Luciana Abreu Loureiro'}
def updates(before_block,changed_ids,before_ids, values , keys):
    print(before_block)
    new_parent = []
    updated_parent = []
    if keys!={}:
        new_key = keys['new']
        old_key = keys['old']

        new_p1, new_p2 = new_key.split("+")
        old_p1 , old_p2 = old_key.split("+")
        if new_p1 == old_p1 and new_p2 != old_p2:
            new_parent = [{new_p2 : changed_ids[new_p2]}]
        elif new_p1 != old_p1 and new_p2 == old_p2:
            new_parent = [{new_p1 : changed_ids[new_p1]}]
        elif new_p1 != old_p1 and new_p2 != old_p2:
            new_parent = [{new_p1 : changed_ids[new_p1]},{new_p2 : changed_ids[new_p2]}]
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
    if (removed := values['removed']) != [] and (added := values['added']) != [] :
        for elem in before_ids.keys():
            print(elem)
            if before_ids[elem] != changed_ids[elem]:
                updated_children.append({elem:changed_ids[elem]})

    return new_parent,updated_parent,added_children,removed_children
            


def add_newlines(string):
    string = string.rstrip('\n')
    return string + '\n\n'


def action(g):
    # with open('complexfam.txt', 'r') as file:
    #     original_config_data = file.read()
    print(g)
    og_family, og_dates = DSL.family.gramma.parsing('complexfam.txt')
    print(og_family)
    block_number = interaction(og_family)
    key = list(og_family.keys())[block_number-1]
    block = add_newlines(retrieve_content_by_name('complexfam.txt',key))
    before_block,before_ids = DSL.family.gramma.check_parsing(block)
    modified_config_data = edit_block(block)
    modified_config_data = add_newlines(modified_config_data)
    changed_block,changed_ids = DSL.family.gramma.check_parsing(modified_config_data)
    
    
    del before_ids['total']
    del before_ids['undiscovered']
    del changed_ids['total']
    del changed_ids['undiscovered']
    
    # print(id_changes(before_ids,changed_ids))
    values,keys = changed(before_block,changed_block)
    print(updates(before_block,changed_ids,before_ids,values,keys))
    # if keys == {}:
    #     #update values only
    #     for elem in values['added'] , changed_ids:
        
        
     
    # else:
    #     #keys and values update
    #     pass

    
    
    
    

    
    
    
    
    
    #new_family,new_dates = DSL.family.gramma.check_parsing(modified_config_data)

    #changes = get_changes(og_family,new_family)
    #print(changes)
    #check_errors(modified_config_data)

### to be passed to genealogia
def adapt_name(name):
    
    name = name.replace(" ","-")
    return name
    


def read_onto_file(filename):
    g = Graph()
    g.parse(filename,format="xml")

    return g 

 

g = read_onto_file('anbsafeonto.rdf')
action(g)