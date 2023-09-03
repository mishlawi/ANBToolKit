import ply.lex as lex
from ply.lex import TOKEN


# terminais
tokens = ['PP','PF','PV','UNIVERSE','VIR','PREFIX','ID','IDm','IDv','IDo','ARROW','LP','RP'] 

t_PP = r'\:'
t_PF = r'\.'
t_VIR = r'\,'
t_LP = r'\('
t_RP = r'\)'
t_UNIVERSE = r'>UNIVERSE<' # maybe change this to something else
t_ARROW = r"\-\>"
t_PV = r'\;'


def t_PREFIX(t):
    r"[a-z]+(\s+)?\."
    t.value = str(t.value)
    return t


# id with symbol "?"
def t_IDo(t):
    r'[a-zA-Z]+\?'
    t.value=str(t.value)
    return t

# id with symbol "+"
def t_IDm(t):
    r'[a-zA-Z]+\+'
    t.value=str(t.value)
    return t

# id with symbol "*"
def t_IDv(t):
    r'[a-zA-Z]+\*'
    t.value=str(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z]+'
    t.value=str(t.value)
    return t


t_ignore=' \n\t\r'

def t_error(t):
    t.lexer.skip(1)
    return t


lexer_fsgram = lex.lex()

# Get each token recognized by the lexer
