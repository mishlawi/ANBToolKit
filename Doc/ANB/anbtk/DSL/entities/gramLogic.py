import os
import re
from . import FSGram
from ...dgu import DGUhand
from ... import dataControl

# *
# ** Controls the way the grammar can be organized and disposed
# * 

def interpreter(terminals,nonterminals):
    interpretation = {}
    for producao in nonterminals.keys():
        racional = []
        for id in nonterminals[producao]:
            collector = []
            zoom(id,terminals,nonterminals,collector)
            if id[-1] in ['*', '+', '?']:
                racional.append((collector,id[-1]))
            else:
                racional.append((collector,''))
        if producao in interpretation:
            aux = interpretation[producao]    
            interpretation[producao] = aux.append(racional)
        else:
            interpretation[producao] = racional
    return interpretation
    

def zoom(value, terminals, nonterminals,buff):
    # Disposal : P, Album* .
    # P : H* , Bio, Foto .
    # Album : Foto*.

    elem = value[:-1] if value[-1] in ['*', '+', '?'] else value
    if elem in terminals.keys():
        if value[-1] in ['*', '+', '?']:
            buff.append((terminals[elem],value[-1]))
        else:
            buff.append((terminals[elem],''))
    elif elem in nonterminals.keys():
        for id in nonterminals[elem]:
            zoom(id,terminals,nonterminals,buff)



def verifyGrammar(lista,grammar):
    for producao in lista:
        for id in producao:
            if id[-1] in ['*', "+", '?']:
                id = id[:-1]

            if id not in grammar.keys():
                print("Gramatica mal formulada")
                exit()



# instead of receiving the whole grammar, choose a production aka a Universal element
def travessia(grammar,dirIn,dirOut,ignoredFiles):
    
    # gets files
    ficheiros = []
    for file in os.listdir(dirIn):
        if os.path.isfile(os.path.join(dirIn, file)):
            ficheiros.append(file)
            print(file)

    # gets top production that defines the grammar
    top = list(grammar.values())[0]
    disposal = []
    
    # iterates through the productions that compose the top production
    
    for elem in top:
        
        # verifies types if productions have different elements
        
        for id in elem:
                  
            if id[-1]=='*': # 0 or plus elements
                id = id[:-1]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                
                for elem in ficheiros:
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:    
                        disposal.append(elem)
            
            elif id[-1]=='+': # 1 or plus elements
                id = id[:-1]
                count = 0
                regex = grammar[id]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                
                for elem in ficheiros:
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:
                        disposal.append(elem)
                        count+=1

                if count==0: 
                    print("não existem um ou mais ficheiros do tipo enunciado na gramática")
                    exit()
            
            elif id[-1]=='?': # optional
                id = id[:-1]
                regex = grammar[id]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                count = 0
                
                
                for elem in ficheiros:
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:
                        if count == 0:          # can only accept 1 max 
                            disposal.append(elem)
                        if count > 0:
                            print("existem ficheiros a mais")
                            exit()
                        count += 1
                                
        
            else: # 1 one element only
                count=0
                regex = grammar[id]
                print(grammar[id][0])
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                
                for elem in ficheiros:
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:
                        
                        if count != 1:
                            disposal.append(elem)
                            count+=1
                        
                        if count > 1:
                            print("existem ficheiros a mais")
                            exit()


                        elif count < 1:
                            print("existem ficheiros a menos")
                            exit()
    return disposal
    

    
def show_declarations(terminals,nonterminals):
    # disposal = travessia(grammar,dirin,dirout,ignoredFiles)
    # genHtml(disposal,dirout,dirin)
    print("\n\n")
    print("-- Declarations --\n")
    print(nonterminals)
    for nonterminal, spec in nonterminals.items():
        text = ''.join(f'{elem}, ' for elem in spec)
        text = text[:-1]
        print(f" - {nonterminal} : {text}")
    print("\n")
    for terminal, symbol in terminals.items(): 
        print(f" -> {terminal} : {symbol}")

    print("\n")



def universehand(universe):
    galaxies = universe.split('\n')
    
    for elem in galaxies:
    
        if len(values:=re.split(r'\-\>',elem))>1:
            entity = values[0]
            atributes = values[1]
            atributes = re.split(r'::',atributes)
            # subclass = DGUhand.dgu_subclass(entity,atributes)


