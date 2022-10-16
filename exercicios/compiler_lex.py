import ply.lex as lex


#reserved = {}

tokens = ['STORY','BIO','PHOTO']

def t_STORY(t):
    r's[0-9]+\-[a-zA-Z]+\.[a-z]+'
    t.value = str(t.value)
    return t


def t_BIO(t):
    r'b[0-9]+\-[a-zA-Z]+\.[a-z]+'
    t.value = str(t.value)
    return t


def t_PHOTO(t):
    r'p[0-9]+\-[a-zA-Z]+\.[a-z]+'
    t.value = str(t.value)
    return t



def t_error(t):
    t.lexer.skip(1)
    return t


lexer = lex.lex()