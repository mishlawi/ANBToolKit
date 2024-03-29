import ply.lex as lex
import ply.yacc as yacc

'''
grammar = γράμμα
'''



# Lexer tokens
tokens = (
    'POINT',
    'PLUS',
    'NEWLINE',
    'NAME',
    'DATE',
    'LP',
    'RP',
    'NDY',
    'UNK',
    'UND'
)


# Token regex
t_POINT = r'\.'
t_PLUS = r'\+'
t_LP = r'\('
t_RP = r'\)'
t_UND = r'\#\d+'                   # reads 'undeterminated'
t_DATE = r'\d{4}'
t_NDY = r'\-'                   # reads 'not dead yet'
t_UNK = r'\?'                   # reads 'unknown'
t_NEWLINE = r'\n'
t_NAME = r'\w+'
t_ignore = r' '




def p_family(p):
    '''
    Family : Couples 

    '''
    p[0] = p[1]



def p_couples(p):
    '''
    Couples : Couples Couple 
            | Couple 
    '''
    if len(p) == 3 :
        aux = p[1]
        if list(p[2].keys())[0] in list(aux.keys()):
            print(f"ERROR: {list(p[2].keys())[0]} is already instanciated as an existing couple.") 
            exit()
        aux.update(p[2])
        p[0] = aux
    else:
        p[0] = p[1]


def p_couple(p):
    '''
    Couple : Person PLUS Person NEWLINE Children NEWLINE
    '''

    p[0] = {f'{p[1]}+{p[3]}': p[5]}

def p_couple_error_plus(p):
    '''
    Couple : Person error Person NEWLINE Children NEWLINE
    '''
    print(f"\nMissing PLUS token between {p[1]} and {p[3]}")


def p_couple_error_newline_2(p):
    '''
    Couple : Person PLUS Person error Children NEWLINE
    '''
    print(f"\nMissing NEWLINE token between {p[3]} and {p[5]}")


def p_person(p):
    '''
    Person : Names Nickname Dates
           | Names Dates
           | UND
    '''
    if len(p) == 4:
        
        if p[1] in meta.keys():
            if meta[p[1]]['birthDate'] != p[3]['birthDate'] or meta[p[1]]['deathDate'] != p[3]['deathDate']:
                print(f"WARNING: {p[1]} is referenced in the document with 2 different dates.")
            if  meta[p[1]]['nickname'] != p[2]:
                print(f"WARNING: {p[1]} is referenced in the document with 2 different nicknames.")
        else:
            p[3].update({'nickname':p[2]})
            meta[p[1]] = p[3]
            meta[p[1]]['id'] = meta['total'] + 1

        p[0] = p[1]
    
    

    if len(p)==3:

        if p[1] in meta.keys():
            if meta[p[1]]['birthDate'] != p[2]['birthDate'] or meta[p[1]]['deathDate'] != p[2]['deathDate']:
                print(f"WARNING: {p[1]} is referenced in the document with 2 different dates.")
        else:

            p[2].update({'nickname':''})
            meta[p[1]] = p[2]
            meta[p[1]]['id'] = meta['total'] + 1
        p[0] = p[1] 

    if len(p)==2:
        
        meta[f"undiscovered_{p[1][1:]}"] = {'birthDate': '?', 'deathDate': '?','nickname':''}
        meta['undiscovered']+=1
        p[0] = f"undiscovered_{p[1][1:]}"
    
    
    meta['total'] += 1
  



def p_names(p):
    '''
    Names : Names NAME
          | NAME
          | empty
    '''
    if len(p) == 3 :
        p[0] = f"{p[1]} {p[2]}"
    else:
        p[0] = p[1]




def p_dates(p):
 
    # (xxxx xxxx)
    # (xxxx -)
    # (xxxx ?)
    # (?   - )
    # (? xxxx)
    # ?
     
    '''
    Dates : LP DATE DATE RP   
          | LP DATE NDY RP    
          | LP DATE UNK RP   
          | LP UNK NDY RP   
          | LP UNK DATE RP   
          | UNK
    '''
    lifespan = {'birthDate': '', 'deathDate': ''}
    if len(p) == 2:  
        lifespan['birthDate'] = lifespan['deathDate'] = '?'  
    else:
        lifespan['birthDate'] = p[2]
        lifespan['deathDate'] = p[3]
    p[0] = lifespan


def p_children(p):
    '''
    Children : Children Child
             | Child
             | empty

             
    '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        if p[1] != None :
            p[0] = [p[1]]
        else:
            p[0] = []




def p_child(p):
    
    '''
    Child : POINT Person NEWLINE
    '''
    p[0] = p[2]


def p_nickname(p):
    '''
    Nickname : LP Names RP
    '''
    p[0] = p[2]


    

def p_empty(p):
    '''
    empty :
    '''
    pass



import shutil



def p_error(p):
    terminal_width = shutil.get_terminal_size().columns
    divider = "=" * terminal_width
    error_title = "ERRORS".center(terminal_width)

    print(divider)
    print(error_title)
    print(divider)

    if p:
        error_message = f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token {p.type} ({p.value})"
        
        # Additional error handling for specific cases
        if p.type == 'PLUS':
            error_message += " - Invalid use of '+' token"
        elif p.type == 'DATE':
            error_message += " - Invalid date format"
        elif p.type == 'UND':
            error_message += " - Invalid use of 'undetermined' token"
        elif p.type == 'UNK':
            error_message += " - Invalid use of 'unknown' token"
        
        print(error_message)
        
        # Get the line where the error occurred
        lines = p.lexer.lexdata.split("\n")
        error_line = lines[p.lineno]
        
        print("in:", error_line)
        print()

    else:
        print("Syntax error: Unexpected end of input")



def t_error(t):
    print(f"Error: Illegal character '{t.value[0]}'")


#   yacc.yacc(errorlog=yacc.NullLogger()) // TO SURPRESS  WARNING MESSAGES
parser = yacc.yacc()
gramma_lexer = lex.lex()
#   lexer = lex.lex(debug=True) // TO DEBUG 
check_lexer = lex.lex()
meta = {'total': 0, 'undiscovered': 0}


def parsing(filename):
    global meta
    meta = {'total': 0, 'undiscovered': 0}


    with open(filename) as file:
        data = file.read()
    family_tree = parser.parse(data,lexer=gramma_lexer)

    terminal_width = shutil.get_terminal_size().columns
    divider = "=" * terminal_width
    if family_tree is None:
        print(divider)
        print("Error while processing the anbtemplate file.")
        print("Either bad input or no added elements.")
        exit(-1)
    
    return family_tree, meta


def check_parsing(data):
    global meta
    meta = {'total': 0, 'undiscovered': 0}


    family_tree = parser.parse(data,lexer=check_lexer)

    terminal_width = shutil.get_terminal_size().columns
    divider = "=" * terminal_width
    if family_tree is None:
        print(divider)
        print("Error while processing the anbtemplate file.")
        print("Either bad input or no added elements.")
        exit(-1)

    return family_tree, meta


#Get each token recognized by the lexer
    # gramma_lexer.input(data)
    # while True:
    #     token = gramma_lexer.token()
    #     if not token:
    #         break  # no more tokens
    #     print(token)

