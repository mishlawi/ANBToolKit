""" ANB toolkit module for """

__version__ = "0.0.1"

import re
import os
import sys
import subprocess
import yaml
import datetime
from DGU import DGU as dgu
from FSGram import initializer
import argparse

# Gets header and body of dgu and turns it in a dictionary
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

############################################

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

############################################

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

#################################################
def dgubook():
    parser = argparse.ArgumentParser(
        prog = 'dgubook',
        description = 'Aglomerates a number of .dgu files in a book - pdf format.',
        epilog = 'Results in a pdf file containing generic universal documents aglutinated.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    group.add_argument('-t','--tree',help="Iterates through the entire tree of documents of the present directory.",action='store_true',default=False)
    parser.add_argument('-o','--output',help="Selects an output folder",nargs=1)
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
                textInserter(temp,tempdgu)
                os.chdir(cwd)
                
                subprocess.check_call(args)

            else:
                raise Exception(elem + " is not a dgu file")
                
    if arguments.tree:
        
        for (dirpath,_,filenames) in os.walk(cwd):
            for filename in filenames:
              if filename.endswith('.dgu'):
                temp = open(dirpath+'/'+filename,'r').read()
                textInserter(temp,tempdgu)
                os.chdir(cwd)
                subprocess.check_call(args)
    
    tempdgu.close()


def textInserter(temp,tempdgu):
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


########################################################
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
                            body = noteSkeleton(notename,adgu.get('title',' '),adgu.get('author',' '),adgu.get('date',' '))
                            foNote = open(f"{identifier}.anbnote",'w')
                            foNote.write(body)
                            foNote.close()
                        # more formats to be added
                            

def noteSkeleton(notename,title,author,date):
    skeleton=f"""---
name: {notename}
title: {title}
author: {author}
date: {date}
---

# Relevant info


===
#""" + """{}"""
    return skeleton


def initanb():
    cwd = os.getcwd()
    if os.path.exists(cwd + '/.anbtk'):
        raise Exception("This folder was already initialized as an ancestors notebook.")
        
    else:
        os.mkdir(cwd + '/.anbtk')

    # group = parser.add_mutually_exclusive_group()
    # group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    # group.add_argument('-t','--tree',help="Iterates through the entire tree of documents of the present directory.",action='store_true',default=False)
    # parser.add_argument('-o','--output',help="Selects an output folder",nargs=1)

def anb():
    parser = argparse.ArgumentParser(prog='anbtk')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('init',action='store_true')

    #subparsers = parser.add_subparsers(title='init',required=False)
    # parser.add_argument('init',action='store_true',help="initialize a ancestors notebook")
    #parser_a = subparsers.add_parser(name = 'init' ,help='init help')
    # parser_a.add_argument('-s','--source', help='select source file', nargs=1)
    
    

    
    
    args =
    print(args)
    if args is None:
        print("asjglaksgjslakjg") 
    else:
        print("a.sgkjalskg")




anb()