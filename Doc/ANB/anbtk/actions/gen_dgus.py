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
    files = []

    file_list = [os.path.abspath(file) for file in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), file))]
    pic_list = [(dataControl.relative_to_anbtk(elem),elem) for elem in file_list if dgu_helper.is_image(elem)]
    dgu_paths = [dgu_helper.parseAbstractDgu(elem)['path'] for elem in gramLogic.retrieve_all_dgu_files(dataControl.get_root())]
    for file in pic_list:
        if file[1] not in dgu_paths:
            files.append(file)
    return files

def view_files():

    item_list = retrieve_all_images()
    relative_paths = [item[0] for item in item_list]


    questions = [
        inquirer.Checkbox('items',
                          message='Select one or more Pictures to generate its DGU file (use spacebar to select, enter to confirm the selection)',
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
    cwd = os.getcwd()
    arguments = argsConfig.a_image()
    if arguments.file:
        selected = view_files()
        genDguImage_file(selected)
    elif arguments.tree:
        genDguImage_tree(cwd)


def verifyDguImage_singular(img):
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
    dgu_files = gramLogic.retrieve_all_dgu_files(dataControl.get_root())
    for file in dgu_files:
        adgu = dgu_helper.parseAbstractDgu(file)
        if adgu['path'] == os.path.abspath(img) :
            return True

def genDguImage_file(files):

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
                        print("A total of " + str(count) + " 'Picture' dgu files were created\n")
                    
                    else:
                       exit()


def simplify(title):
    words = title.split()
    words = [word.capitalize() for word in words]
    simplified_title = "".join(words)
    simplified_title = re.sub(r'[^\w\s]', '', simplified_title)
    return simplified_title 



def genStory():
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
        filename = "hx-{denomination}"
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
        mdfileobject.write(skeletons.dguBio(name,birth,death,bp,o,path) )
    controlsystem.auto_sync()



# path is missing
def genDgu(title, attributes, nameofthefile, dir):
    id = dataControl.dataUpdate(title, nameofthefile)
    subclass = DGUhand.dgu_subclass(title, attributes)
    newDgu = subclass(nameofthefile, "", title, "", f"{dir}/{id}.dgu", *["" for _ in attributes])
#    os.chdir(dir)
    with open(f"{dir}/{id}.dgu", "w") as f:
        dgu_helper.dguheadercomposer(newDgu, f)
    controlsystem.auto_sync()
       
    