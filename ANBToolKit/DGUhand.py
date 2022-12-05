import os
import re 
import yaml
import subprocess
import datetime

from DGU import DGU as dgu




#pandoc -s h2-moto4.tex -o h2-moto4.md
#pandoc -f markdown universoConceptual.dgu -o _.pdf


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
        abouts = re.findall(r"\\ind\{(.+)\}",file)
        yaml.dump(dgu(id = id,format = format,type=type,about=abouts),dgufile,default_flow_style=False, sort_keys=False,allow_unicode=True)
        yaml.dump(adgu,dgufile)
        dgufile.write("---\n")
        dgufile.write(text)
        subprocess.check_call(['rm',filename[:-4]+'.md'])
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

#maybe add current dir, then go to the paths, then temporarly move them to the og folder then rm them ?
#title of the pdf should be described in yaml then processed naturally
def dgus2pdf(dirout=""):
    time = datetime.datetime.now()
    x = str(time)
    tempdgu = open('dgu2pdf.md','w')
    tempdgu.write("# PDF COMPILATION\n\n\n")
    tempdgu.write("### Compilation made via AnbToolKit\n\n")
    tempdgu.write(f"Processed and generated on {x[:10]}.\n\n\n")
    tempdgu.write('\pagebreak\n\n')
    args = ['pandoc', '-f','markdown','dgu2pdf.md','-o','doc.pdf']
    cwd = os.getcwd()
    print(cwd)
    for (dirpath,dirname,filenames) in os.walk(cwd):
        for filename in filenames:
            if filename.endswith('.dgu'):
                temp = open(dirpath+'/'+filename,'r').read()
                tempdgu.write(temp)
                tempdgu.write('\pagebreak\n\n')
    os.chdir(cwd)
    tempdgu.close()
    subprocess.check_call(args)

    # for dgu in dgus:
    #     os.chdir(os.path.dirname(dgu))
    #     name = os.path.basename(dgu)
    #     args.append(name)
    #     # tempdgu.write("<space><space>")
    #subprocess.check_call(['rm',"dgu2pdf.tempdgu"])

    
# pandoc -f markdown universoConceptual.dgu -o _.pdf
    
def handletex(text,dgu,id,format,ftype,titulo):
    print(text)
    abouts = re.findall(r"\\ind\{(.+)\}",text) # get anotted characters 
    dgu.write(dguInserter(id,format,ftype,abouts,titulo))
    dgu.write("\n===")
    text = re.search(r'\\begin\{document\}((.|\s)+)(\\end\{document\})$',text)
    text = text.group(1)
    text = text.replace("\printindex","")
    text = text.replace("\maketitle","")
    dgu.write(text)


# adds different type of elements from latex into a dgu         
def dguInserter(id,formato,type,about,title):
    const = f"""---
id : {id}
format : {formato}
type  : {type}

about :"""

    for elem in about:
        const += '\n\t- ' + elem
    const+= f"""\n\ntitle: {title}
---"""
    return const





# generates universe.dgu and formats.dgu
def bigbang(stringUniverse,stringFormats):
    uniformats = re.findall(r'\w+',stringUniverse)
    formatformats = re.findall(r'\w+',stringFormats)
    universeAbout = "Universe of entities currently being used in this ancestors notebook"
    formatsAabout = "Accepted types of file formats"
    print(uniformats)
    with open(r'universe.dgu', 'w') as file:
        file.write("---\n")
        yaml.dump(dgu(id = "Universe",format = "free?",type="universe?",about=[universeAbout]),file,default_flow_style=False, sort_keys=False)
        file.write("---\n\n")
        for elem in uniformats:
            file.write(f"* {elem}\n")
    # usar o objeto dgu para inserir coisas
    with open(r'formats.dgu', 'w') as file:
        file.write("---\n")
        yaml.dump(dgu(id = "Formats",format = "free?",type="formats?",about=[formatsAabout]),file,default_flow_style=False, sort_keys=False)
        file.write("---\n\n")
        for elem in formatformats:
            file.write(f"* {elem}\n")

    


dirin= "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/ANBToolKit/ClaraVilar"
dirout = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/ANBToolKit/ClaraVilar"
test ="/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/ANBToolKit/h2-moto4.dgu"
#tex2dgu(test)
dgus2pdf([test])

#generate(dirin,dirout,'h2-moto4.tex') 
#parseAbstractDgu('formatos.dgu',dirout)
