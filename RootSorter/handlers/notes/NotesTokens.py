import ply.lex as lex

tokens = ["DELIMITER","ANCHOR","NAME","TITLE","AUTHOR","DATE","TEXT"]

t_HDELIMETER = r'\-\-\-'
t_DELIMETER = r'\=\=\='
t_ANCHOR = r'\#'

def t_NAME(t):
    r'\=\=\= \w+([0-9]{1,5})?'
    t.value = str(t.value.replace(r"\=\=\= ",''))
    return t

def t_TITULO(t):
    r'title: [a-zA-Z]+'
    t.value = str(t.value.replace(r"title ",''))
    return t

def t_AUTHOR(t):
    r'author: [a-zA-Z]+'
    t.value = str(t.value.replace(r"author ",''))
    return t

def t_DATE(t):
    r'date: [0-9]+'
    t.value = str(t.value.replace(r"date ",''))
    return t

def t_CHAPTER(t): # important facts
    r'Important facts'


def t_TEXT(t):
    r'(.+| )+'
    t.value = str(t.value)
    return t

t_ignore=' \t\n\r'

def t_error(t):
    t.lexer.skip(1)
    return t

lexer = lex.lex()