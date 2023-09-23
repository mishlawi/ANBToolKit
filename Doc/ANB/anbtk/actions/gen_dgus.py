import os
import re

from ..auxiliar import argsConfig
from ..auxiliar import dgu_helper
from ..auxiliar import skeletons


import inquirer

from ..dgu import DGUhand
from ..dgu import dguObject as dgu

from .. import dataControl
from .. import controlsystem

from ..DSL.entities import gramLogic




def retrieve_all_images():
    """
    Retrieve a list of all image files in the current directory not associated with DGU files.

    This function scans the current directory for image files and filters out those that are not
    associated with DGU files based on their file paths. It returns a list of tuples containing the
    relative path to the image and its absolute path.

    Returns:
        list: A list of tuples containing the relative path and absolute path of image files not
        associated with DGU files.
    """
    files = []

    file_list = [os.path.abspath(file) for file in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), file))]
    pic_list = [(dataControl.relative_to_anbtk(elem),elem) for elem in file_list if dgu_helper.is_image(elem)]
    dgu_paths = [dgu_helper.parseAbstractDgu(elem)['path'] for elem in gramLogic.retrieve_all_dgu_files(dataControl.get_root())]
    for file in pic_list:
        if file[1] not in dgu_paths:
            files.append(file)
    return files

def view_files():
    """
    Display a list of images for selection and return the selected image file paths.

    This function retrieves a list of image files not associated with DGU files using the
    `retrieve_all_images` function. It then displays a list of these images for selection
    using the Inquirer library, allowing the user to choose one or more images. The selected
    images' file paths are returned as a list.

    Returns:
        list: A list of selected image file paths.
    """

    item_list = retrieve_all_images()
    relative_paths = [item[0] for item in item_list]


    questions = [
        inquirer.Checkbox('items',
                          message='elect one or more Pictures to generate its DGU file (use SPACEBAR key to select and ENTER key to confirm the selection)',
                          choices=relative_paths,
                          ),
    ]

    answers = inquirer.prompt(questions)
    selected_items = answers['items']
    selected_formated_paths = []
    for item in selected_items:
        for files in item_list:
            if files[0] == item:
                selected_formated_paths.append(files[1])
    return selected_formated_paths



def genDguImage():
    """
    Generate DGU files for selected images.

    This function handles the process of generating DGU files for selected images.
    It can be configured to generate DGU files for individual images or all images
    in a directory tree, depending on the provided command-line arguments.
    """  
    cwd = os.getcwd()
    arguments = argsConfig.a_image()
    if arguments.file:
        selected = view_files()
        genDguImage_file(selected)
    elif arguments.tree:
        genDguImage_tree(cwd)


def verifyDguImage_singular(img):
    """
    Verify if a DGU file already exists for a given image.

    This function checks if there is already a DGU file associated with the provided image.
    It compares the normalized and lowercase paths of the image and the DGU files' paths.

    Args:
        img (str): The absolute path of the image to check.

    Returns:
        bool: True if a DGU file exists for the image; otherwise, False.
    """
    dgu_files = gramLogic.retrieve_all_dgu_files(dataControl.get_root())
    for file in dgu_files:        
        adgu = dgu_helper.parseAbstractDgu(file)
        
        # Normalize and convert paths to lowercase for consistent comparison
        normalized_adgu_path = os.path.normpath(adgu['path']).lower()
        normalized_img_path = os.path.normpath(os.path.abspath(img)).lower()
        
        if normalized_adgu_path == normalized_img_path:
            print(f"There is a dgu file for this image already in:\n* {file}\n")
            return True
        


def verifyDguImage(img):
    """
    Verify if a DGU file already exists for a given image.

    This function checks if there is already a DGU file associated with the provided image.
    It compares the paths of the image and the DGU files' paths.

    Args:
        img (str): The absolute path of the image to check.

    Returns:
        bool: True if a DGU file exists for the image; otherwise, False.
    """
    dgu_files = gramLogic.retrieve_all_dgu_files(dataControl.get_root())
    for file in dgu_files:
        adgu = dgu_helper.parseAbstractDgu(file)
        if adgu['path'] == os.path.abspath(img) :
            return True

