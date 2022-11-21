import ply.yacc as yacc
from notes.NotesTokens import tokens

# Anbnotes -> nota *
# nota -> ====Titulo
#           Conteudo
# conteudo -> Texto  | Genealogic expression
# Texto -> md


# RSNotes  ->  Notas
#
# Notas -> Notas Nota
#        | Nota
#        | Empty 

def p_RSNotesEmpty(p):
    "RSNotes : Notes"

def p_NotesAll(p):
    "Notes : Notes Nota"

def p_Notes(p):
    "Notes : Nota"

def p_NotesEmpty(p):
    "Notes : "

def p_Note(p):
    "Nota : Header Body Genealogy"

def p_Header(p):
    "Header : DELIMITER NOME TITULO AUTHOR DATE DELIMETER" 

def p_Body(p):
    "Body : ANCHOR CHAPTER Conteudo"

def p_Conteudo(p):
    "Conteudo : TEXTO"

# def p_Genealogy(p):
#     "Genealogy : "

def p_error(p):
    print("erro")
    print(p)



parser = yacc.yacc() 