import ply.yacc as yacc
import re


from .FSGramTokens import tokens,lexer_fsgram
from ...auxiliar import constants


#todo nao ir ao topo da produção


grammar = {}
terminals = {}
nonterminals = {}


def p_FSGram(p):
    "FSGram : Prods UNIVERSE IGNORED"
    universe = re.sub('UNIVERSE','',p[2]).strip()
    ignoredFiles = list(re.sub('IGNORE','',p[3]).strip().split('\n'))
    top = list(grammar.values())[0]

    # gramLogic.process_fsgram(top,grammar,universe,terminals,nonterminals)
    p[0] = top,grammar,universe,terminals,nonterminals
    # return ignoredFiles,grammar
   


def p_Prods(p):
    "Prods : Prod Prods"



def p_Prodsingle(p):
    """Prods : Prod"""




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
    "IDgen : IDo"
    p[0] = [p[1]]

def p_error(p):
    print("error")
    print(p)




def initializer(res=''):
    global nonterminals
    global terminals
    nonterminals,terminals = {} , {}
    parser = yacc.yacc()
    if res=='' :
        result = parser.parse(constants.defaultFsgram,lexer=lexer_fsgram)
        
    else:
        result = parser.parse(res,lexer=lexer_fsgram)


    return result

def parse_grammar(data):

    global nonterminals
    global terminals

    nonterminals,terminals = {} , {}

    parser = yacc.yacc()
    result = parser.parse(data,lexer=lexer_fsgram)
    
        

    return result


def parse_individual_production(data):
    global nonterminals
    nonterminals = {}
    single_prod_parser = yacc.yacc(start='Prods')
    single_prod_parser.parse(data,lexer=lexer_fsgram)
    return nonterminals

