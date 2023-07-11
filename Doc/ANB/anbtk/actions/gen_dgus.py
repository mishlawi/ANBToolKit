import os
import yaml
import re

from ..auxiliar import argsConfig
from ..auxiliar import dgu_helper
from ..auxiliar import skeletons

from ..dgu import DGUhand
from ..dgu import dguObject as dgu

from .. import dataControl
from .. import controlsystem



def genDguImage():    
    cwd = os.getcwd()
    arguments = argsConfig.a_image()
    if arguments.file:
        genDguImage_file(arguments.file)
    elif arguments.tree:
        genDguImage_tree(cwd)


def genDguImage_file(files):

    cwd = os.getcwd()

    for elem in files:
        if not dgu_helper.is_image(elem):
            raise Exception(f"{elem} is not an image file")
        else:
            filename = os.path.basename(elem)
            format = re.split("\.",filename)[1]
            id = dgu_helper.get_filename_no_extension(elem) 
            abpath = os.path.abspath(elem)
            realpath = dataControl.relative_to_anbtk(abpath)
            if os.path.dirname(elem)!='':    
                os.chdir(os.path.dirname(abpath))
            usedname = filename[:-4].replace(" ", "")
            if not os.path.exists(usedname+'.dgu'):
                with open(usedname+'.dgu','w') as dgufile:
                    dgufile.write('---\n')
                    yaml.dump(dgu.DGU(id = id,format = format,path=abpath),dgufile,default_flow_style=False, sort_keys=False,allow_unicode=True)
                    dgufile.write('---\n')
                os.chdir(cwd)

                    
def genDguImage_tree(cwd):
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
                    if not os.path.exists(os.path.join(dirpath, id + '.dgu')):
                        with open(os.path.join(dirpath, id + '.dgu'), 'w') as dgufile:
                            dgufile.write('---\n')
                            yaml.dump(dgu.DGU(id=id, format=format, path=abpath), dgufile, default_flow_style=False, sort_keys=False, allow_unicode=True)
                            dgufile.write('---\n')
                    else:
                        print("There is a dgu file for this image already!\n")
    controlsystem.auto_sync()
                    


def simplify(title):
    words = title.split()
    words = [word.capitalize() for word in words]
    simplified_title = "".join(words)
    simplified_title = re.sub(r'[^\w\s]', '', simplified_title)
    return simplified_title 



def genStory():
    cd = os.getcwd()
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
        os.chdir(dataControl.find_anb())
        filename = dataControl.dataUpdate('Story',denomination)
    os.chdir(cd)
    
    if args.dgu:
        with open(f'{filename}.dgu','w') as dgufo:
            dgufo.write(skeletons.dguStory(title,author,date,denomination))
    else:
        with open(f'{filename}.tex','w') as texfo:
            texfo.write(skeletons.story(title,author,date))

    controlsystem.auto_sync()



def genBio():    
    cd = os.getcwd()
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
        os.chdir(dataControl.find_anb())
        filename = dataControl.dataUpdate('Biography',simplify(name))
        os.chdir(cd)
    with open(f'{filename}.md','w') as mdfileobject:
        mdfileobject.write(skeletons.biography(name,birth,death,bp,o))
    controlsystem.auto_sync()



# path is missing
def genDgu(title, attributes, nameofthefile, dir):
    id = dataControl.dataUpdate(title, nameofthefile)
    subclass = DGUhand.dgu_subclass(title, attributes)
    newDgu = subclass(nameofthefile, "", title, "", "", *["" for _ in attributes])
#    os.chdir(dir)
    with open(f"{dir}/{id}.dgu", "w") as f:
        dgu_helper.dguheadercomposer(newDgu, f)
    controlsystem.auto_sync()
       
    