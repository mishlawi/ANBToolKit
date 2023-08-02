import os
import inquirer
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


    elem = value[:-1] if value[-1] in ['*', '+', '?'] else value
    if elem in terminals.keys():
        if value[-1] in ['*', '+', '?']:
            buff.append((terminals[elem],value[-1]))
        else:
            buff.append((terminals[elem],''))
    elif elem in nonterminals.keys():
        for id in nonterminals[elem]:
            zoom(id,terminals,nonterminals,buff)



# def verifyGrammar(lista,grammar):
#     for producao in lista:
#         for id in producao:
#             if id[-1] in ['*', "+", '?']:
#                 id = id[:-1]

#             if id not in grammar.keys():
#                 print("Errors in the structure of the grammar.")
#                 exit()




# def universehand(universe):
#     galaxies = universe.split('\n')
    
#     for elem in galaxies:
    
#         if len(values:=re.split(r'\-\>',elem))>1:
#             entity = values[0]
#             atributes = values[1]
#             atributes = re.split(r'::',atributes)
#             # subclass = DGUhand.dgu_subclass(entity,atributes)

import shutil
    
terminal_width = shutil.get_terminal_size().columns
divider = "=" * terminal_width

def show_declarations():

    nonterminals, terminals = get_nonterminals_terminals_fsgram()
    # disposal = travessia(grammar,dirin,dirout,ignoredFiles)
    # genHtml(disposal,dirout,dirin)
    title = f"Loaded Declarations:".center(terminal_width)
    print(divider)
    print(title)
    print(divider)
    
    print("Entities Aggregators:")
    print("-"*terminal_width)
    for nonterminal, spec in nonterminals.items():
        text = ', '.join(f'{elem}' for elem in spec)
        print(f" - {nonterminal} : {text}")

    print(divider)
    

    # Printing terminals
    
    print("Entities:")
    print("-"*terminal_width)
    for terminal, symbol in terminals.items():
        print(f" - {terminal} : {symbol}")
    print(divider)
    
    # for nonterminal, spec in nonterminals.items():
    #     text = ''.join(f'{elem}, ' for elem in spec)
    #     text = text[:-1]
    #     print(f" - {nonterminal} : {text}")
    # print("\n")
    # for terminal, symbol in terminals.items(): 
    #     print(f" -> {terminal} : {symbol}")

    # print("\n")


def get_entities_fsgram():
    try:
        with open (f"{dataControl.find_anb()}/fsgram.anb","r") as productions_file:
            content = productions_file.read()
    except FileNotFoundError:
        print("✗ Fsgram file not found! Is this an AncestorsNotebook?")
        exit()

    entities,_,_,_ = FSGram.initializer(content)

    return entities


def get_nonterminals_terminals_fsgram():
    try:
        with open (f"{dataControl.find_anb()}/fsgram.anb","r") as productions_file:
            content = productions_file.read()
    except FileNotFoundError:
        print("✗ Fsgram file not found! Is this an AncestorsNotebook?")
        exit()

    grammar,universe,terminals,nonterminals = FSGram.initializer(content)


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
        return None
    elif selected_name == 'Leave':
        exit()
    
    return selected_name




def get_dgu_correspondence(all_files,terminals):

    dgu_correspondence = {
        terminal: [
            file
            for file in all_files
            if (os.path.basename(file)).startswith(terminals[terminal][:-1])
        ]
        for terminal in terminals
    }

    return dgu_correspondence


def convert_to_inquirer(nonterminals):
    values = []
    for key,value in nonterminals.items():
        terminals = ', '.join(str(item) for item in value)
        values.append(f"{key} : {terminals} ")
    return values


