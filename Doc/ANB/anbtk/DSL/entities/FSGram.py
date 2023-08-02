import ply.yacc as yacc
import re


from .FSGramTokens import tokens,lexer_fsgram
from ...auxiliar import constants


#todo nao ir ao topo da produção


grammar = {}
terminals = {}
nonterminals = {}
entityuniverse = {}

def p_FSGram(p):
    "FSGram : Entities UNIVERSE Prods"
    universe =  re.sub('UNIVERSE','',p[2]).strip()

    # gramLogic.process_fsgram(top,grammar,universe,terminals,nonterminals)
    p[0] = grammar,universe,terminals,nonterminals
    # return ignoredFiles,grammar
   
def p_Entities(p):
    """Entities : Entities Entity
                | Entity 
    """

def p_Entity(p):
    """Entity : ID Abreviation ARROW Attributes PV"""
    #   if p[1]!=p[2] :
    #         if len(p[1])>len(p[2]):
    # else:
    #             print(f"{p[2]} is supposed to be an abbreviation, not a longer name than {p[1]}.")
    #             exit()
    #     else:
    #         print(f"{p[2]} is supposed to be different than {p[1]}.")
    #         exit()
    entityuniverse[p[1]] = (p[2],p[4])

def p_Abreviation(p):
    """Abreviation : LP ID RP
                   | empty
    """
    if len(p) == 4:
        p[0] = p[2]
            
        

def p_Attributes(p):
    """
    Attributes : Attributes VIR Attribute 
               | Attribute
    """
    if len(p) == 4:
        if p[3] in p[1]:
            print(f"{p[3]} is already an attribute of {p[1]}, so it can't be added again.")
            exit()
        else:
            p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_Attribute(p):
    """
    Attribute : ID 
    """
    p[0] = p[1]


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



def p_empty(p):
    '''
    empty :
    '''
    pass


def p_error(p):
    if p is not None:
        print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}'")
    else:
        print("Syntax error: Unexpected end of input")




def get_entities_abbreviations(entityuniverse):
    return {k:v[0] for k,v in entityuniverse.items()}


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
    global entityuniverse

    nonterminals,terminals,entityuniverse = {} , {} , {}

    parser = yacc.yacc()
    result = parser.parse(data,lexer=lexer_fsgram)
    
    # lexer_fsgram.input(data)
    # while True:
    #     token = lexer_fsgram.token()
    #     if not token:
    #         break  # no more tokens
    #     print(token)
    print(entityuniverse)
    return result


def parse_individual_production(data):
    global nonterminals
    nonterminals = {}
    single_prod_parser = yacc.yacc(start='Prods')
    single_prod_parser.parse(data,lexer=lexer_fsgram)
    return nonterminals

