import subprocess
import os 
import time

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
    print("Launching text editor for modification...")

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

def get_changes(original_dict, updated_dict):
    changes = {}

    for key in original_dict:
        if key not in updated_dict:
            changes[key] = 'Key removed'
        else:
            original_values = original_dict[key]
            updated_values = updated_dict[key]

            if original_values != updated_values:
                added_values = [value for value in updated_values if value not in original_values]
                removed_values = [value for value in original_values if value not in updated_values]

                if added_values or removed_values:
                    changes[key] = {
                        'Added values': added_values,
                        'Removed values': removed_values
                    }

    for key in updated_dict:
        if key not in original_dict:
            changes[key] = 'Key added'

    return changes




def convert_dictionary(dictionary):
    for key, values in dictionary.items():
        print(key)
        for value in values:
            print(f". {value}")

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
        string += key + '\n'
        for value in values:
            string += '.' + value + '\n'
    return string

def retrieve_content_by_name(file_path, name):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        found = False
        content = []
        for line in lines:
            line = line.strip()
            if line == name:
                found = True
            elif found and line.startswith('.'):
                content.append(line[2:])
            elif found:
                break
    return '\n'.join(content)


def action():
    with open('complexfam.txt', 'r') as file:
        original_config_data = file.read()

    og_family, og_dates = DSL.family.gramma.parsing('complexfam.txt')
    block_number = interaction(og_family)
    key = list(og_family.keys())[block_number-1]



    
    print(block)
    

    
    
    
    
    
    #new_family,new_dates = DSL.family.gramma.check_parsing(modified_config_data)

    #changes = get_changes(og_family,new_family)
    #print(changes)
    #check_errors(modified_config_data)



action()