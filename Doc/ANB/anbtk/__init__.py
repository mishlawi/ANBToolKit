""" ANB toolkit module for sorting and managing documents and material from different family branches"""

__version__ = "0.0.1"

import re
import os
import json
import subprocess
import yaml
import datetime
import argparse
import yaml

from . import argsConfig
from . import Constants
from . import dguObject as dgu
from . import DGUhand
from . import FSGram
from . import skeletons
from . import dataControl

#*TODO
## code
# Distribute all aux functions in specific files
# reactoring of functions, some things are repeated a lot and could be easily represented by a function
# templates are trash atm
## ideias
#
#! dsl for notes
#! generate 
#! start to consider images
#* i want it so that story and bio (and others) are default formats but the users can create their ones 





# Gets header and body of dgu and turns it in a dictionary
#NEEDS MAINTANCE

def parseAbstractDgu(filename):
    base, ext = os.path.splitext(filename)
    if ext == '.dgu':
        with open(filename) as f:
            data = f.read()
        headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)", data).group()
        adgu = yaml.full_load(headers)
        text = re.split(r'\-\-\-', data)[2]
        adgu['body'] = text
        return adgu
    else:
        raise ValueError("File format is invalid")


def aboutism(abouts):
    string="\\begin{itemize}"
    if len(abouts)>0:

        for elem in abouts:
            string+= f"\\item {elem}\n"
        string+="\\end{itemize}"
        return string
    else:
        return ""

def texSkeleton(texadgu):
    string = f"""\\section{{{texadgu.get('title',"missing title")}}}
{aboutism(texadgu.get('about',[]))}
\\  
    \\begin{{center}}
        $\\ast$~$\\ast$~$\\ast$
    \\end{{center}}
    {texadgu.get('body',"")}
    """
    return string



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
                temptext = defaultConversion(text)
                adgu['body'] = temptext
                fo.write(texSkeleton(adgu))
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
                    temptext = defaultConversion(text)
                    adgu['body'] = temptext
                    fo.write(texSkeleton(adgu))
                    fo.write("\t")
                    fo.write("\n")
                    fo.write("\pagebreak")
    fo.write("\end{document}")
    
    fo.close()



def defaultConversion(text):
    with open('temp.md', 'w') as temp_md:
        temp_md.write(text)
    subprocess.check_call(['pandoc', '-f', 'markdown', '-t', 'latex', 'temp.md', '-o', 'temp.tex'])
    with open('temp.tex') as temp_tex:
        temptext = temp_tex.read()

    return temptext

################### dgu generation ######################


#maybe add a way to personalize different types of docs 
def docType(file):
    if file.startswith("h"):
        return 'Story'
    elif file.startswith("p"):
        return 'Picture'
    elif file.startswith("b"):
        return 'Biography'


def getFormat(string):
    if string == 'tex':
        return 'latex'
    elif string == 'txt':
        return 'text'
    elif string == 'md':
        return 'markdown'
    else:
        return string

#################### pdf books#############################
# usage: -file+
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
                format = getFormat('tex')
                type = docType(filename)
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
                heading2markdown(temp,tempdgu)
                os.chdir(cwd)
                subprocess.run(['pandoc', 'dgu2pdf.md', '-o', 'dgu2pdf.pdf']) # maybe have a personalized name
                

            else:
                raise Exception(elem + " is not a dgu file")
                
    if arguments.tree:
        
        for (dirpath,_,filenames) in os.walk(cwd):
            for filename in filenames:
              if filename.endswith('.dgu'):
                temp = open(dirpath+'/'+filename,'r').read()
                heading2markdown(temp,tempdgu)
                os.chdir(cwd)
                subprocess.run(['pandoc', 'dgu2pdf.md', '-o', 'dgu2pdf.pdf']) # maybe have a personalized name
    
    tempdgu.close()



from jinja2 import Environment, FileSystemLoader


def dgubook():
    arguments = argsConfig.a_dgubook()
    if arguments is None:
        print("You need to specify a flag. Use dguBook -h for more info.")
        exit(1)

    tempdgu = open('AncestorsNotebook.md', 'w')

    args = ['pandoc', '-f', 'markdown', 'AncestorsNotebook.md', '-o', 'AncestorsNotebook.pdf']

    cwd = os.getcwd()

    if not find_anb():
        print("Initialize the ancestors notebook first.")
        exit(1)

    os.chdir(find_anb()) 
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
            elem_dirname = os.path.dirname(elem_path)
            
            if elem_dirname:
                os.chdir(elem_dirname)
            adgu = parseAbstractDgu(elem)
            print(adgu)
            with open(os.path.basename(elem_path)) as elem_file:
                
                temp = elem_file.read()
                if aux:= re.split('---',temp):
                    (_,cabecalho,corpo) = aux
                    meta = yaml.safe_load(cabecalho)  # moved inside the loop
                    #print(meta)
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
                            #print(meta)
                            meta['corpo'] = corpo
                            if not "title" in meta.keys() or meta['title'] =='':
                                meta['title'] = meta['id']
                            h2.append(meta)
        tempdgu.write(dgus2md.render(tit="Livro dos antepassados",hs=h2)) 
            
        os.chdir(cwd)

    tempdgu.close()
    if not arguments.markdown:
        subprocess.check_call(args)
        os.remove("AncestorsNotebook.md")
        