def travessia_specific():
    nonterminals, terminals = get_nonterminals_terminals_fsgram()

    root_folder = dataControl.get_root()
    files = retrieve_all_dgu_files(root_folder)
    dgu_correspondence = get_dgu_correspondence(files,terminals)
    inquirer_values = convert_to_inquirer(nonterminals)
    production = select_simple(inquirer_values,"Select a production to gather documents")
    production = production.split(':')[0].strip()
    
    documents = []
    for sym in nonterminals[production]:
        if sym[-1] in ["*","+","?"]:
            id = sym[:-1]
        else:
            id = sym
        
        if sym.endswith("*"):
            if len(dgu_correspondence[id])==0:
                continue
            else:
                documents.append((id,dgu_correspondence[id]))

        elif sym.endswith("+"):
            if  dgu_correspondence[id] != []:
                documents.append((id,dgu_correspondence[id]))
            else:
                print(f"✗ It is necessary to exist at least a {sym} file!")
                exit()

        elif sym.endswith("?"):
            
            if  dgu_correspondence[id] != []:
                preview = {}
                for elem in dgu_correspondence[id]:
                    preview[dataControl.relative_to_anbtk(elem)] = elem
                lista = list(preview.keys())
                lista.insert(0,'Ignore')
                lista.insert(0,'Leave')
                message = f"Chose a file or just ignore to satisfy the symbol\n {sym}"
                value = select_file_optional(lista,message)
                if value is not None:
                    documents.append((id,[preview[value]]))
                    
        else:
            
            if  dgu_correspondence[id] != []:
                if len(dgu_correspondence[id]) == 1:
    
                    documents.append((id,dgu_correspondence[id]))
                else:
                    preview = {}

                    for elem in dgu_correspondence[id]:
                        preview[dataControl.relative_to_anbtk(elem)] = elem
                    lista = list(preview.keys())
                    lista.insert(0,'Leave')
                    message = f"Chose a file to satisfy {sym}:\n"
                    value = select_file_optional(lista,message)
                    documents.append((id,[preview[value]]))
            else:
                print(f"✗ It is necessary to exist at least a {sym} file!")
                exit()

    return documents



# def travessia_geral():
#     nonterminals, terminals = read_fsgram_file()

#     root_folder = dataControl.get_root()
#     files = retrieve_all_dgu_files(root_folder)
#     dgu_correspondence = get_dgu_correspondence(files,terminals)

#     data = {}
#     for production, symbols in nonterminals.items():
#         data[production] = []
#         for sym in symbols:
#             if sym[-1] in ["*","+","?"]:
#                 id = sym[:-1]
#             else:
#                 id = sym
#             documents = data[production]
#             if sym.endswith("*"):
#                 documents.append((id,dgu_correspondence[id]))

#             elif sym.endswith("+"):
#                 if  dgu_correspondence[id] != []:
#                     documents.append((id,dgu_correspondence[id]))
#                 else:
#                     print(f"It is necessary to exist at least a {production} file!")
#                     exit()

#             elif sym.endswith("?"):
                
#                 if  dgu_correspondence[id] != []:
#                     preview = {}
#                     for elem in dgu_correspondence[id]:
#                         preview[elem] = dataControl.relative_to_anbtk(elem)
#                     lista = list(preview.values())
#                     lista.insert(0,'Ignore')
#                     lista.insert(0,'Leave')
#                     message = f"Chose a file or just ignore to satisfy\n {sym}"
#                     value = select_file_optional(lista,message)
#                     if value != '':
#                         documents.append((id,[value]))
#             else:
#                 if  dgu_correspondence[id] != []:
#                     if len(dgu_correspondence[id]) == 1:
#                         documents.append((id,value))
#                     else:
#                         preview = {}

#                         for elem in dgu_correspondence[id]:
#                             preview[elem] = dataControl.relative_to_anbtk(elem)
#                         lista = list(preview.values())
#                         lista.insert(0,'Leave')
#                         message = f"Chose a file to satisfy {sym}:\n"
#                         value = select_file_optional(lista,message)
#                         documents.append((id,[value]))
#                 else:
#                     print(f"It is necessary to exist at least a {production} file!")
#                     exit()
#     return data


def select_simple(symbols,message):

    print(message)
    questions = [
        inquirer.List('files',
                      choices=symbols,
                      ),
    ]
    answers = inquirer.prompt(questions)
    selected_name = answers['files']

    if selected_name == 'Leave':
        exit()
    
    return selected_name



def travessia_terminals():  
    _ , terminals = get_nonterminals_terminals_fsgram()
    root_folder = dataControl.get_root()
    files = retrieve_all_dgu_files(root_folder)
    dgu_correspondence = get_dgu_correspondence(files,terminals)
    selected = select_simple(terminals,f"Choose one type of document to gather.") 
    lista = [(selected,dgu_correspondence[selected])]
    return lista
    

from ...anbPE.blocks import edit_block

def get_fsgram():
    with open(dataControl.find_anb()+"/fsgram.anb") as f:
        fsgram = f.read()
    return fsgram

def choose_add_option():
    questions = [
        inquirer.List('selected_option',
                      message='Choose an option:',
                      choices=['Add entity', 'Add aggregator','Leave'],
                      ),
    ]

    answers = inquirer.prompt(questions)

    if answers['selected_option'] == 'Leave':
        exit()
    return answers['selected_option']


