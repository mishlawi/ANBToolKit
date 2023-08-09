import ply.lex as lex
from ply.lex import TOKEN


# terminais
tokens = ['PP','PF','PV','UNIVERSE','VIR','REGEX','ID','IDm','IDv','IDo','NAME','ARROW','LP','RP'] 

t_PP = r'\:'
t_PF = r'\.'
t_VIR = r'\,'
t_LP = r'\('
t_RP = r'\)'
t_UNIVERSE = r'>UNIVERSE<' # maybe change this flag lol
t_ARROW = r"\-\>"
t_PV = r'\;'

#p[0-9]+\-\w+\.\w+'
def t_REGEX(t):
    r"[a-z]+(\s+)?\."
    t.value = str(t.value)
    return t


# def t_UNIVERSE(t):
#     r'UNIVERSE(.|\n)+?(?=IGNORE)'
#     t.value=str(t.value)
#     return t


    
# def t_IGNORED(t):
#     r'IGNORE(.|\n)+'
#     t.value = str(t.value)
#     return t

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
