import os
import shutil

from .. import dataControl

# def list_and_num_families(dictionary):
#     """

#     This function takes the dictionary generated after processing the seed file.
#     It iterates over the dictionary, printing each couple and their children with its associated number.

#     Args:
#         dictionary (dict): The dictionary of families and their members.
#     """
    
#     for i, key in enumerate(dictionary, start=1):
#         print(f"{i}.     {key}")
#         for element in dictionary[key]:
#             print(f"        * {element}")
#         print("\n")
#     print("0. Leave\n")


terminal_width = shutil.get_terminal_size().columns
divider = "=" * terminal_width


def normalize_string(input_str):
    if not input_str:
        return ""

    # Convert the first character to uppercase and the rest to lowercase
    normalized_str = input_str[0].upper() + input_str[1:].lower()
    return normalized_str

def list_and_num_families(dictionary):
    """
    This function takes a dictionary generated from processing a seed file.
    It iterates over the dictionary and prints each family, along with its members and associated number.

    Args:
        dictionary (dict): The dictionary of families and their members.
    """
    family_name = normalize_string(os.path.basename(dataControl.get_root()))
    title = f"{family_name}'s Ancestors NoteBook:".center(terminal_width)
    print(divider)
    print()
    print(title)
    print(divider)
    
    for i, key in enumerate(dictionary, start=1):
        print(f"{i}. {key}")
        
        for element in dictionary[key]:
            print(f"   - {element}")
            
        print("\n")
    
    print("0. Leave\n")





def interaction(og_family):
    """
    Manages the interaction and user input for choosing a family block to edit.

    Args:
        og_family (dict): The original family dictionary.

    Returns:
        int: The number of the chosen block.
    """

    length = len(og_family.keys())
    while True:
        try:
            list_and_num_families(og_family)
            print(divider)
            number = int(input("Choose a block to be edited: "))
            if 0 < number <= length:
                return number
            elif number == 0:
                exit(0)
            else:
                print(f"Number should be between 0 and {length}. Try again.")
        except ValueError:
            print("\n> Invalid input. Please enter a number.")
    



def visual_dictionary_simple(dictionary):
    """
    Converts a dictionary to a simplified string representation.

    This function takes in a dictionary and converts it into a string representation.
    It concatenates the dictionary keys and values into a single string.

    Args:
        dictionary (dict): The dictionary to convert.

    Returns:
        str: The simplified string representation of the dictionary.
    """
    string = ''
    for key, values in dictionary.items():
        string += key
        for value in values:
            string += value
    return string



def retrieve_content_by_name(file_path, name):
    """
    Retrieves the content by name from a file.

    This function takes in a file path and a name to search for.
    It reads the contents of the file, searches for the specified name,
    and retrieves the content associated with the name. The content is returned
    as a simplified string representation using the 'visual_dictionary_simple()' function.

    Args:
        file_path (str): The file path.
        name (str): The name to search for.

    Returns:
        str: The retrieved content as a simplified string representation.
    """
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