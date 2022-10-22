from operator import invert
import ply.yacc as yacc
import sys
import re
import os
from ANBcompiler_lex import tokens

ignoredFiles = []
executable = ''
grammar = {}


def p_FSGram(p):
    "FSGram : Prods PYTHON IGNORED"
    
    print(grammar)
    top = list(grammar.values())[0]
    verifyGrammar(top,grammar)
    ignored = re.sub('IGNORE','',p[3]).strip().split('\n')    
    for elem in ignored:
        ignoredFiles.append(elem)
    travessia(grammar,dirin,dirout)        
    executable = re.sub('%%','',p[2]).strip()
    print("\n\n*******\nPYTHON\n*******")
    exec(executable)


def p_Prods(p):
    "Prods : Prod Prods"


def p_Prodsingle(p):
    "Prods : Prod"


def p_Prod(p):
    "Prod : ID PP IDS PF"
    
    if p[1] in grammar.keys():
        aux = grammar[p[1]]
        aux.append(p[3])
        grammar[p[1]] = aux
    else:
        grammar[p[1]] = [p[3]]


def p_ProdSimple(p):
    "Prod : ID PP REGEX"
    try:
        re.compile(p[3])
        if p[1] in grammar.keys():
            aux = grammar[p[1]]
            aux.append(p[3])
            grammar[p[1]] = aux
        else:
            grammar[p[1]] = [p[3]]
    except re.error:
        print("Regex inválido")
        exit()



def p_IDS(p):
    "IDS : IDS VIR ID"
    p[0] = p[1] + [p[3]]
        
def p_IDSingle(p):
    "IDS : ID"
    p[0] = [p[1]]

def p_IDPLUS(p):
    "IDS : IDM"
    p[0] = [p[1]]

def p_IDTIMES(p):
    "IDS : IDV"
    p[0] = [p[1]]

def p_error(p):
    print("erro")
    print(p)

def verifyGrammar(lista,grammar):
    for producao in lista:
        print(producao)
        for id in producao:
            if id[-1] == '*' or id[-1] == "+":
                id = id[:-1]
            print(id)

            if id not in grammar.keys():
                print("Gramatica mal formulada")

def invertedSuper(id,grammar):
    if len(grammar[id])==1:
        print("regex",grammar[id])
        return grammar[id]


def travessia(grammar,DirIn,DirOut):

    # for subdir, dirs, files in os.walk(DirIn):
    #     ficheiros=[]
    #     for file in files:
    #         ficheiros.append(file)
    #         #print(os.path.join(subdir, file))
    ficheiros = []
    for file in os.listdir(DirIn):
        if os.path.isfile(os.path.join(DirIn, file)):
            ficheiros.append(file)
            print(file)

    top = list(grammar.values())[0]
    disposal = []
    for elem in top:
        for id in elem:
            if id[-1]=='*': # 0 or plus elements
                id = id[:-1]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                print(regex)
                for elem in ficheiros:
                    if re.match(regex,elem):    
                        disposal.append(elem)
            
            elif id[-1]=='+': # 1 or plus elements
                id = id[:-1]
                count = 0
                regex = grammar[id]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                for elem in ficheiros:
                    print(elem)
                    if re.match(regex,elem):
                        disposal.append(elem)
                        count+=1
                if count==0: 
                    print("não existem um ou mais ficheiros do tipo enunciado na gramática")
            
            else: # 1 one element only
                count=0
                regex = grammar[id]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                for elem in ficheiros:
                    if re.match(regex,elem):
                        disposal.append(elem)
                        count+=1
                if count!=1:
                    print("existem ficheiros a mais ou a menos")
    print(disposal)



dirin = '/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/exercicios/DuarteVilar'
dirout = '/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/exercicios/OUT'



#directory_path = os.getcwd()
#print(directory_path)

parser = yacc.yacc() 

fo = open("ANB.fsgram").read()

result = parser.parse(fo)
