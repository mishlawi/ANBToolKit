import os
import re 
import yaml
import subprocess
import datetime
import sys
from pathlib import Path


from DGU import DGU as dgu


#pandoc -s h2-moto4.tex -o h2-moto4.md
#pandoc -f markdown universoConceptual.dgu -o _.pdf


# generates universe.dgu and formats.dgu
def bigbang(stringUniverse,stringFormats):
    uniformats = re.findall(r'\w+',stringUniverse)
    formatformats = re.findall(r'\w+',stringFormats)
    universeAbout = "Universe of entities currently being used in this ancestors notebook"
    formatsAabout = "Accepted types of file formats"
    print(uniformats)
    with open(r'universe.dgu', 'w') as file:
        file.write("---\n")
        yaml.dump(dgu(id = "Universe",format = "dgu",type="universe?",about=[universeAbout]),file,default_flow_style=False, sort_keys=False)
        file.write("---\n\n")
        for elem in uniformats:
            file.write(f"* {elem}\n")

    # usar o objeto dgu para inserir coisas
    with open(r'formats.dgu', 'w') as file:
        file.write("---\n")
        yaml.dump(dgu(id = "Formats",format = "dgu",type="formats?",about=[formatsAabout]),file,default_flow_style=False, sort_keys=False)
        file.write("---\n\n")
        for elem in formatformats:
            file.write(f"* {elem}\n")



#############

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
    string=""
    if len(abouts)>0:
        for elem in abouts:
            string+= f"\\footnote{{{elem}}}\n"
        return string
    else:
        return ""

def texSkeleton(texadgu):
    string = f"""\\section{{{texadgu.get('title',"missing title")}}}
{aboutism(texadgu.get('about',[]))}   
    \\begin{{center}}
        $\\ast$~$\\ast$~$\\ast$
    \\end{{center}}
    {texadgu.get('body',"")}
    """
    print(string)
    return string

# ver como adicionar body a adgu
def dgu2tex(file):
    adgu = parseAbstractDgu(file)
    if adgu['format'] == 'latex':
        return texSkeleton(adgu)
    else:
        return ""

def mainDgu2tex():
    for file in sys.argv[1:]:
        print(dgu2tex(file))

############################################

def dgu2texbook():
    fo = open("texbook.tex",'w')
    fo.write(f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{imakeidx}}
\\makeindex
\\begin{{document}}\n""")

    if "-s" in sys.argv and len(sys.argv)>2:
        for file in sys.argv[2:]:
            temp = open(file,'r').read()
            headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",temp).group()
            adgu = yaml.full_load(headers)
            text = re.split(r'\-\-\-',temp)[2]
            adgu['body'] = text
            fo.write(texSkeleton(adgu))
    if len(sys.argv)==1:
        cwd = os.getcwd()
        for (dirpath,_,filenames) in os.walk(cwd):
            for filename in filenames:
                if filename.endswith('.dgu'):
                    temp = open(dirpath+'/'+filename,'r').read()
                    headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",temp).group()
                    adgu = yaml.full_load(headers)
                    text = re.split(r'\-\-\-',temp)[2]
                    adgu['body'] = text
                    fo.write(texSkeleton(adgu))
                    fo.write("\t")
                    fo.write("\n")
                    fo.write("\pagebreak")
    fo.write("\end{document}")
    
    fo.close()

    
############################################

def tex2dgu(path,dirout=""):
    filename = os.path.basename(path)
    if filename.endswith(".tex"):
        file = open(filename).read()
        os.chdir(os.path.dirname(path))
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
        raise TypeError("Not a latex file")



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

################################################
#generates a pdf book of the dgus of the current dir and the current dir children's dgus

def dgubook():
    time = datetime.datetime.now()
    x = str(time)
    tempdgu = open('dgu2pdf.md','w')
    tempdgu.write("# PDF COMPILATION\n\n\n")
    tempdgu.write("### Compilation made via AnbToolKit\n\n")
    tempdgu.write(f"Processed and generated on {x[:10]}.\n\n\n")
    tempdgu.write('\pagebreak\n\n')
    args = ['pandoc', '-f','markdown','dgu2pdf.md','-o','dgu2pdf.pdf']
    cwd = os.getcwd()
    for (dirpath,_,filenames) in os.walk(cwd):
        for filename in filenames:
            if filename.endswith('.dgu'):
                temp = open(dirpath+'/'+filename,'r').read()
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
    os.chdir(cwd)
    tempdgu.close()
    subprocess.check_call(args)
    #subprocess.check_call(['rm','dgu2pdf.md'])

dirin= "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/ANBToolKit/ClaraVilar"
dirout = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/ANBToolKit/ClaraVilar"
test ="/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/ANBToolKit/h2-moto4.dgu"
test2="/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/ANBToolKit/h1-viagemCaboVerde.tex"

#tex2dgu(test2)
dgubook()
dgu2texbook()
#dgu2tex(test)~
#mainDgu2tex()