import ply.yacc as yacc
import re
from .handlers.html.htmlLogic import *
from .handlers.grammar.gramLogic import *
from .FSGramTokens import tokens
from .DGUhand import *
from .Constants import *

#todo nao ir ao topo da produção
grammar = {}
terminals = {}
nonterminals = {}

def universehand(universe):
    galaxies = universe.split('\n')
    
    for elem in galaxies:
        print(elem)
        if len(values:=re.split(r'\-\>',elem))>1:
            entity = values[0]
            atributes = values[1]
            atributes = re.split(r'::',atributes)
            subclass = dgu_subclass(entity,atributes)

def p_FSGram(p):
    "FSGram : Prods UNIVERSE FORMATS IGNORED"
    ignoredFiles = []
    executable = ''
    top = list(grammar.values())[0]
    verifyGrammar(top,grammar)
    universe = re.sub('UNIVERSE','',p[2]).strip()
    formats = re.sub('FORMATS','',p[3]).strip()
    #universehand(universe)
    ignored = re.sub('IGNORE','',p[4]).strip().split('\n')    
    bigbang(universe,formats)
    
    for elem in ignored:
        ignoredFiles.append(elem)
    interpreter(terminals,nonterminals)
    

    #! keep tagged, needs maintance
    # disposal = travessia(grammar,dirin,dirout,ignoredFiles)
    # genHtml(disposal,dirout,dirin)
    
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



dirin = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/RootSorter/DuarteVilar"
dirout = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/RootSorter/OUT"


def initializer(res=''):
    parser = yacc.yacc()
    if res=='' :
        result = parser.parse(defaultFsgram)
    else:
        result = parser.parse(res) 

    return result