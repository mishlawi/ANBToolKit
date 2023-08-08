import os
import inquirer
import inquirer
import shutil

from ... import dataControl
from . import FSGram

# *
# ** Controls the way the grammar can be organized and disposed
# * 

# grammar = """Story (H) -> title,author,date;
# Biography  -> name,birthday,birthplace,occupation,death;
# Foto  -> note,date;

# >UNIVERSE<

# Pessoa : H* , Facade, Bio?, Foto.
# Album : Foto*.
# Luquinhas : Banana*.

# H : h.
# Bio : b.
# Foto : p.
# """

    
terminal_width = shutil.get_terminal_size().columns
divider = "=" * terminal_width

def show_declarations():

    nonterminals, terminals = get_nonterminals_terminals_fsgram()
    entityuniverse = get_entities_fsgram()
    title = f"** ANB FSGram: **".center(terminal_width)
    print(divider)
    print(title)
    print(divider)
    print()
    

    for entity, (abv,speclist) in entityuniverse.items():

        if abv is not '':
            print(f"Entity: {entity} ({abv})")
        else:
            print(f"Entity: {entity}")
        for spec in speclist:
            print(f" * {spec}")
        print()
    
    # Printing terminals
    print(divider)
    
    print("DGU prefixs:")
    print(divider)
    
    for terminal, symbol in terminals.items():
        print(f" = {terminal} : {symbol}")
    
    print()

    print(divider)
    print("Entities Aggregators:")
    print(divider)
    for nonterminal, spec in nonterminals.items():
        text = ', '.join(f'{elem}' for elem in spec)
        print(f" = {nonterminal} : {text}.")

    print()
    

    

    
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


def add_aggregator(entitiesuniverse,terminals,nonterminals):
    
    show_declarations()
    print(divider)
    print() 
    added = input('''NOTE:\nTo add an aggregator, remember to use:\n
* Colon ":" to separate the aggregator name fromm the respective entities.
* Commas "," to separate entities.
* Period "." at the end of the definition.
\nFORMAT:\n<aggregator> : <entity> , <entity> , ... , <entity> .\n\nEXAMPLE:\n Person : Bio? , Foto .\n\n> ''')
    print(divider)

    if added == '':
        exit()
    if added[-1] != '.' or added.count(':') != 1 or added.count('.') != 1:
        print("Error in the aggregator definition.")
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
        verifyGrammar(entitiesuniverse,terminals,nonterminals)
        anbtk = dataControl.find_anb()
        with open(f"{anbtk}/fsgram.anb",'w') as anbtk:
            anbtk.write(full_fsgram_string(nonterminals,terminals,entitiesuniverse))



def entity_from_view_to_fsgram_dict(entity_name,abreviature,attributes):
    return {entity_name:(abreviature,attributes)}



