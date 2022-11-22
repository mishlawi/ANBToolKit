import re
import os
import subprocess
import json

def genNote(file,dirIn):
    name = re.split("\.",file)[0]
    format = re.split("\.",file)[1]
    os.chdir(dirIn)
    with open("/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/RootSorter/data/notes.json","r") as fo:
            data = json.load(fo)
    
    identifier = re.split("-",name)[0]
    if identifier not in data["documents"].keys():
        if format == 'tex':
            #fDgu = open(f"{name}.dgu").read()
            #info = {'author':'','date':'','title':''}
            os.chdir(dirIn)
            args = ['pandoc','-s', file, '-o', name + '.md']
            subprocess.check_call(args)
            fo = open(f'{name}.md').read()
            text = re.split('---',fo,1)[1]
            text = re.split('---',text)[0]
            title = re.split('title:',text)[1].strip()
            date = text[text.find('date:')+5 : text.find('title:')].strip()
            author = text[text.find('\n-')+2 : text.find("\ndate")].strip()
            subprocess.check_call(['rm',f"{name}.md"])
            data["size"]=len(data["documents"].keys())+1
            notename = "note" + str(data["size"])
            data["documents"][identifier] = (notename,dirIn)
            body = noteSkeleton(notename,title,author,date)
            foNote = open(f"{identifier}.anbnote",'w')
            foNote.write(body)
            with open("/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/RootSorter/data/notes.json","w") as fo:
                json.dump(data,fo)
    else:
        print("nota já existe")






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


genNote("h1-viagemCaboVerde.tex","/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/RootSorter/DuarteVilar")
    
    