def genDguImage_file(files):
    """
    Generate DGU files for a list of image files.

    This function generates DGU files for a list of image files. Each image is associated with
    a DGU file containing metadata such as format, ID, and file path. The function checks if a
    DGU file already exists for each image before generating a new one.

    Args:
        files (list): A list of absolute paths to image files for which DGU files will be generated.
    """

    cwd = os.getcwd()

    for elem in files:
        if not dgu_helper.is_image(elem):
            print(f"{elem} is not an image file")
            exit()
        
        else:
            filename = os.path.basename(elem)
            format = re.split("\.",filename)[1]
            id = dgu_helper.get_filename_no_extension(elem) 
            abpath = os.path.abspath(elem)
            # realpath = dataControl.relative_to_anbtk(abpath)
            if os.path.dirname(elem)!='':    
                os.chdir(os.path.dirname(abpath))
            usedname = filename[:-4].replace(" ", "")
            usedname = dataControl.dataUpdate('Picture',usedname)
            if not verifyDguImage_singular(elem):
                entities = gramLogic.get_entities_fsgram()
                att_entities = gramLogic.get_entites_attributes(entities)
                subclass = DGUhand.dgu_subclass('Picture', att_entities['Picture'])
                newDgu = subclass(id, format, 'Picture', "", abpath, *["" for _ in att_entities['Picture']])
                with open(os.path.join(usedname + '.dgu'), 'w') as dgufile:
                    dgu_helper.dguheadercomposer(newDgu, dgufile)
                controlsystem.auto_sync()
                os.chdir(cwd)
            else:
                exit()

                    
def genDguImage_tree(cwd):
    """
    Generate DGU files for images in a directory tree.

    This function traverses a directory tree starting from the specified 'cwd' (current working directory).
    It identifies image files in the tree, generates DGU files for each image, and associates metadata
    such as format, ID, and file path with each DGU file. The function checks if a DGU file already exists
    for each image before generating a new one.

    Args:
        cwd (str): The path to the root directory of the directory tree to search for image files.

    Note:
        This function relies on external modules and functions such as `os`, `dgu_helper`,
        `gramLogic`, `dataControl`, and `DGUhand` for image processing and DGU file generation.
    """
    count = 0
    visited = set()
    for dirpath, _, filenames in os.walk(cwd):
        realpath = os.path.realpath(dirpath)
        if realpath in visited or os.path.basename(dirpath) == '.anbtk':
            continue
        else:
            visited.add(realpath)
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if not dgu_helper.is_image(filepath) or os.path.islink(filepath) and not os.path.exists(filepath):
                    continue
                else:
                    format = os.path.splitext(filename)[1][1:]
                    id = os.path.splitext(filename)[0]
                    abpath = os.path.abspath(filepath)
                    # realpath = dataControl.relative_to_anbtk(abpath)

                    if not verifyDguImage(filepath):
                    # if not os.path.exists(os.path.join(dirpath, id + '.dgu')):
                        usedname = dataControl.dataUpdate('Picture',id)
                        entities = gramLogic.get_entities_fsgram()
                        att_entities = gramLogic.get_entites_attributes(entities)
                        subclass = DGUhand.dgu_subclass('Picture', att_entities['Picture'])
                        newDgu = subclass(id, format, 'Picture', "", abpath, *["" for _ in att_entities['Picture']])
                        with open(os.path.join(dirpath, usedname + '.dgu'), 'w') as dgufile:
                            dgu_helper.dguheadercomposer(newDgu, dgufile)
                        count+=1
                        controlsystem.auto_sync()    
                    else:
                           exit()
                print("A total of " + str(count) + " 'Picture' dgu files were created\n")        
                


