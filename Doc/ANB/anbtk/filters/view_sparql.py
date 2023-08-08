import inquirer
import os

from prettytable import PrettyTable

def select_names(names):
    folder_names = names
    folder_names.append("Leave")
    print("Possible correspondences:")
    questions = [
        inquirer.List('names',
                      choices=folder_names,
                      
                      ),
    ]
    answers = inquirer.prompt(questions)
    selected_name = answers['names']

    if selected_name == "Leave":
        exit()
    
    return selected_name




def select_path(paths):
    folder_names = [os.path.basename(path) for path in paths]
    folder_names.append("Leave")

    questions = [
        inquirer.List('path',
                      message="Select a folder:",
                      choices=folder_names,
                      ),
    ]
    answers = inquirer.prompt(questions)
    selected_folder_name = answers['path']

    if selected_folder_name == "Leave":
        exit()

    # Get the corresponding full path for the selected folder name
    selected_path = next(path for path in paths if os.path.basename(path) == selected_folder_name)

    return selected_path


def compose_header(initial,arguments):
    header = "The "
    for (elem,_) in arguments[:-1]:
        if elem == 'unclesaunts':
            header += "uncles and aunts of the "
        else:
            header += elem + " of the "
    elem,_ = arguments[-1]
    if elem == 'unclesaunts':
        header += f"uncles and aunts of {initial}:"
    else:
        header += elem + f" of {initial}:"
    return header  


def show_data(unique, message, header):
    table = PrettyTable([header])
    for elem in unique:
        table.add_row(["* " + elem.replace("-", " ")])
    print(table)
    print("\n" + message)