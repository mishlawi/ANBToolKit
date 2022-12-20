import re
import os
import subprocess
import json
import yaml 

# TODO -> timestamp
def genNote(file):
    name = re.split("\.",file)[0]
    format = re.split("\.",file)[1]
    cwd = os.getcwd()
    
    #with open("/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/RootSorter/data/notes.json","r") as fo:
     #       data = json.load(fo)
    #os.chdir(dirIn)
    
    identifier = re.split("-",name)[0]
    # if identifier not in data["documents"].keys():
    if format == 'tex':
        #os.chdir(dirIn)
        args = ['pandoc','-s', file, '-o', name + '.md']
        subprocess.check_call(args)
        fo = open(f'{name}.md').read()
        headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",fo).group()
        adgu = yaml.full_load(headers)
        subprocess.check_call(['rm',f"{name}.md"])
        #data["size"]=len(data["documents"].keys())+1
        #data["documents"][identifier] = (notename,dirIn)
        notename = "note" + '-' + re.split("-",name)[1] 
        body = noteSkeleton(notename,adgu.get('title','no title'),adgu.get('author','no author available'),adgu.get('date','no date available'))
        foNote = open(f"{identifier}.anbnote",'w')
        foNote.write(body)
        # with open("/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/RootSorter/data/notes.json","w") as fo:
        #     json.dump(data,fo)
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
    
    
