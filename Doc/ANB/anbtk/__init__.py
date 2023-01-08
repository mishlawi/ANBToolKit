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
import markdown2
import weasyprint
import time

from . import Constants
from . import FSGram
from . import dguObject as dgu
from . import skeletons

#*TODO
## code
# Distribute all aux functions in specific files
# try to remove verbose to another file brought by the argparse module
# reactoring of functions, some things are repeated a lot and could be easily represented by a function
# templates are trash atm
## ideias
#
#! dsl for notes
#! generate 
#! start to consider images




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
    parser = argparse.ArgumentParser(
        prog = 'dgu2texbook',
        description = 'Aglomerates a number of .dgu files in a latex book.',
        epilog = 'In a latex file with diferent latex files aglutinated in one')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    #parser.add_argument('-o','--out',help="output destination",nargs=1)
    group.add_argument('-t','--tree',help="Iterates through the entire tree of document of the present directory.",action='store_true',default=False)
    arguments = parser.parse_args()
    
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

def tex2dgu(dirout=""):
    parser = argparse.ArgumentParser(
        prog = 'dgubook',
        description = 'Aglomerates a number of .dgu files in a book - pdf format.',
        epilog = 'Results in a pdf file containing generic universal documents aglutinated.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    arguments = parser.parse_args()
    
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
                dgufile.write("---\n")
                format = getFormat('tex')
                type = docType(filename)
                abouts = re.findall(r'\\ind\{(.+?| )\}',file)
                yaml.dump(dgu(id = id,format = format,type=type,about=abouts),dgufile,default_flow_style=False, sort_keys=False,allow_unicode=True)
                yaml.dump(adgu,dgufile)
                dgufile.write("---\n")
                dgufile.write(text)
                subprocess.check_call(['rm',filename[:-4]+'.md'])
                if dirout!="":
                    subprocess.check_call(['mv',filename+'.dgu',dirout])
            else:
                raise Exception("Not a latex file")



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
#! THIS ONE IS NOT FINISHED, I NEED A DIFFERENT APPROACH
def dgubookmd():

    parser = argparse.ArgumentParser(
        prog = 'dgubook',
        description = 'Aglomerates a number of .dgu files in a book - pdf format.',
        epilog = 'Results in a pdf file containing generic universal documents aglutinated.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    group.add_argument('-t','--tree',help="Iterates through the entire tree of documents of the present directory.",action='store_true',default=False)
    parser.add_argument('-o','--output',help="Selects an output folder",nargs=1) #! is not being used
    arguments = parser.parse_args()
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



def dgubook():

    parser = argparse.ArgumentParser(
        prog = 'dgubook',
        description = 'Aglomerates a number of .dgu files in a book - pdf format.',
        epilog = 'Results in a pdf file containing generic universal documents aglutinated.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    group.add_argument('-t','--tree',help="Iterates through the entire tree of documents of the present directory.",action='store_true',default=False)
    parser.add_argument('-o','--output',help="Selects an output folder",nargs=1) #! is not being used
    arguments = parser.parse_args()
    time = datetime.datetime.now()
    x = str(time)
    tempdgu = open('dgu2pdf.md','w')
    tempdgu.write("# PDF COMPILATION\n\n\n")
    tempdgu.write("### Compilation made via AnbToolKit\n\n")
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
                
                subprocess.check_call(args)

            else:
                raise Exception(elem + " is not a dgu file")
                
    if arguments.tree:
        
        for (dirpath,_,filenames) in os.walk(cwd):
            for filename in filenames:
              if filename.endswith('.dgu'):
                temp = open(dirpath+'/'+filename,'r').read()
                heading2Latex(temp,tempdgu)
                os.chdir(cwd)
                subprocess.check_call(args)
    
    tempdgu.close()

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
def genNote():
    parser = argparse.ArgumentParser(
        prog = 'genNote',
        description = 'Generates a note for a specific Ancestors Notebook Element',
        epilog = 'Composes a note to be filled by the user.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    arguments = parser.parse_args()
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


def genStory():
    cd = os.getcwd()
    parser = argparse.ArgumentParser(
        prog = 'genStory',
        description = 'Generates a Story in the accepted format for Ancestors Notebook',
        epilog = 'Composes a story to be filled by the user.')

    # Optional flags '-t', '-a', '-d'
    parser.add_argument('-t', '--title',required=True, help='Title of the story')
    parser.add_argument('-a', '--author', default="", help='Author of the story',nargs='+')
    parser.add_argument('-d', '--date', default=time.strftime('%Y-%m-%d'), help='the date of the story')
    parser.add_argument('-dgu',action='store_true',help='generates a Story dgu in Latex format')

    args = parser.parse_args()
    title = args.title
    date = args.date

    if author := args.author is None:
        print("It is assumed that the author is the current folder denomination") # this should be changed
        author = os.path.split(os.getcwd())[-1]
    
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
    parser = argparse.ArgumentParser(
        prog = 'genBio',
        description = 'Generates a Biography in the accepted format for Ancestors Notebook',
        epilog = 'Composes a Biography to be filled by the user.')

    parser.add_argument('-n', '--name',required=True, help='Name of the individual')
    parser.add_argument('-b', '--birth',default="", help='Date of Birth')
    parser.add_argument('-d', '--death',default="", help='Date of Death')
    parser.add_argument('-bp', '--birthplace',default="", help='BirthPlace')
    parser.add_argument('-o', '--occupation',default="", help="Individual's Job or Occupation")

    args = parser.parse_args()
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
    
    if args.dgu:
        with open(f'{filename}.dgu','w') as dgufo:
            print()
           # dgufo.write(dguBio(title,author,date,denomination))
    else:
        with open(f'{filename}.md','w') as mdfileobject:
            mdfileobject.write(skeletons.biography(name,birth,death,bp,o))



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
            
def anb():

    import argparse

    parser = argparse.ArgumentParser(prog='ancestors notebook')

    subparsers = parser.add_subparsers(dest='subcommand',required=True,help='List of subcommands accepted')
    init_parser = subparsers.add_parser('init')
    init_parser.add_argument('-s','--source',help='Specify a source fsgram file to generate an ancestors notebook', nargs=1)
    args = parser.parse_args()

    if args.subcommand == 'init':
        if args.source:
            file = args.source[0]
            initanb(os.path.abspath(file))
    
        else:
            initanb()
