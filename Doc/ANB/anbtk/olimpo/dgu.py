import os
import json
from . import skeletons
import re
import imghdr
import time


# todo:
#! add the respective ontology additions to dgu files and only accept those 
# add error handling in sync



def initanb(path=""):
    """
    Initializes a new Ancestors Notebook in the current working directory or at the specified path.

    Args:
        path (str): Optional. The path to create the Ancestors Notebook. Defaults to the current working directory.

    Raises:
        Exception: If the current working directory or specified path has already been initialized as an Ancestors Notebook.
    """

    cwd = os.getcwd()
    if os.path.exists(cwd + '/.anbtk'):        
        raise Exception("This folder was already initialized as an Ancestors Notebook.")
    elif find_anb() is not None:
        raise Exception("You are already in an Ancestors Notebook")  
    else:
        os.mkdir(filepath := (cwd + '/.anbtk'))
        os.chdir(filepath)
        initData()
    os.chdir(cwd)


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





def initData():
    """
    Create an initial JSON file for storing statistics related to the types of content in the notebook.
    """

    data = {}
    
    data['Picture'] = 0
    data['Biography'] = 0
    data['Story'] = 0
    
    # > more formats tba
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
        id = f"s{data[file_type]}-{name}"

    elif file_type == 'Picture':
        id = f"p{data[file_type]}-{name}"
    

    with open('anbtk.json', 'w') as f:
        json.dump(data, f)

    return id



def genStory(title,date,author=""):

    """Generates a new text file in the current working directory with a unique filename based on the given title and containing a story skeleton. If an Ancestors Notebook has been initialized, the file will be added to the appropriate folder within the notebook. If not, the file will be created in a directory called 's-[denomination]' in the current working directory. The filename will be of the form 's-[denomination]-YYYYMMDD_HH:MM:SS.dgu', where [denomination] is a simplified version of the title and YYYYMMDD_HH:MM:SS represents the current date and time in UTC.

    Parameters:
    title (str): The title of the story.
    date (str): The date on which the story was written.
    author (str): The name of the story's author (optional).

    Returns:
    None
    """

    cd = os.getcwd()
    title = title
    author = author    
    denomination = simplify(title)

    if find_anb() is None:
        print("No guarantee of a unique name, are you in the correct folder?\n")
        # maybe add a 4 digit hash value 
        filename = f"s-{denomination}-" + time.strftime("%Y%m%d_%H:%M:%S")
        print(f"The file was created with the name {filename}")
    else:
        os.chdir(find_anb())
        filename = dataUpdate('Story',denomination)
    os.chdir(cd)
    
    with open(f'{filename}.dgu','w') as dgufo:
        dgufo.write(skeletons.dguStory(title,author,date,denomination))
   

def simplify(title):
    """Simplifies a given title by capitalizing the first letter of each word and removing any non-alphanumeric characters.

    Parameters:
    title (str): The title to be simplified.

    Returns:
    simplified_title (str): The simplified version of the title.
    """

    words = title.split()
    words = [word.capitalize() for word in words]
    simplified_title = "".join(words)
    simplified_title = re.sub(r'[^\w\s]', '', simplified_title)
    return simplified_title

def genBio(name,birth,death):
    """Generates a new text file in the current working directory
    with a unique filename based on the given name and containing a biography skeleton.
    If an Ancestors Notebook has been initialized, the file will be added to the appropriate folder
    within the notebook.

    Parameters:
    name (str): The name of the person whose biography is being written.
    birth (str): The date of the person's birth.
    death (str): The date of the person's death.

    Returns:
    None
    """
    cd = os.getcwd()
    name = name
    birth = birth
    death = death
    
    if find_anb() is None:
        print("No guarantee of a unique name since you haven't initialized an Ancestors Notebook\n")
        denomination = simplify(name)
        filename = f"b-{denomination}/" + time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        os.chdir(find_anb())
        filename = dataUpdate('Biography', denomination := simplify(name))
        os.chdir(cd)

        with open(f'{filename}.dgu','w') as dgufo:
            dgufo.write(skeletons.dguBio(denomination,name,birth,death))
   


def genDguImage_individual(files,about):
    """
    Generates a .dgu file for each image in a list of image files. Each .dgu file contains information about 
    the image file, such as the path, file format, and an 'about'.

    Args:
        files (list): A list of image file paths.
        about (str): A string that provides a description about the images.

    Raises:
        Exception: If a file in the input list is not an image file.

    Returns:
        None
    """


    root = find_anb()
    if root == None:
        print("Warning: Are you in the correct folder? Path will be absolute.")
    else:
        root = os.path.dirname(root)

    cwd = os.getcwd()
    
    for elem in files:
        if not is_image(elem):
            raise Exception(f"{elem} is not an image file")
        else:
            if root != None:
                path = os.path.relpath(os.path.abspath(elem), root)
                path = os.path.join(os.path.basename(root),path)
            else:
                path = os.path.abspath(elem)
            filename = os.path.basename(elem)
            format = re.split("\.",filename)[1]
            id = get_filename_no_extension(elem) # what to do to have data control?
            if os.path.dirname(elem)!='':               
                os.chdir(os.path.dirname(os.path.abspath(elem)))
            if not os.path.exists(filename[:-4]+'.dgu'):
                with open(filename[:-4]+'.dgu','w') as dgufile:
                    dgufile.write(skeletons.genDguImage(id,format,path,about))
            os.chdir(cwd)

#maybe change to take a path
def genDguImage_tree(about=""):

    """
    Traverses a directory tree and generates a .dgu file for each image file found in the directory and its subdirectories.
    Each .dgu file will contain information about the image file, such as the path, file format, and an 'about'.

    Args:
        about (str): A string that provides a description about the images.

    Returns:
        None
    """

    cwd = os.getcwd() 
    visited = set()
    for dirpath, _, filenames in os.walk(cwd):
        realpath = os.path.realpath(dirpath)
        
        if realpath in visited or os.path.basename(dirpath) == '.anbtk':
            continue
        else:
            visited.add(realpath)
            root = find_anb()
            for filename in filenames:
                if root != None:
                    root = os.path.dirname(root)
                    path = os.path.relpath(os.path.abspath(dirpath), root)
                    path = os.path.join(os.path.basename(root),path)
                else:
                    path = os.path.abspath(filename)
                filepath = os.path.join(dirpath, filename)
                if not is_image(filepath) or os.path.islink(filepath) and not os.path.exists(filepath):
                    continue
                else:
                    format = os.path.splitext(filename)[1][1:]
                    
                    id = os.path.splitext(filename)[0]
                    if not os.path.exists(os.path.join(dirpath, id + '.dgu')):
                        with open(os.path.join(dirpath, id + '.dgu'), 'w') as dgufile:
                            dgufile.write(skeletons.genDguImage(id,path,format,about))


def is_image(path):
    
    """
    Determine if a file is an image based on its content type.

    Args:
        path (str): The file path to check.

    Returns:
        bool: True if the file is an image, False otherwise.
    """
    content_type = imghdr.what(path)
    if content_type is not None:
        return True
    else:
        return False
    

def get_filename_no_extension(path):
    
    """
    Get the filename without extension from a file path.

    Args:
        path (str): The file path to process.

    Returns:
        str: The filename without extension.
    """

    file_name = os.path.basename(path) 
    file_name_without_ext = os.path.splitext(file_name)[0]  
    return file_name_without_ext

