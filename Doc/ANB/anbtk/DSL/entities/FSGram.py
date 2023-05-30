import ply.yacc as yacc
import re


from .FSGramTokens import tokens,lexer_fsgram
from . import gramLogic
from ...dgu import DGUhand
from ...auxiliar import constants

#todo nao ir ao topo da produção


grammar = {}
terminals = {}
nonterminals = {}

def universehand(universe):
    galaxies = universe.split('\n')
    
    for elem in galaxies:
    
        if len(values:=re.split(r'\-\>',elem))>1:
            entity = values[0]
            atributes = values[1]
            atributes = re.split(r'::',atributes)
            subclass = DGUhand.dgu_subclass(entity,atributes)



def p_FSGram(p):
    "FSGram : Prods UNIVERSE  IGNORED"
    ignoredFiles = []
    executable = ''
    top = list(grammar.values())[0]
    gramLogic.verifyGrammar(top,grammar)
    universe = re.sub('UNIVERSE','',p[2]).strip()
    #universehand(universe)
    ignored = re.sub('IGNORE','',p[3]).strip().split('\n')    
    
    for elem in ignored:
        ignoredFiles.append(elem)
    gramLogic.interpreter(terminals,nonterminals)
    
    DGUhand.bigbang(universe,terminals)

    #! keep tagged, needs maintance
    # disposal = travessia(grammar,dirin,dirout,ignoredFiles)
    # genHtml(disposal,dirout,dirin)
    
    print("\n\n")
    print("fsgram file declarations:")
    print(" * non terminals",nonterminals)
    print(" * terminals",terminals)
    print("\n\n")


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
    print("error")
    print(p)



# dirin = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/RootSorter/DuarteVilar"
# dirout = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/RootSorter/OUT"


parser = yacc.yacc()

def initializer(res=''):
    if res=='' :
        result = parser.parse(constants.defaultFsgram,lexer=lexer_fsgram)
    else:
        result = parser.parse(res,lexer=lexer_fsgram) 

    return result