def read_fsgram_file():
    try:
        with open (f"{dataControl.find_anb()}/fsgram.anb","r") as productions_file:
            content = productions_file.read()
    except FileNotFoundError:
        print("There isn't a fsgram file in this AncestorsNotebook.")
        exit()

    top,grammar,universe,terminals,nonterminals = FSGram.initializer(content)

    print(nonterminals)
    return nonterminals,terminals

def retrieve_all_dgu_files(root_folder):
    files = []


    for root, dirs, _ in os.walk(root_folder, followlinks=False):
        for folder in dirs:
            if not folder.startswith("."):
                folder_path = os.path.join(root, folder)
                if not os.path.islink(folder_path):
                    for file in os.listdir(folder_path):      
                        file_path = os.path.join(folder_path, file)
                        if not os.path.islink(file_path) and os.path.isfile(file_path) and file_path.endswith(".dgu"):
                            files.append(file_path) 
    return files

import inquirer

def select_file_optional(files,message):
    folder_names = files

    print(message)
    questions = [
        inquirer.List('files',
                      choices=folder_names,
                      ),
    ]
    answers = inquirer.prompt(questions)
    selected_name = answers['files']

    if selected_name == "Ignore":
        return ''
    
    return selected_name


"""
defaultFsgram = Pessoa : H* , Bio?, Foto.
Album : Foto*.

H : h.
Bio : b.
Foto : p.

UNIVERSE

Story -> title,author,date
Biography -> name,birthday,birthplace,occupation,death
Foto -> note,date

IGNORE
.py 
.out
.fsgram
"""

def travessia_new():
    nonterminals, terminals = read_fsgram_file()

    root_folder = dataControl.get_root()
    files = retrieve_all_dgu_files(root_folder)
    dgu_correspondence = {
        terminal: [
            file
            for file in files
            if (os.path.basename(file)).startswith(terminals[terminal][:-1])
        ]
        for terminal in terminals
    }

    data = {}
    for production, symbols in nonterminals.items():
        data[production] = []
        for sym in symbols:
            if sym[-1] in ["*","+","?"]:
                id = sym[:-1]
            else:
                id = sym
            documents = data[production]
            if sym.endswith("*"):
                documents.append((id,dgu_correspondence[id]))

            elif sym.endswith("+"):
                if  dgu_correspondence[id] != []:
                    documents.append((id,dgu_correspondence[id]))
                else:
                    print(f"It is necessary to exist at least a {production} file!")
                    exit()

            elif sym.endswith("?"):
                
                if  dgu_correspondence[id] != []:
                    preview = {}
                    for elem in dgu_correspondence[id]:
                        preview[elem] = dataControl.relative_to_anbtk(elem)
                    lista = list(preview.values())
                    lista.insert(0,'Ignore')
                    message = f"Chose a file or just ignore to satisfy\n {sym}"
                    value = select_file_optional(lista,message)
                    if value != '':
                        documents.append((id,value))
            else:
                if  dgu_correspondence[id] != []:
                    preview = {}
                    for elem in dgu_correspondence[id]:
                        preview[elem] = dataControl.relative_to_anbtk(elem)
                    lista = list(preview.values())
                    message = f"Chose a file to satisfy {sym}:\n"
                    value = select_file_optional(lista,message)
                    documents.append((id,value))
                else:
                    print(f"It is necessary to exist at least a {production} file!")
                    exit()
    return data


def topdf(data,production):
    files = data[production]
    for symb in files:
        print(symb)

def gen_productions_file(nonterminals):
    string = ''
    for production, terminals in nonterminals.items():
        string += f'{production} : '
        if terminals:  
            for elem in terminals[:-1]:
                string += f'{elem} , '
            string += f'{terminals[-1]}'  
        string += '\n'

    with open(r'productions.txt', 'w') as file:
        file.write(string)


def process_fsgram(top,grammar,universe,terminals,nonterminals):
    """
    This function serves as an handler that pin-points all the information that needs to be processed to their corresponding functions.
    """
    verifyGrammar(top,grammar)
    interpreter(terminals,nonterminals)
    #universehand(universe)
    show_declarations(terminals,nonterminals)
    DGUhand.bigbang(universe,terminals)
    gen_productions_file(nonterminals)
    



