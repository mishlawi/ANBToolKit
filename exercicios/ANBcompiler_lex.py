import ply.lex as lex


#reserved = {}

tokens = ['PP','PF','PYTHON','VIR','ID','IGNORED']

t_PP = r'\:'

t_PF = r'\.'

t_VIR = r'\,'



def t_IGNORED(t):
    r'IGNORE\n(.|\n)+'
    t.value = str(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z]+'
    t.value=str(t.value)
    return t

def t_PYTHON(t):
    r'\%\%\n(.|\n)+\%\%'
    t.value=str(t.value)
    return t

t_ignore=' \t\n\r'

def t_error(t):
    t.lexer.skip(1)
    return t


lexer = lex.lex()


