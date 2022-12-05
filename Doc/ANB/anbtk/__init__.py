""" ANB toolkit module for """

__version__ = "0.0.1"

import re
import os
import sys


# get yaml to convert
def parseAbstractDgu(filename,path=""):
    if re.split(r'\.',filename)[1] == 'dgu':
        info = {'type':'','format':'','id':'', 'body' : []}
        #os.chdir(path)
        fo = open(filename).read()
        print(fo)
        if (x:=re.search(r'type :  ([a-zA-Z]+)',fo)) != None:
            info["type"] = x.group(1)
        if (x:= re.search(r'format : ([a-zA-Z]+)',fo)) != None:
            info["format"] = x.group(1)
        if (x:= re.search(r'id : ([a-zA-Z]+)',fo)) != None:
            info["id"] = x.group(1)
        texts = re.split(r"\=\=\=",fo)[1:]
        for elem in texts:
            info['body'].append(elem)
        print(info)
        return info            
    
    else:
        ValueError("File Format is invalid")

def texSkel(adgu):
    string = f"""\\section{{{adgu.get('title',"missing title")}}}
    \\footnote{{{adgu.get('about',"")}}}
    {adgu['body']}
    """
    return string


def dgu2tex(adgu):
    if adgu['format'] == 'tex':
        return texSkel(adgu)
    else:
        return ""

def mainDgu2tex():
    for file in sys.argv[1:]:
        print(dgu2tex(parseAbstractDgu(file)))
    