def add_aggregator(terminals,nonterminals):
    
    show_declarations() 
    added = input('''To add an aggregator, remember to use:\n
* Colon ":" to separate the aggregator name fromm the respective entities.
* Commas "," to separate entities.
* Period "." at the end of the definition.
\nFORMAT:\n<aggregator> : <entity> , <entity> , ... , <entity>.\n\nEXAMPLE:\n Person : Bio? , Foto .\n\n''')
    if added == '':
        exit()
    nonterminal = FSGram.parse_individual_production(added)
    if nonterminal == {} :
        print("Error in the aggregator development.")
        exit()
    else:
        agg = list(nonterminal.keys())[0]
        if agg in nonterminals.keys():
            print(f"{agg} is already defined as an aggregator. Give it another name.")
            exit()
        nonterminals.update(nonterminal)
        verifyGrammar(terminals,nonterminals)
        string = nonterminals_dict_to_string(nonterminals)

        # write_fsgram_file(nonterminals,terminals)
                        


def add_to_fsgram():
    x = FSGram.parse_grammar(grammar)
    print("?")
    a1,a2,a3,a4 = x
    print("1",a1)
    print("2",a2)
    print("3",a3)
    print("4",a4)
    # nonterminals , terminals = read_fsgram_file()
    # #show_declarations()
    # if choose_add_option() == 'Add aggregator':
    #     add_aggregator(terminals,nonterminals)
       



def nonterminals_dict_to_string(nonterminals):
    string = ''
    for production, terminals in nonterminals.items():
        string += f'{production} : '
        if terminals:  
            for elem in terminals[:-1]:
                string += f'{elem} , '
            string += f'{terminals[-1]} .'  
        string += '\n'
    

    return string


grammar = """Story (H) -> title,author,date;
Biography  -> name,birthday,birthplace,occupation,death;
Foto  -> note,date;

>UNIVERSE<

Pessoa : H* , Facade, Bio?, Foto.
Album : Foto*.
Luquinhas : Banana*.

H : h.
Bio : b.
Foto : p.


"""

def count_occurrences(lst, target):
    count_dict = {}
    for item in lst:
        count_dict[item] = count_dict.get(item, 0) + 1

    return count_dict.get(target, 0)

# add terminals and non terminals as argument
def verifyGrammar(entityuniverse,terminals,nonterminals):
    entityuniverse = get_entities_abbreviations(entityuniverse)
    print("*",entityuniverse)
    # terminals,nonterminals = read_fsgram_file()
    # _,_,_,terminals,nonterminals = FSGram.parse_grammar(grammar)
    for aggregator in nonterminals.keys():
       if count_occurrences(list(nonterminals.keys()),aggregator) > 1:
            print(f"ERROR: Repetition of aggregator '{aggregator}'.")
    for aggregator, productions in nonterminals.items():
        for symbol in productions:
            if count_occurrences(productions,symbol) > 1:
                print(f"ERROR: Symbol '{symbol}' repetition in the aggregator '{aggregator}' definition.")
                exit()
            if symbol[-1] in ["?","*","+"]:
                symbol = symbol[:-1]
                
            if symbol not in entityuniverse.keys() and symbol not in entityuniverse.values():
                print(f"ERROR: Symbol '{symbol}' in '{aggregator}' not recognized.")
                exit()
    
    print("Grammar verified successfully.")
            


def get_entities_abbreviations(entityuniverse):
    return {k:v[0] for k,v in entityuniverse.items()}


def get_entites_attributes(entityuniverse):
    return {k:v[1] for k,v in entityuniverse.items()}


def get_entity_name_by_abv(value,abv_entities):
    for key, val in abv_entities.items():
        if val == value:
            return key
    return None
def get_abbreviature_by_name(name,anb_entities):
    for key, val in anb_entities.items():
        if key == name:
            return val
    return None

def process_fsgram(entityuniverse,universe,terminals,nonterminals):

    """
    This function serves as an handler that pin-points all the information that needs to be processed to their corresponding functions.
    """
    verifyGrammar(entityuniverse,terminals,nonterminals)
    interpreter(terminals,nonterminals)
    DGUhand.get_symbols(universe,terminals)

    #universehand(universe)
    # show_declarations(terminals,nonterminals)
    #DGUhand.bigbang(universe,terminals)
    # gen_productions_file(nonterminals)
    



