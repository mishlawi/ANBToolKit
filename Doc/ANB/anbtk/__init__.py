""" ANB toolkit module for sorting and managing documents and material from different family branches"""

__version__ = "0.0.1"

import re
import os
import subprocess
import yaml
import datetime
import argparse
import yaml

from jinja2 import Environment, FileSystemLoader

from . import argsConfig
from . import Constants
from . import dguObject as dgu
from . import DGUhand
from . import FSGram
from . import skeletons
from . import dataControl
from . import auxiliar

#*TODO
## code
# reactoring of functions, some things are repeated a lot and could be easily represented by a function
# templates are trash atm
## ideias
#
#!FIX TEX2DGU regarding the UTF8
#! start to consider images
#* i want it so that story and bio (and others) are default formats but the users can create their ones 


#################### latex book ########################

def dgu2texbook():
    
    arguments = argsConfig.a_dgu2texbook()
    
    fo = open("texbook.tex",'w')
    fo.write(f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{imakeidx}}
\\makeindex
\\begin{{document}}\n""")
    
    if arguments.file:
        for file in arguments.file:
            if file.endswith('.dgu'):
                if os.path.dirname(file)!='':
                        os.chdir(os.path.dirname(os.path.abspath(file)))
                temp = open(file,'r').read()
                headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",temp).group()
                adgu = yaml.full_load(headers)
                text = re.split(r'\-\-\-',temp)[2] 
                temptext = auxiliar.defaultConversion(text)
                adgu['body'] = temptext
                fo.write(auxiliar.texSkeleton(adgu))
                fo.write("\t")
                fo.write("\n")
                fo.write("\pagebreak")
            

            else:
                raise Exception(file + ' is not a dgu file.')
            
    elif arguments.tree:
        cwd = os.getcwd()
        for (dirpath,_,filenames) in os.walk(cwd):
            for filename in filenames:
                if filename.endswith('.dgu'):
                    temp = open(dirpath+'/'+filename,'r').read()
                    headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",temp).group()
                    adgu = yaml.full_load(headers)
                    text = re.split(r'\-\-\-',temp)[2]
                    temptext = auxiliar.defaultConversion(text)
                    adgu['body'] = temptext
                    fo.write(auxiliar.texSkeleton(adgu))
                    fo.write("\t")
                    fo.write("\n")
                    fo.write("\pagebreak")
    fo.write("\end{document}")
    
    fo.close()




#################### pdf books#############################
# usage: -file+

#* dont forget to add the path if needed in the future
def tex2dgu(dirout=""):
    arguments = argsConfig.a_tex2dgu()
    if arguments.file:
        for elem in arguments.file:
            filename = os.path.basename(elem)
            if filename.endswith(".tex"):
                if os.path.dirname(elem)!='':
                    os.chdir(os.path.dirname(os.path.abspath(elem)))
                file = open(filename).read()
                args = ['pandoc','-s', filename, '-o', filename[:-4] + '.md']
                subprocess.check_call(args)
                fo = open(filename[:-4] + '.md').read()
                headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",fo).group()
                adgu = yaml.full_load(headers)
                dgufile = open(filename[:-4]+'.dgu','w')
                id = re.search(r'(?<=\-).+(?=\.)',filename).group()
                text = re.split(r'\-\-\-',fo)[2]
                print(text)
                dgufile.write("---\n")
                format = auxiliar.getFormat('tex')
                type = auxiliar.docType(filename)
                abouts = re.findall(r'\\ind\{(.+?| )\}',file)
                yaml.dump(dgu.DGU(id = id,format = format,type=type,about=abouts),dgufile,default_flow_style=False, sort_keys=False,allow_unicode=True)
                yaml.dump(adgu,dgufile)
                dgufile.write("---\n")
                dgufile.write(text)
                subprocess.check_call(['rm',filename[:-4]+'.md'])
                if dirout!="":
                    subprocess.check_call(['mv',filename+'.dgu',dirout])
            else:
                raise Exception("Not a latex file")




#! THIS ONE IS NOT FINISHED, I NEED A DIFFERENT APPROACH
# usage: -file+ | -tree{1} 
def dgubookmd():
    arguments = argsConfig.a_dgubookmd()
    time = datetime.datetime.now()
    x = str(time)

    tempdgu =  open('dgu2pdf.md','w') 
    tempdgu.write(Constants.markdownbook)
    tempdgu.write(f"<sup>Processed and generated on {x[:10]}</sup>.\n\n\n")

    cwd = os.getcwd()

    if arguments.file:            
        for elem in arguments.file:
            if elem.endswith('.dgu'):
                if os.path.dirname(elem)!='':
                    os.chdir(os.path.dirname(os.path.abspath(elem)))
                temp = open(os.path.basename(elem),'r').read()
                auxiliar.heading2markdown(temp,tempdgu)
                os.chdir(cwd)
                subprocess.run(['pandoc', 'dgu2pdf.md', '-o', 'dgu2pdf.pdf']) # maybe have a personalized name
                

            else:
                raise Exception(elem + " is not a dgu file")
                
    if arguments.tree:
        
        for (dirpath,_,filenames) in os.walk(cwd):
            for filename in filenames:
              if filename.endswith('.dgu'):
                temp = open(dirpath+'/'+filename,'r').read()
                auxiliar.heading2markdown(temp,tempdgu)
                os.chdir(cwd)
                subprocess.run(['pandoc', 'dgu2pdf.md', '-o', 'dgu2pdf.pdf']) # maybe have a personalized name
    
    tempdgu.close()



def dgubook():
    arguments = argsConfig.a_dgubook()
    if arguments is None:
        print("You need to specify a flag. Use dguBook -h for more info.")
        exit(1)

    tempdgu = open('AncestorsNotebook.md', 'w')

    args = ['pandoc', '-s', 'AncestorsNotebook.md', '-o', 'AncestorsNotebook.pdf']
    #args = ['pdflatex', 'AncestorsNotebook.tex']

    cwd = os.getcwd()

    if not dataControl.find_anb():
        print("Initialize the ancestors notebook first.")
        exit(1)

    os.chdir(dataControl.find_anb()) 
    environment = Environment(loader=FileSystemLoader("templates/"))
    dgus2md = environment.get_template("anb1.j2")
    os.chdir(cwd)
    if arguments.file:
        h2=[]
        for elem in arguments.file:
            if not elem.endswith('.dgu'):
                tempdgu.close()
                raise Exception(f"{elem} is not a dgu file")
            
            elem_path = os.path.abspath(elem)
            with open(elem_path) as elem_file:
                
                temp = elem_file.read()
                if aux:= re.split('---',temp):
                    (_,cabecalho,corpo) = aux
                    meta = yaml.safe_load(cabecalho)  # moved inside the loop
                    meta['corpo'] = corpo
                    if not "title" in meta.keys() or meta['title'] == '':
                        meta['title'] = meta['id']
                    h2.append(meta)

        tempdgu.write(dgus2md.render(tit="Livro dos antepassados",hs=h2))            
        os.chdir(cwd)
    if arguments.tree:
        h2=[]
        visited = set()
        for dirpath, _, filenames in os.walk(cwd, followlinks=True):
            realpath = os.path.realpath(dirpath)
            if realpath in visited or os.path.basename(dirpath) == '.anbtk':
                continue

            visited.add(realpath)
            for filename in filenames:
                if filename.endswith('.dgu'):
                    elem_path = os.path.join(dirpath, filename)
                    with open(elem_path) as elem_file:
                        temp = elem_file.read()
                        if aux:= re.split('---',temp):
                            (_,cabecalho,corpo) = aux
                            meta = yaml.safe_load(cabecalho)  # moved inside the loop
                            meta['corpo'] = corpo
                            if not "title" in meta.keys() or meta['title'] =='':
                                meta['title'] = meta['id']
                            h2.append(meta)
        tempdgu.write(dgus2md.render(tit="Livro dos antepassados",hs=h2)) 
            
        os.chdir(cwd)

    tempdgu.close()
    if not arguments.markdown:
        subprocess.check_call(args)
        os.remove("AncestorsNotebook.md") #! this is tex, change if it turns out to be necessary to use tex instead of md
        


######################## notes #######################
def genDguImage():
    cwd = os.getcwd()
    arguments = argsConfig.a_image()
    if arguments.file:
        for elem in arguments.file:
            if not auxiliar.is_image(elem):
                raise Exception(f"{elem} is not an image file")
            else:
                filename = os.path.basename(elem)
                format = re.split("\.",filename)[1]
                id = auxiliar.get_filename_no_extension(elem) # what to do to have data control?
                abpath = os.path.abspath(elem)
                if os.path.dirname(elem)!='':
                    
                    os.chdir(os.path.dirname(os.path.abspath(elem)))
                
                with open(filename[:-4]+'.dgu','w') as dgufile:
                    dgufile.write('---\n')
                    yaml.dump(dgu.DGU(id = id,format = format,path=abpath),dgufile,default_flow_style=False, sort_keys=False,allow_unicode=True)
                    dgufile.write('---\n')
                os.chdir(cwd)
                               
    if arguments.tree:
        visited = set()
        for dirpath, _, filenames in os.walk(cwd, followlinks=True):
            realpath = os.path.realpath(dirpath)
            if realpath in visited or os.path.basename(dirpath) == '.anbtk':
                continue
            else:
                visited.add(realpath)
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if not auxiliar.is_image(filepath) or os.path.islink(filepath) and not os.path.exists(filepath):
                        continue
                    else:
                        format = os.path.splitext(filename)[1][1:]
                        id = os.path.splitext(filename)[0]
                        abpath = os.path.abspath(filepath)
                        with open(os.path.join(dirpath, id + '.dgu'), 'w') as dgufile:
                            dgufile.write('---\n')
                            yaml.dump(dgu.DGU(id=id, format=format, path=abpath), dgufile, default_flow_style=False, sort_keys=False, allow_unicode=True)
                            dgufile.write('---\n')

                            
    
      
 
#? needs to be checked
# usage : --f+
def genNote():
    arguments = argsConfig.a_notes()
    if arguments.file:            
        for elem in arguments.file:
                if os.path.dirname(elem)!='':
                    filename = os.path.basename(elem)
                    name = re.split("\.",filename)[0]
                    format = re.split("\.",filename)[1]
                    identifier = re.split("-",name)[0]
                    os.chdir(os.path.dirname(os.path.abspath(elem)))
                    if (identifier +'.anbnote') in os.listdir(os.getcwd()):
                        print("Note already exists.")
                    else:
                        if format == 'tex':
                            args = ['pandoc','-s', elem, '-o', name + '.md']
                            subprocess.check_call(args)
                            fo = open(f'{name}.md').read()
                            headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",fo).group()
                            adgu = yaml.full_load(headers)
                            subprocess.check_call(['rm',f"{name}.md"])
                            notename = "note" + '-' + re.split("-",name)[1] 
                            body = skeletons.note(notename,adgu.get('title',' '),adgu.get('author',' '),adgu.get('date',' '))
                            foNote = open(f"{identifier}.anbnote",'w')
                            foNote.write(body)
                            foNote.close()
                        # more formats to be added

# aux of genStory
def simplify(title):
    words = title.split()
    words = [word.capitalize() for word in words]
    simplified_title = "".join(words)
    simplified_title = re.sub(r'[^\w\s]', '', simplified_title)
    return simplified_title

# usage : -title -author? -date -dgu
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

    if auxiliar.find_anb is None:
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


def genBio():
    cd = os.getcwd()
    args = argsConfig.a_genBio()
    name = args.name
    birth= args.birth
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
    




############################## .anb ################################





def genDgu(title, attributes, nameofthefile, dir):
    id = dataControl.dataUpdate(title, nameofthefile)
    subclass = DGUhand.dgu_subclass(title, attributes)
    newDgu = subclass(nameofthefile, "", title, "", "", *["" for _ in attributes])
    os.chdir(dir)
    with open(f"{id}.dgu", "w") as f:
        auxiliar.dguheadercomposer(newDgu, f)
     

def initanb(path=""):
    cwd = os.getcwd()
    if os.path.exists(cwd + '/.anbtk'):
        
        raise Exception("This folder was already initialized as an Ancestors Notebook.")
    elif dataControl.find_anb() is not None:
        raise Exception("You are already in an Ancestors Notebook")  
    else:
        os.mkdir(filepath := (cwd + '/.anbtk'))
        os.chdir(filepath)
        dataControl.initData()
        

        if path=="":
            FSGram.initializer()
        else:
            if os.path.dirname(path)!='':
                os.chdir(os.path.dirname(os.path.abspath(path)))
            
            temp = open(path,'r').read()
            os.chdir(filepath)
            FSGram.initializer(temp)
        dataControl.templateGen()



def anb():
    
    parser = argparse.ArgumentParser(prog='ancestors notebook')
    subparsers = parser.add_subparsers(dest='subcommand',required=True,help='List of subcommands accepted')
    init_parser = subparsers.add_parser('init')
    init_parser.add_argument('-s','--source',help='Specify a source fsgram file to generate an ancestors notebook', nargs=1)
    dguCommands_parser = subparsers.add_parser('dgu',help='Creates a default dgu or a entity based dgu')
    dguCommands_parser.add_argument('-e','--entity',help='Specify an entity as described in your FSGram file or the default file',nargs=1)
    dguCommands_parser.add_argument('-f','--filename',help='Name of the dgu',type=str,dest='filename',required=True,nargs=1)

    args = parser.parse_args()
    currentdir = os.getcwd()

    if args.subcommand == 'init':
    
        if args.source:
            file = args.source[0]
            initanb(os.path.abspath(file))
    
        else:
            initanb()
    
    elif args.subcommand == 'dgu':
        if dataControl.search_anbtk():

            if args.entity:
            
                with open('universe.dgu') as universe:
                    entities = auxiliar.parse_text(universe.read())
                    if args.entity[0] in entities.keys():
                        genDgu(args.entity[0], entities[args.entity[0]], args.filename[0],currentdir)
                    else:
                        print("No entity exists with that name")
            if not args.entity:
                os.chdir(currentdir)
                empty_dgu = dgu.DGU()
                with open(args.filename[0]+'.dgu',"w") as f:
                    auxiliar.dguheadercomposer(empty_dgu,f)

        else:
            print("You need to initialize an ancestors notebook")
        

    else:
        args.func(args.name, args.attributes, args)


