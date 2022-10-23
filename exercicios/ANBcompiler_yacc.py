import ply.yacc as yacc
import sys
import imghdr
import shutil
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
    print("\n\n*******\nPYTHON\n*******")
    executable = re.sub('%%','',p[2]).strip()
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
        for id in producao:
            if id[-1] == '*' or id[-1] == "+":
                id = id[:-1]

            if id not in grammar.keys():
                print("Gramatica mal formulada")

# def invertedSuper(id,grammar):
#     if len(grammar[id])==1:
#         print("regex",grammar[id])
#         return grammar[id]


def travessia(grammar,dirIn,dirOut):
    
    # gets files
    ficheiros = []
    for file in os.listdir(dirIn):
        if os.path.isfile(os.path.join(dirIn, file)):
            ficheiros.append(file)
            print(file)

    # gets top production that defines the grammar
    top = list(grammar.values())[0]
    disposal = []
    
    # iterates through the productions that compose the top production
    for elem in top:
        for id in elem:
    
            # verifies types if productions have different elements

            if id[-1]=='*': # 0 or plus elements
                id = id[:-1]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                
                for elem in ficheiros:
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:    
                        disposal.append(elem)
            
            elif id[-1]=='+': # 1 or plus elements
                id = id[:-1]
                count = 0
                regex = grammar[id]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                
                for elem in ficheiros:
                    print(elem)
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:
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
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:
                        disposal.append(elem)
                        count+=1
                if count > 1:
                    print("existem ficheiros a mais")

                elif count < 1:
                    print("existem ficheiros a menos")
    print(disposal)
    genHtml(ficheiros,dirOut,dirIn)


def genHtml(files,dirOut,dirIn):

    #? maybe understand how should the html public folder creation should be organized

    directory = "public"
    path = os.path.join(dirOut,directory)
    if not os.path.exists(path):
        os.mkdir(path)
    for file in files:
        considered = os.path.join(dirIn,file)

        # image
        if imghdr.what(considered):
            img = os.path.join(dirIn,file)
            shutil.copy(img,path)

    #! it might be important to define case by case for each format the equivalent converter, unless a more simple aproach can be pursued      

        

dirin = '/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/exercicios/DuarteVilar'
dirout = '/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/exercicios/OUT'



#directory_path = os.getcwd()
#print(directory_path)

parser = yacc.yacc() 

fo = open("ANB.fsgram").read()

result = parser.parse(fo)
