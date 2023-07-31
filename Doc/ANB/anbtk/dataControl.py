
#? This module represents all the control version of the files and entities

from pathlib import Path
import json
import os

from .DSL.entities import FSGram
from .auxiliar import constants
from .auxiliar import dgu_helper
from .DSL.entities import gramLogic


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


def initanb(grampath="",folderpath=""):
    cwd = os.getcwd()
    if not os.path.exists(cwd + "/.anbtk/anbtemp.txt"):
        if os.path.exists(cwd + '/.anbtk'):
            print("✗ This folder was already initialized as an Ancestors Notebook or there might be an existing anb with the default name.")
            exit()
        elif find_anb() is not None:
            print("✗ You are already in an Ancestors Notebook")  
            exit()
        else:
            os.mkdir(filepath := (cwd + '/.anbtk'))
            os.chdir(filepath)
            initData()
            
            if grampath=="":
                top,grammar,universe,terminals,nonterminals = FSGram.initializer()
                gramLogic.process_fsgram(top,grammar,universe,terminals,nonterminals)
                with open('fsgram.anb','w') as fsgram:
                    fsgram.write(constants.defaultFsgram)
            else:
                if os.path.dirname(grampath)!='':
                    os.chdir(os.path.dirname(os.path.abspath(grampath)))
                temp = open(grampath,'r').read()
                os.chdir(filepath)
                top,grammar,universe,terminals,nonterminals = FSGram.initializer(temp)
                gramLogic.process_fsgram(top,grammar,universe,terminals,nonterminals)
                # this file creation and such might cause some stress
                with open('fsgram.anb','w') as fsgram:
                    fsgram.write(temp)
            templateGen()
        os.chdir(cwd)


def get_root():
    if (anbtk_path:=find_anb())!=None:
        return os.path.dirname(anbtk_path)



def relative_to_anbtk(path):
    if (anbtk_path := find_anb()) != None:
        seed_folder = os.path.dirname(anbtk_path)
        relative_path = Path(path).relative_to(seed_folder)
        relative_path = os.path.join(os.path.basename(seed_folder),relative_path)
        relative_path =   "/".join(relative_path.split("/")[1:])
        return relative_path





# must go and calculate the others entities
def initData():
    """
    Create an initial JSON file or storing statistics related to the types of content in the notebook.
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
    anbtk = find_anb()
    with open(f'{anbtk}/anbtk.json', 'r') as f:
        data = json.load(f)
    
    if file_type not in data:
        data[file_type] = 0
    
    data[file_type] += 1
    with open(f'{anbtk}/universe.dgu','r') as universe:
        const = dgu_helper.parse_text_denomination(universe.read())[file_type]
    print(const)
    id = f"{const}[{data[file_type]}]-{name}"
    
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
    with open('anb2.j2','w') as f:
        f.write(constants.template_productions)







