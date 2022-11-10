import ply.yacc as yacc
import re
from handlers.html.fsgramHtml import *
from handlers.grammar.fsGrammar import *
from ANBcompiler_lex import tokens


# nao ir ao topo da produção
grammar = {}
terminals = {}
nonterminals = {}

def p_FSGram(p):
    "FSGram : Prods PYTHON IGNORED"
    
    ignoredFiles = []
    executable = ''
    print(grammar)
    top = list(grammar.values())[0]
    verifyGrammar(top,grammar)
    ignored = re.sub('IGNORE','',p[3]).strip().split('\n')    
    
    for elem in ignored:
        ignoredFiles.append(elem)
    interpreter(terminals,nonterminals)
    #travessia(grammar,dirin,dirout,ignoredFiles)        
    print("\n\n*******\nPYTHON\n*******")
    executable = re.sub('%%','',p[2]).strip()
    exec(executable)
    print("\n\n\n")
    print("Nao terminais",nonterminals)
    print("Terminais",terminals)


def p_Prods(p):
    "Prods : Prod Prods"


def p_Prodsingle(p):
    "Prods : Prod"

# basically non terminal
def p_Prod(p):
    "Prod : ID PP IDS PF"
    nonterminals[p[1]] = p[3]
    if p[1] in grammar.keys():
        aux = grammar[p[1]]
        aux.append(p[3])
        grammar[p[1]] = aux
    else:
        grammar[p[1]] = [p[3]]

# basically terminal
def p_ProdSimple(p):
    "Prod : ID PP REGEX"
    try:
        re.compile(p[3])
        terminals[p[1]] = p[3]
        grammar[p[1]] = [p[3]]

    except re.error:
        print("Regex inválido")
        exit()

def p_IDS(p):
    "IDS : IDS VIR IDgen"
    p[0] = p[1] + p[3]

def p_IDgen(p):
    "IDS : IDgen"
    p[0] = p[1]
        
def p_IDSingle(p):
    "IDgen : ID"
    p[0] = [p[1]]

def p_IDPLUS(p):
    "IDgen : IDm"
    p[0] = [p[1]]

def p_IDTIMES(p):
    "IDgen : IDv"
    p[0] = [p[1]]

def p_IDOPTN(p):
    "IDS : IDo"
    p[0] = [p[1]]

def p_error(p):
    print("erro")
    print(p)


dirin = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/exercicios/DuarteVilar"
dirout = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/exercicios/OUT"

parser = yacc.yacc() 

fo = open("ANB.fsgram").read()

result = parser.parse(fo)