def entity_view(entity):
    attributes = []
    abreviature = ''
    os.system('clear')
    while True:
        os.system('clear')
    
        if attributes != []:
            choices=['Add attribute', 'Edit attribute', 'Remove attribute','Add or edit alternative symbol', 'Save and exit', 'Delete entity and exit']
            
            if abreviature != '':
                choices=['Add attribute', 'Edit attribute', 'Remove attribute','Add or edit alternative symbol','Remove alternative symbol', 'Save and exit', 'Delete entity and exit']

            print(f"{entity} {abreviature} Attributes:\n")
            for elem in attributes:
                print("*",elem)
            print("\n")

            questions = [
                inquirer.List('selected_option',
                            message='Choose an option:',
                            choices = choices,
                ),
            ]
        else:
            print(f"{entity} has no attributes yet.\n")
            choices=['Add attribute','Add or edit alternative symbol', 'Delete entity and exit']
            if abreviature != '':
                choices=['Add attribute','Add or edit alternative symbol','Remove alternative symbol', 'Delete entity and exit']
            questions = [
                inquirer.List('selected_option',
                            message='Choose an option:',
                            choices=choices,
                ),
            ]
        answers = inquirer.prompt(questions)
        selected_option = answers['selected_option']

        if selected_option == 'Add attribute':
            while True:
                attribute_name = input("Attribute name:\n > ")
                if attribute_name == '':
                    print("No attribute name given.\n")
                elif not attribute_name.isalpha():
                    print("Only alphabetical characters are allowed.\n")
                elif attribute_name in attributes:
                    print("Attribute already exists.\n")
                else:
                    attributes.append(attribute_name)
                    break
        
        elif selected_option == 'Add or edit alternative symbol':
            print("The use of an alternative symbol aims to help to associate an entity with a more intuitive way to represent the an entity in the anb fsgram.\nFor example, if you were to write a alternative symbol for Biography you would write 'Bio'.")
            while True:
                alternative_symbol = input("Choose an alternative symbol (leave it empty to cancel and leave):\n > ")
                if alternative_symbol == '':
                    print("No alternative symbol given.\n")
                elif not alternative_symbol.isalpha():
                    print("Only alphabetical characters are allowed.\n")
                elif alternative_symbol in attributes:
                    print("Alternative symbol already exists.\n")
                elif alternative_symbol==entity or len(alternative_symbol)>len(entity):
                    print("Alternative symbol should be different and an abreviature of the entity.\nFor example: \nentity: Biography\nsymbol: Bio")
                else:
                    abreviature = alternative_symbol
                    break
        elif selected_option == 'Remove alternative symbol':
            abreviature = ''
            print("Alternative symbol removed.\n")
            
        elif selected_option == 'Remove attribute':
            attribute_list = [
                inquirer.List('selected_option',
                            message=f"{entity}'s attribute to be removed :",
                            choices= attributes,
                ),
            ]
            answers = inquirer.prompt(attribute_list)
            os.system('clear')
            selected_attribute = answers['selected_option']
            attributes.remove(selected_attribute)

 
        elif selected_option == 'Edit attribute':
            attribute_list = [
                inquirer.List('selected_option',
                            message=f"{entity}'s attribute to be edited :",
                            choices= attributes,
                ),
            ]
            answers = inquirer.prompt(attribute_list)
            os.system('clear')
            selected_attribute = answers['selected_option']
            index = attributes.index(selected_attribute)
            attributes[index] = input(f"Edit attribute '{selected_attribute}':\n > ")
            
        elif selected_option == 'Save and exit':
            print("To identify an pinpoint the compatible documents the DGU prefix has to be provided")
            prefix = ''
            while True:
                prefix = input("Please give a DGU prefix:\n > ")
                if prefix != '':
                    prefix = f"{prefix}."
                    break                
            new_addition = entity_from_view_to_fsgram_dict(entity,abreviature,attributes)
            nonterminals,terminals  = get_nonterminals_terminals_fsgram()
            terminals.update({entity:prefix})
            entityuniverse = get_entities_fsgram()
            entityuniverse.update(new_addition)
            anbtk = dataControl.find_anb()
            with open(f"{anbtk}/fsgram.anb",'w') as anbtk:
                anbtk.write(full_fsgram_string(nonterminals,terminals,entityuniverse))
            print("Entity saved and added to fsgram.\n")
            exit()


        elif selected_option == 'Delete entity and exit':
            exit()



def add_entity():
    show_declarations()
    entity_name = input("Entity name:\n > ")
    entity_view(entity_name)
         
    # inquirer module a while true that ineterruptly allows to ask to add attribute or to save and exit



def add_to_fsgram():

    nonterminals , terminals = get_nonterminals_terminals_fsgram()
    entitiesuniverse = get_entities_fsgram()
    view = choose_add_option()
    if view == 'Add aggregator':
        add_aggregator(entitiesuniverse, terminals,nonterminals)
    elif view== 'Add entity':
        add_entity()
       


def full_fsgram_string(nonterminals,terminals,entityuniverse):
    string = ''
    string += entities_universe_to_string(entityuniverse)
    string +='\n>UNIVERSE<\n'
    string += nonterminals_dict_to_string(nonterminals)
    string += terminals_to_string(terminals)
    return string

def entities_universe_to_string(entitiesuniverse):
    string = ''
    for aggregator,(abreviature,symbols) in entitiesuniverse.items():
    
        string +=f"{aggregator} "
        if abreviature is not None and abreviature!='':
            string += f"({abreviature})"
        string+=" -> "
        for elem in symbols[:-1]:
            string += f'{elem}, '
        string += f"{symbols[-1]} ;\n"
    
    return string
    


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

def terminals_to_string(terminals):
    string = ''
    for terminal,abv in terminals.items():
        string += f'{terminal} : {abv}\n'
    return string



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
    
    for terminal,abv in terminals.items():
        if terminal not in entityuniverse.values() and terminal not in entityuniverse.keys():
            print(f"ERROR: Terminal '{terminal}' pin-pointing to the abreviature {abv[:-1]} not recognized.")
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
    # interpreter(terminals,nonterminals)
    # DGUhand.get_symbols(universe,terminals)

    #universehand(universe)
    # show_declarations(terminals,nonterminals)
    #DGUhand.bigbang(universe,terminals)
    # gen_productions_file(nonterminals)
    



