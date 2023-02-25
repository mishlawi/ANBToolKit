""" ANB toolkit module for sorting and managing documents and material from different family branches"""

__version__ = "0.0.1"

import re
import os
import json
import sys
import subprocess
import yaml
import datetime
import argparse
import yaml
import time

from . import argsConfig
from . import Constants
from . import dguObject as dgu
from . import DGUhand
from . import FSGram
from . import skeletons

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
    if re.split(r'\.',filename)[1] == 'dgu':
        fo = open(filename).read()
        headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",fo).group()
        adgu = yaml.full_load(headers)
        text = re.split(r'\-\-\-',fo)[2]
        adgu['body'] = text
        return adgu            
    
    else:
        ValueError("File Format is invalid")


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

def dgu2texbuilder(file):
    adgu = parseAbstractDgu(file)
    if adgu['format'] == 'latex':
        return texSkeleton(adgu)
    else:
        return ""

def dgu2tex():
    for file in sys.argv[1:]:
        print(dgu2texbuilder(file))

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
    temporary = open('temp.md','w')
    temporary.write(text)
    temporary.close()
    subprocess.check_call(['pandoc','-f', 'markdown', '-t', 'latex','temp.md', '-o','temp.tex'])
    temptext = open('temp.tex').read()
    subprocess.check_call(['rm','temp.md'])
    subprocess.check_call(['rm','temp.tex'])
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


# usage: -file+ | -tree{1} 
def dgubook():
 
    arguments = argsConfig.a_dgubook()
    if arguments is not None:
        time = datetime.datetime.now()
        x = str(time)
        tempdgu = open('dgu2pdf.md','w')
        tempdgu.write("# Ancestors Notebook\n")
        tempdgu.write("### _A Book of special stories_\n\n\n")
        tempdgu.write(f"Processed and generated on {x[:10]}.\n\n\n")
        tempdgu.write('\pagebreak\n\n')
        args = ['pandoc', '-f','markdown','dgu2pdf.md','-o','dgu2pdf.pdf']
        cwd = os.getcwd()
        if arguments.file:            
            for elem in arguments.file:
                if elem.endswith('.dgu'):
                    if os.path.dirname(elem)!='':
                        os.chdir(os.path.dirname(os.path.abspath(elem)))
                    temp = open(os.path.basename(elem),'r').read()
                    heading2Latex(temp,tempdgu)
                    os.chdir(cwd)

                else:
                    tempdgu.close()        
                    raise Exception(elem + " is not a dgu file")
            tempdgu.close()
            subprocess.check_call(args)
                    
        if arguments.tree:
            
            visited = set()
            for dirpath, _, filenames in os.walk(cwd, followlinks=True):
                realpath = os.path.realpath(dirpath)
                if realpath in visited:
                    continue
                visited.add(realpath)
                
                if os.path.basename(dirpath) == '.anbtk':
                    continue
                for filename in filenames:
                    if filename.endswith('.dgu'):
                        temp = open(os.path.join(dirpath, filename),'r').read()
                        heading2Latex(temp,tempdgu)
                        os.chdir(cwd)
            tempdgu.close()
            subprocess.check_call(args)
            
    else:
        print("You need to specify a flag. Use dguBook -h")

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
    args = argsConfig.a_genStory
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
        filename = dataUpdate('Story',denomination)
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
        filename = dataUpdate('Biography',simplify(name))
        os.chdir(cd)
    with open(f'{filename}.md','w') as mdfileobject:
        mdfileobject.write(skeletons.biography(name,birth,death,bp,o))
    
    # if args.dgu:
    #     with open(f'{filename}.dgu','w') as dgufo:
    #         print()
    #        # dgufo.write(dguBio(title,author,date,denomination))
    # else:



############################## .anb ################################

def initData():
    data = {}
    
    data['Biography'] = 0
    data['Story'] = 0

    # > more formats tba
    with open('anbtk.json','w') as anbtkfo:
        json.dump(data,anbtkfo)

def dataUpdate(file_type, name):
    
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

def template_generator():
    os.mkdir('templates')
    os.chdir('templates')




def handleCommand(title, attributes, nameofthefile):
    id = dataUpdate(title,nameofthefile)
    subclass = DGUhand.dgu_subclass(title, attributes)
    newDgu = subclass(None, None, None, None, *[None for _ in attributes])
    yaml.dump(newDgu, f"{id}.dgu")




    



        

def initanb(path=""):
    cwd = os.getcwd()
    if os.path.exists(cwd + '/.anbtk'):
        
        raise Exception("This folder was already initialized as an Ancestors Notebook.")
    elif find_anb() is not None:
        raise Exception("You are already in an Ancestors Notebook")  
    else:
        os.mkdir(filepath := (cwd + '/.anbtk'))
        os.chdir(filepath)
        initData()
        if path=="":
            FSGram.initializer()
        else:
            if os.path.dirname(path)!='':
                os.chdir(os.path.dirname(os.path.abspath(path)))
            
            temp = open(path,'r').read()
            os.chdir(filepath)
            FSGram.initializer(temp)       



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
    dguCommands_parser = subparsers.add_parser('dgu',help='Creates a default dgu or a')
    dguCommands_parser.add_argument('-e','--entity',help='Specify a entity as described in your FSGram file or the default file',nargs=1)
    dguCommands_parser.add_argument('-f','--filename',help='Name of the dgu',type=str,dest='filename',required=True,nargs=1)
    dguCommands_parser.set_defaults(func=lambda args: dgu_default_action())

    def dgu_default_action():
        print("Please specify an entity using the '-e' flag or use '-h' for help.")
    args = parser.parse_args()


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
                        handleCommand(args.entity[0], entities[args.entity], args.filename)
                    else:
                        print("No entity exists with that name")
            if not args.entity:
                empty_dgu = dgu.DGU("", "", "", "")
                with open(args.filename+'.dgu',"w") as f:
                    yaml.dump(empty_dgu,f)



        else:
            print("You need to initialize an ancestors notebook")
        
            
        


    else:
        args.func(args.name, args.attributes, args)