#################### headings ##########################


def heading2markdown(temp,tempdgu):
    headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",temp).group()
    adgu = yaml.full_load(headers)
    
    if adgu['type'] == 'Story':
        tempdgu.write(f"# {{{adgu['title']}}}\n")
        tempdgu.write(f"### A story written or falling back to _{{{adgu['date']}}}_\n")

    elif adgu['type'] == 'Biography':
        tempdgu.write(f"## _A suscint Biography regarding:_\n")
    else:
        tempdgu.write(f"### {{{adgu['id']}}}\n")
        
    tempdgu.write("---\n")
    for elem in adgu.get('about',''):
        if elem == '':
            pass
        else:
            tempdgu.write(f"* {elem}\n")
    tempdgu.write("---\n")
    text = re.split(r'\-\-\-',temp)[2]
    tempdgu.write(text)
    tempdgu.write('\n<div class="page-break"></div>\n')
    


def heading2Latex(temp,tempdgu):
    headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",temp).group()
    adgu = yaml.full_load(headers)
    for elem in adgu['about']:
        tempdgu.write(f"\\footnote{{{elem}}}")
    if adgu['type'] == 'Story':
        tempdgu.write(f"\\section{{{adgu['title']}}}\n")
        tempdgu.write("Date: \t" + str(adgu['date']))
    else:
        tempdgu.write(f"\\section{{{adgu['id']}}}\n")
        
    tempdgu.write("""\\begin{center}
$\\ast$~$\\ast$~$\\ast$
\\end{center}""")
    text = re.split(r'\-\-\-',temp)[2]
    tempdgu.write("\t")
    tempdgu.write(text)
    tempdgu.write("\n") 
    tempdgu.write("\pagebreak\n\n")


######################## notes #######################

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

    if find_anb is None:
        print("No guarantee of a unique name\n")
        filename = "hx-{denomination}"
    else:
        os.chdir(find_anb())
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
    
    if find_anb() is None:
        print("No guarantee of a unique name since you haven't initialized an Ancestors Notebook\n")
        denomination = simplify(name)
        filename = f"bx-{denomination}"
    else:
        os.chdir(find_anb())
        filename = dataControl.dataUpdate('Biography',simplify(name))
        os.chdir(cd)
    with open(f'{filename}.md','w') as mdfileobject:
        mdfileobject.write(skeletons.biography(name,birth,death,bp,o))
    


############################## .anb ################################


def find_anb():
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

def dguheadercomposer(newDgu,fileObject):
    fileObject.write("---\n")
    yaml.dump(newDgu,fileObject,default_flow_style=False, sort_keys=False,allow_unicode=True)
    fileObject.write("---\n")
    fileObject.close()



def genDgu(title, attributes, nameofthefile, dir):
    id = dataControl.dataUpdate(title, nameofthefile)
    subclass = DGUhand.dgu_subclass(title, attributes)
    newDgu = subclass(nameofthefile, "", title, "", *["" for _ in attributes])
    os.chdir(dir)
    with open(f"{id}.dgu", "w") as f:
        dguheadercomposer(newDgu, f)

        

def initanb(path=""):
    cwd = os.getcwd()
    if os.path.exists(cwd + '/.anbtk'):
        
        raise Exception("This folder was already initialized as an Ancestors Notebook.")
    elif find_anb() is not None:
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



def search_anbtk():
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

def parse_text(input):
    lines = input.strip().split('\n')
    result = {}   
    i = 0
    while i < len(lines):
        if lines[i].startswith('*'):
            name = lines[i][1:].strip().split()[0]            
            items = []
            i += 1
            while i < len(lines) and lines[i].startswith('\t*'):
                item = lines[i][2:].strip()               
                items.append(item)       
                i += 1       
            result[name] = items
        i += 1
    
    return result



def anb():
    
    parser = argparse.ArgumentParser(prog='ancestors notebook')
    subparsers = parser.add_subparsers(dest='subcommand',required=True,help='List of subcommands accepted')
    init_parser = subparsers.add_parser('init')
    init_parser.add_argument('-s','--source',help='Specify a source fsgram file to generate an ancestors notebook', nargs=1)
    dguCommands_parser = subparsers.add_parser('dgu',help='Creates a default dgu or a entity based dgu')
    dguCommands_parser.add_argument('-e','--entity',help='Specify a entity as described in your FSGram file or the default file',nargs=1)
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
        if search_anbtk():

            if args.entity:
            
                with open('universe.dgu') as universe:
                    entities = parse_text(universe.read())
                    if args.entity[0] in entities.keys():
                        genDgu(args.entity[0], entities[args.entity[0]], args.filename[0],currentdir)
                    else:
                        print("No entity exists with that name")
            if not args.entity:
                os.chdir(currentdir)
                empty_dgu = dgu.DGU("","","","")
                with open(args.filename[0]+'.dgu',"w") as f:
                    dguheadercomposer(empty_dgu,f)

        else:
            print("You need to initialize an ancestors notebook")
        

    else:
        args.func(args.name, args.attributes, args)


