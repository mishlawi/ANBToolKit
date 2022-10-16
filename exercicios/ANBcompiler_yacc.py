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
    executable = re.sub('%%','',p[2]).strip()
    exec(executable)
    ignored = re.sub('IGNORE','',p[3]).strip().split('\n')    
    for elem in ignored:
        ignoredFiles.append(elem)
    


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




def p_IDS(p):
    "IDS : IDS VIR ID"
    p[0] = p[1] + [p[3]]


        
def p_IDSingle(p):
    "IDS : ID"
    p[0] = [p[1]]

def p_error(p):
    print("erro")
    print(p)


parser = yacc.yacc() 

fo = open("ANB.fsgram").read()

result = parser.parse(fo)
