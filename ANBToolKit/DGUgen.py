import os
import re 
import subprocess

#pandoc -s h2-moto4.tex -o h2-moto4.md
#pandoc -f markdown universoConceptual.dgu -o _.pdf

def generate(dirIn, dirOut, file):
    info = {'author':'','date':'','title':''}
    filename = re.split(r'\.',file)[0]
    os.chdir(dirIn)
    args = ['pandoc','-s', file, '-o', filename + '.md']
    subprocess.check_call(args)
    fo = open(f'{filename}.md').read()
    text = re.split('---',fo,1)[1]
    text = re.split('---',text)[0]
    titulo = re.split('title:',text)[1].strip()
    date = text[text.find('date:')+5 : text.find('title:')].strip()
    author = text[text.find('\n-')+2 : text.find("\ndate")].strip()
    info['title'] = titulo
    info['author'] = author
    info['date'] = date
    name = re.split('\-',filename)[0]
    id = re.split('\-',filename)[1]
    if 'h' == name[0] : 
        ftype = 'História' 
    elif 'b' == name[0] : 
        ftype = 'Biografia'
    elif 'p' == name[0] :
        ftype = 'Fotografia'
    else :
        ftype = 'undefined' 
    format = re.split(r'\.',file)[1]
    text = open(file).read()
    dgu = open(f'{filename}.dgu','w')
    if format == 'tex':
        #todo function to handle latex files
        handletex(text,dgu,id,format,ftype,titulo)
    #else:
        #todo accept as md file -> default
    subprocess.check_call(['mv',filename+'.dgu',dirOut])
    subprocess.check_call(['rm',filename+'.md'])
    #print(f"Generated {filename} in .md format")
    
# pandoc -f markdown universoConceptual.dgu -o _.pdf    
def handletex(text,dgu,id,format,ftype,titulo):
    print(text)
    abouts = re.findall(r"\\ind\{(.+)\}",text) # get anotted characters 
    dgu.write(dguInserter(id,format,ftype,abouts,titulo))
    text = re.search(r'\\begin\{document\}((.|\s)+)(\\end\{document\})$',text)
    text = text.group(1)
    text = text.replace("\printindex","")
    text = text.replace("\maketitle","")
    dgu.write(text)



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


    




dirin= "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/RootSorter/DuarteVilar"
dirout = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/RootSorter"


def dguAcopler():
    print("bruv")



generate(dirin,dirout,'h2-moto4.tex') 
