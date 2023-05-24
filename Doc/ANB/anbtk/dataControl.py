
#? This module represents all the control version of the files and entities

import json
import os

from .DSL.entities import FSGram
from .DSL.family import gramma
from .auxiliar import constants

def initanb(grampath,folderpath=""):
    cwd = os.getcwd()
    if os.path.exists(cwd + '/.anbtk'):
        
        raise Exception("This folder was already initialized as an Ancestors Notebook.")
    elif find_anb() is not None:
        raise Exception("You are already in an Ancestors Notebook")  
    else:
        os.mkdir(filepath := (cwd + '/.anbtk'))
        os.chdir(filepath)
        initData()
        

        if grampath=="":
            FSGram.initializer()
        else:
            if os.path.dirname(grampath)!='':
                os.chdir(os.path.dirname(os.path.abspath(grampath)))
            print(grampath)
            temp = open(grampath,'r').read()
            os.chdir(filepath)
            FSGram.initializer(temp)
        templateGen()
    os.chdir(cwd)




def initData():
    """
    Create an initial JSON file for storing statistics related to the types of content in the notebook.
    """

    data = {}
    
    data['Biography'] = 0
    data['Story'] = 0
    data['Picture'] = 0
    
    #  > more formats tba
    with open('anbtk.json','w') as anbtkfo:
        json.dump(data,anbtkfo)



def dataUpdate(file_type, name):

    """
    Update the count of files of a particular file type in 'anbtk.json' and return an ID for the new file.

    Args:
    - file_type (str): The type of file. Currently supported types are 'Biography' and 'Story'.
    - name (str): The name of the new file.

    Returns:
    - id (str): The ID of the new file, which is generated based on the type and count of files of that type.
    """
    
    with open('anbtk.json', 'r') as f:
        data = json.load(f)
    
    if file_type not in data:
        data[file_type] = 0
    
    data[file_type] += 1
    
    if file_type =='Biography':
        id = f"b{data[file_type]}-{name}"
    
    elif file_type == 'Story':
        id = f"h{data[file_type]}-{name}"
    
    # > more formats tba

    with open('anbtk.json', 'w') as f:
        json.dump(data, f)

    return id


def templateGen():
    """
    Generates a directory called "templates" with the different templates to be used.

    Returns:
    None
    
    Raises:
    OSError: If there is an error creating the "templates" directory or writing to the "anb1.j2" file.
    """

    os.mkdir('templates')
    os.chdir('templates')

    with open('anb1.j2','w') as f:
        f.write(constants.templateLatex)


def find_anb():
    
    """
    Returns the absolute path of the .anbtk directory if found, else returns None.
    
    The function recursively searches the current working directory and all its parent directories
    until it finds the .anbtk directory. If the .anbtk directory is found, its absolute path is returned.
    If the root directory is reached without finding the .anbtk directory, the function returns None.
    
    """
    
    current_dir = os.getcwd()
    while True:
        if os.path.isdir(os.path.join(current_dir, '.anbtk')):
            # .anb folder found
            return os.path.abspath(os.path.join(current_dir, '.anbtk'))
        new_dir = os.path.dirname(current_dir)
        if new_dir == current_dir:
            # reached root directory without finding .anb folder
            return None
        current_dir = new_dir


def search_anbtk():

    """
    Searches for the existence of an `.anbtk` folder in the current directory or any of its parent directories, and changes the working directory to the `.anbtk` folder if found. If the folder is not found, it changes the working directory back to its original location and returns False.

    Returns:
    bool:
        True if the `.anbtk` folder is found and the working directory is changed to it, False otherwise.
    """
    save = os.getcwd()
    current_dir = os.getcwd()
    while current_dir != '/':
        folder_path = os.path.join(current_dir, '.anbtk')
        if os.path.isdir(folder_path):
            os.chdir(folder_path)
            return True
        current_dir = os.path.dirname(current_dir)
    os.chdir(save)
    return False




