import ply.yacc as yacc
import sys
import re
import os
from compiler_lex import tokens


def p_Person(p):
    "Person : STORIES BIO PHOTO"
    p[0] = p[1] + p[2] + p[3]

def p_stories(p):
    "STORIES : STORY STORIES"
    p[0] = p[1] + p[2]

def p_stories_unique(p):
    "STORIES : STORY"
    p[0] = p[1]

def p_error(p):
    print("erro")
    print(p)


def dirName():
    dir = str(re.split('/',os.getcwd())[-1])
    files = []
    files = re.findall('[A-Z][^A-Z]*', dir)

    name = ''
    for elem in files:
        name+= elem + ' '
    return name 


def fileList():
    story = r"s[0-9]+\-[a-zA-Z]+\.[a-z]+"
    bio = r"b[0-9]+\-[a-zA-Z]+\.[a-z]+"
    pic = r"p[0-9]+\-[a-zA-Z]+\.[a-z]+"

    files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.getcwd()+'/'+f)]
    
    sorter = [story,bio,pic]
    print(sorter.index(r"s[0-9]+\-[a-zA-Z]+\.[a-z]+"))
    files.sort(key = lambda i: sorter.index(i)  )
    print(files)

    

    #return ficheiros

fileList()

parser = yacc.yacc() 