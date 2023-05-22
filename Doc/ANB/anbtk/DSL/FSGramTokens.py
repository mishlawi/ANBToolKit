import ply.lex as lex
from ply.lex import TOKEN


# terminais
tokens = ['PP','PF','UNIVERSE','VIR','IGNORED','REGEX','ID','IDm','IDv','IDo'] 

t_PP = r'\:'

t_PF = r'\.'

t_VIR = r'\,'

def t_REGEX(t):
    r'r\'.+\''
    t.value = str(t.value)
    return t


# UNIVERSE\n(.+|\n)+?(?=FORMATS)
# STATE CONDITIONS
# ADICIONAR LOOKAHEAD


def t_UNIVERSE(t):
    r'UNIVERSE(.|\n)+?(?=IGNORE)'
    t.value=str(t.value)
    return t



def t_IGNORED(t):
    r'IGNORE(.|\n)+'
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


lexer = lex.lex()