def simplify(title):
    """
    Simplify a title by capitalizing words and removing special characters.

    This function takes a title as input, capitalizes each word, and removes special characters
    to create a simplified version of the title.

    Args:
        title (str): The title to be simplified.

    Returns:
        str: The simplified title.
    """
    words = title.split()
    words = [word.capitalize() for word in words]
    simplified_title = "".join(words)
    simplified_title = re.sub(r'[^\w\s]', '', simplified_title)
    return simplified_title 



def genStory(): 
    """
    Generate a story DGU file with metadata.

    This function generates a story DGU file based on the provided arguments. It accepts
    title, author, date, and DGU options. If author is not provided, it assumes the author is
    the current folder denomination. It also creates a unique filename based on the simplified
    title.

    Args:
        None (Arguments are parsed internally using `argsConfig.a_genStory()`).

    Returns:
        None
    """
    args = argsConfig.a_genStory()
    title = args.title
    date = args.date

    if args.author is None:
        print("It is assumed that the author is the current folder denomination") # this should be changed
        author = os.path.split(os.getcwd())[-1]
    else:
        author = args.author[0]
    
    denomination = simplify(title)

    if dataControl.find_anb is None:
        print("No guarantee of a unique name\n")
        filename = f"hx-{denomination}"
    else:
        
        filename = dataControl.dataUpdate('Story',denomination)
    
    if args.dgu:
        path  = os.path.join(os.getcwd(),f'{filename}.dgu')
        with open(f'{filename}.dgu','w') as dgufo:
            dgufo.write(skeletons.dguStory(title,author,date,denomination,path))
    else:
        with open(f'{filename}.tex','w') as texfo:
            texfo.write(skeletons.story(title,author,date))

    controlsystem.auto_sync()



def genBio():
    """
    Generate a biography DGU file with metadata.

    This function generates a biography DGU file based on the provided arguments, including the name,
    birth date, death date, birthplace, and occupation. It creates a unique filename based on the
    simplified name. If an Ancestors Notebook is not initialized, it warns about the absence of
    guaranteed unique names.

    Args:
        None (Arguments are parsed internally using `argsConfig.a_genBio()`).

    Returns:
        None
    """
    args = argsConfig.a_genBio()
    name = args.name
    birth = args.birth
    death = args.death
    bp = args.birthplace
    o = args.occupation
    
    if dataControl.find_anb() is None:
        print("No guarantee of a unique name since you haven't initialized an Ancestors Notebook\n")
        denomination = simplify(name)
        filename = f"bx-{denomination}"
    else:
        filename = dataControl.dataUpdate('Biography',simplify(name))
    path  = os.path.join(os.getcwd(),f'{filename}.dgu')
    with open(f'{filename}.dgu','w') as mdfileobject:
        mdfileobject.write(skeletons.dguBio(name,path,birth,death,bp,o) )
    controlsystem.auto_sync()



# path is missing
def genDgu(title, attributes, nameofthefile, dir):
    """
    Generate a DGU file with metadata.

    This function generates a DGU file based on the provided title, attributes, file name, and directory.
    It creates a unique ID for the DGU file, creates a subclass of the specified title with the given
    attributes, and writes the DGU file with metadata.

    Args:
        title (str): The title or type of the DGU file.
        attributes (list): A list of attributes associated with the DGU file.
        nameofthefile (str): The name of the DGU file without the file extension.
        dir (str): The directory where the DGU file will be saved.

    Returns:
        None
    """
    id = dataControl.dataUpdate(title, nameofthefile)
    subclass = DGUhand.dgu_subclass(title, attributes)
    newDgu = subclass(nameofthefile, "", title, "", f"{dir}/{id}.dgu", *["" for _ in attributes])
#    os.chdir(dir)
    with open(f"{dir}/{id}.dgu", "w") as f:
        dgu_helper.dguheadercomposer(newDgu, f)
    controlsystem.auto_sync()
       
    