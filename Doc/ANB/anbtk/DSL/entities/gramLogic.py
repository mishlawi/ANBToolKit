import os
import inquirer
import shutil

from ... import dataControl
from . import FSGram
from ...ontology import ousia
from ... import genealogia

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
    """
    Display the declarations, nonterminals, terminals, entity universe, and other information related to the ANB FSGram.

    This function retrieves nonterminals, terminals, and entity universe information using the functions
    `get_nonterminals_terminals_fsgram()` and `get_entities_fsgram()`. It then prints the retrieved data in a
    formatted manner, displaying entities, their abbreviations, specifications, DGU prefixes, and entity aggregators.

    Args:
        None

    Returns:
        None
    """

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
    """
    Retrieve entity information from the FSGram file in the AncestorsNotebook.

    This function reads the 'fsgram.anb' file located in the AncestorsNotebook folder .anbtk using the path obtained from
    It then initializes the FSGram using the file's content and extracts the entities names, attributes and abreviation.

    Returns:
        dict: A dictionary containing entity information.
    """
    try:
        with open (f"{dataControl.find_anb()}/fsgram.anb","r") as productions_file:
            content = productions_file.read()
    except FileNotFoundError:
        print("✗ Fsgram file not found! Is this an AncestorsNotebook?")
        exit()

    entities,_,_,_ = FSGram.initializer(content)

    return entities


def get_nonterminals_terminals_fsgram():
    """
    Retrieve nonterminals and terminals information from the FSGram file in the AncestorsNotebook.

    This function reads the 'fsgram.anb' file located in the AncestorsNotebook using the path obtained from
    `dataControl.find_anb()`. It then initializes the FSGram using the file's content and extracts nonterminals and
    terminals information.

    Returns:
        tuple: A tuple containing two dictionaries. The first dictionary contains nonterminal information, and the
               second dictionary contains terminal information.
    """
    try:
        with open (f"{dataControl.find_anb()}/fsgram.anb","r") as productions_file:
            content = productions_file.read()
    except FileNotFoundError:
        print("✗ Fsgram file not found! Is this an AncestorsNotebook?")
        exit()

    _,_,terminals,nonterminals = FSGram.initializer(content)


    return nonterminals,terminals

 

def retrieve_all_dgu_files(root_folder):
    """
    Retrieve paths of all .dgu files within the specified root folder.

    This function walks through the directory structure starting from the given root folder and collects paths of all
    files with a '.dgu' extension. It excludes hidden folders and symlinks.

    Args:
        root_folder (str): The root folder from which to start the search.

    Returns:
        list: A list containing paths to all .dgu files found within the specified root folder and its subdirectories.
    """
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
    """
    Prompt the user to select a file from a list, with optional "Ignore" and "Leave" choices.
    This function takes a list of files and displays it to the user, allowing him to choose one. It uses the 'inquirer' library to present
    the list of files to the user for selection.
    Args:
        files (list): A list of file names to choose from.
        message (str): The message to display before presenting the file choices.

    Returns:
        str or None: The selected file name from the list. Returns `None` if the user chooses to ignore, and exits the
        program if the user chooses to leave.
    """
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
    """
    Generate a correspondence between terminals and corresponding .dgu files.

    This function creates a dictionary that associates each terminal with a list of .dgu files that have filenames
    starting with the corresponding terminal abbreviation. It iterates through the provided list of terminals and uses
    the dgu prefix stored in the terminals dictionary to match .dgu filenames.

    Args:
        all_files (list): A list of paths to .dgu files.
        terminals (dict): A dictionary containing terminal abbreviations as keys and corresponding symbols as values.

    Returns:
        dict: A dictionary where keys are terminals and values are lists of corresponding .dgu files.
    """

    dgu_correspondence = {
        convertid(terminal): [
            file
            for file in all_files
            if (os.path.basename(file)).startswith(terminals[terminal][:-1])
        ]
        for terminal in terminals
    }

    return dgu_correspondence


def convert_to_inquirer(nonterminals):
    """
    Convert nonterminals dictionary into a format suitable for the 'inquirer' library.

    This function takes a dictionary of nonterminals and their corresponding values, and converts it into a list of
    formatted strings suitable for use with the 'inquirer' library. Each nonterminal and its associated values are
    formatted as a single string in the form "key : value1, value2, ...".

    Args:
        nonterminals (dict): A dictionary containing nonterminal keys and corresponding values.

    Returns:
        list: A list of formatted strings representing nonterminals and their associated values.
    """
    values = []
    for key,value in nonterminals.items():
        terminals = ', '.join(str(item) for item in value)
        values.append(f"{key} : {terminals} ")
    return values



def convertid(id):
    entity_universe = get_entities_fsgram()
    ent_abv = get_entities_abbreviations(entity_universe)
    if id in ent_abv.values():
        for key,value in ent_abv.items():
            if value == id:
                id = key
                return id
    return id    

def travessia_specific():
    """
    Perform a specific traversal and document gathering based on selected productions.

    This function orchestrates the process of traversing specific productions, gathering documents according to the
    specified symbols, and returning the collected documents. It interacts with user choices using the 'inquirer' library
    and makes use of various helper functions to achieve its purpose.

    Returns:
        list: A list of tuples containing symbols and corresponding lists of document paths.
    """
    nonterminals, terminals = get_nonterminals_terminals_fsgram()
    
    root_folder = dataControl.get_root()
    files = retrieve_all_dgu_files(root_folder)
    dgu_correspondence = get_dgu_correspondence(files,terminals)
    inquirer_values = convert_to_inquirer(nonterminals)
    production = view_select_aggregators_or_symbols(inquirer_values,"Select a production to gather documents")
    production = production.split(':')[0].strip()
    
    documents = []
    for sym in nonterminals[production]:
        if sym[-1] in ["*","+","?"]:
            id = sym[:-1]
        else:
            id = sym
        id = convertid(id)
        print(id)
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


def view_select_aggregators_or_symbols(aggregators,message):
    """
    Prompt the user to select a symbol (either an aggregator or an entity) from a list with a "Leave" choice.

    This function takes a list of aggregators and displays a user-friendly message. It uses the 'inquirer' library to present
    the list of aggregators to the user for selection. The function also includes the option "Leave," which allows the user
    to exit the program.

    Args:
        aggregators (list): A list of aggregators to choose from.
        message (str): The message to display before presenting the symbol choices.

    Returns:
        str: The selected symbol from the list. Returns "Leave" if the user chooses to exit the program.
    """
    
    aggregators.append('Leave')
    print(message)
    questions = [
        inquirer.List('files',
                      choices=aggregators,
                      ),
    ]
    answers = inquirer.prompt(questions)
    selected_name = answers['files']

    if selected_name == 'Leave':
        exit()
    
    return selected_name



def travessia_terminals():
    """
    Perform a traversal and document gathering based on selected terminal symbols.

    This function prompts the user to choose a type of document from a list of terminal symbols. It then retrieves
    .dgu files corresponding to the selected terminal and returns a list containing the selected terminal and its
    corresponding .dgu files.

    Returns:
        list: A list containing a tuple with the selected terminal and its corresponding .dgu files.
    """  
    _ , terminals = get_nonterminals_terminals_fsgram()
    root_folder = dataControl.get_root()
    files = retrieve_all_dgu_files(root_folder)
    dgu_correspondence = get_dgu_correspondence(files,terminals)
    selected = view_select_aggregators_or_symbols(terminals,f"Choose one type of document to gather.") 
    lista = [(selected,dgu_correspondence[selected])]
    return lista
    


def get_fsgram():
    """
    Read and retrieve the content of the 'fsgram.anb' file.

    This function reads the content of the 'fsgram.anb' file located in the AncestorsNotebook using the path obtained
    from `dataControl.find_anb()`.

    Returns:
        str: The content of the 'fsgram.anb' file.
    """

    with open(dataControl.find_anb()+"/fsgram.anb") as f:
        fsgram = f.read()
    return fsgram

def choose_add_option():
    """
    Prompt the user to choose an option for adding entities or aggregators.

    This function presents the user with a list of options, including 'Add entity', 'Add aggregator', and 'Leave'. It
    uses the 'inquirer' library to capture the user's selection.

    Returns:
        str: The selected option. Returns "Leave" if the user chooses to exit the program.
    """
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
    """
    Add an aggregator to the FSGram grammar based on user input.

    This function displays the existing declarations using `show_declarations()` and prompts the user to input an
    aggregator definition. The definition should follow the format:
    "<aggregator> : <entity> , <entity> , ... , <entity> ."

    Args:
        entitiesuniverse (dict): A dictionary containing entity information.
        terminals (dict): A dictionary containing terminal information.
        nonterminals (dict): A dictionary containing nonterminal information.

    Returns:
        None
    """
    
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
        print(f"{agg} successfully added as an new aggregator.\nUse dgubook -p to select it and use it.")



def entity_from_view_to_fsgram_dict(entity_name,abreviature,attributes):
    """
    This function takes entity information in the form of entity name, abbreviation, and attributes, and converts it
    into a dictionary format suitable for use in the FSGram dictionary.

    Args:
        entity_name (str): The name of the entity.
        abreviature (str): The abbreviation of the entity.
        attributes (list): A list of attributes associated with the entity.

    Returns:
        dict: A dictionary containing the entity name as the key and a tuple of abbreviation and attributes as the value.
    """
    return {entity_name:(abreviature,attributes)}



def entity_view(entity):
    """
    Display an interactive view for managing entity attributes and alternative symbols.

    This function provides the interactive menu and underlying logic for managing an entity's attributes and alternative symbols. Users can
    add, edit, or remove attributes, add or edit an alternative symbol, and save the entity to the FSGram.

    Args:
        entity (str): The name of the entity.

    Returns:
        None
    """
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
            print("The use of an alternative symbol aims to help to associate an entity with a more intuitive way to represent the entity in the anb fsgram.\nFor example, if you were to write a alternative symbol for Biography you would write 'Bio'.")
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
            while True:
                edited_attribute = input(f"Edit attribute '{selected_attribute}':\n > ")
                if edited_attribute == '':
                    print("No alternative symbol given.\n")
                elif not edited_attribute.isalpha():
                    print("Only alphabetical characters are allowed.\n")
                else:
                    attributes[index] = edited_attribute
                    break
           
            
        elif selected_option == 'Save and exit':
            print("To identify and pinpoint the compatible documents the DGU prefix has to be provided.\nFor example the prefix for Biography is b, so a recognized file would be 'b[1]-document_name.dgu'\n")
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

            g = genealogia.read_onto_file(f"{anbtk}/anbsafeonto.rdf")
            ousia.new_dgu_object(entity,attributes,g)
            genealogia.gen_onto_file(g, dataControl.find_anb() + '/anbsafeonto')

            with open(f"{anbtk}/fsgram.anb",'w') as anbtk:
                anbtk.write(full_fsgram_string(nonterminals,terminals,entityuniverse))
             
            
            print("Entity saved and added to fsgram.\n")
            exit()


        elif selected_option == 'Delete entity and exit':
            exit()



def add_entity():
    """
    Start the process of adding a new entity to the FSGram.

    This function displays existing aggregators, entities and terminals and prompts the user to input the name of the new entity. It then
    initiates the entity view using the provided entity name to manage attributes and alternative symbols.

    Returns:
        None
    """
    show_declarations()
    entity_name = input("Entity name:\n > ")
    entity_view(entity_name)
         



def add_to_fsgram():
    """
    Start the process of adding new entities or aggregators to the FSGram.

    This function retrieves existing nonterminals, terminals, and entity information using helper functions, and prompts
    the user to choose between adding an aggregator or an entity. It then directs the user to the respective function for
    adding the selected option.

    Returns:
        None
    """

    nonterminals , terminals = get_nonterminals_terminals_fsgram()
    entitiesuniverse = get_entities_fsgram()
    view = choose_add_option()
    if view == 'Add aggregator':
        add_aggregator(entitiesuniverse, terminals,nonterminals)
    elif view== 'Add entity':
        add_entity()
       


def full_fsgram_string(nonterminals,terminals,entityuniverse):
    """
    Generate a complete FSGram string based on provided nonterminals, terminals, and entity information.

    This function takes dictionaries containing nonterminals, terminals, and entity information, and generates a
    formatted FSGram string combining these elements.

    Args:
        nonterminals (dict): A dictionary containing nonterminal information.
        terminals (dict): A dictionary containing terminal information.
        entityuniverse (dict): A dictionary containing entity information.

    Returns:
        str: The complete FSGram string.
    """
    string = ''
    string += entities_universe_to_string(entityuniverse)
    string +='\n>UNIVERSE<\n'
    string += nonterminals_dict_to_string(nonterminals)
    string += terminals_to_string(terminals)
    return string

def entities_universe_to_string(entitiesuniverse):
    """
    Convert entity universe information to a formatted string.

    This function takes a dictionary containing entity universe information and converts it into a formatted string
    representation, ready to be included in the FSGram.

    Args:
        entitiesuniverse (dict): A dictionary containing entity universe information.

    Returns:
        str: The formatted string representation of the entity universe.
    """
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
    """
    Convert nonterminals dictionary to a formatted string.

    This function takes a dictionary containing nonterminal information and converts it into a formatted string
    representation, ready to be included in the FSGram.

    Args:
        nonterminals (dict): A dictionary containing nonterminal information.

    Returns:
        str: The formatted string representation of the nonterminals.
    """
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
    """
    Convert terminals dictionary to a formatted string.

    This function takes a dictionary containing terminal information and converts it into a formatted string
    representation, ready to be included in the FSGram.

    Args:
        terminals (dict): A dictionary containing terminal information.

    Returns:
        str: The formatted string representation of the terminals.
    """
    string = ''
    for terminal,abv in terminals.items():
        string += f'{terminal} : {abv}\n'
    return string



def count_occurrences(lst, target):
    """
    Count occurrences of a specific element in a list.

    This function counts the number of times a specific element appears in a list and returns the count.

    Args:
        lst (list): The list to search for occurrences.
        target: The element to count occurrences of.

    Returns:
        int: The number of occurrences of the target element in the list.
    """
    count_dict = {}
    for item in lst:
        count_dict[item] = count_dict.get(item, 0) + 1

    return count_dict.get(target, 0)

# add terminals and non terminals as argument
def verifyGrammar(entityuniverse,terminals,nonterminals):
    """
    Verify the consistency of the grammar based on provided entity universe, terminals, and nonterminals.

    This function checks the consistency of the grammar by verifying aggregators, symbols, and their presence in the
    entity and terminals correspondent dictionaries.

    Args:
        entityuniverse (dict): A dictionary containing entity universe information.
        terminals (dict): A dictionary containing terminal information.
        nonterminals (dict): A dictionary containing nonterminal information.

    Returns:
        None
    """
    entityuniverse = get_entities_abbreviations(entityuniverse)
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
    """
    Extract entity abbreviations from the entity universe dictionary.

    This function takes a dictionary containing entity universe information and extracts entity abbreviations.

    Args:
        entityuniverse (dict): A dictionary containing entity universe information.

    Returns:
        dict: A dictionary containing entity names as keys and their corresponding abbreviations as values.
    """
    return {k:v[0] for k,v in entityuniverse.items()}


def get_entites_attributes(entityuniverse):
    """
    Extract entity attributes from the entity universe dictionary.

    This function takes a dictionary containing entity universe information and extracts entity attributes.

    Args:
        entityuniverse (dict): A dictionary containing entity universe information.

    Returns:
        dict: A dictionary containing entity names as keys and their corresponding attributes as values.
    """
    return {k:v[1] for k,v in entityuniverse.items()}


def get_entity_name_by_abv(value,abv_entities):
    """
    Retrieve the entity name using its abbreviation.

    This function searches for an entity name based on its abbreviation.

    Args:
        value: The abbreviation of the entity.
        abv_entities (dict): A dictionary containing entity names as keys and their abbreviations as values.

    Returns:
        str or None: The corresponding entity name. Returns None if no match is found.
    """

    for key, val in abv_entities.items():
        if val == value:
            return key
    return None


def get_abbreviature_by_name(name,anb_entities):
    """
    Retrieve the abbreviation using the entity name.

    This function searches for an abbreviation based on the entity name.

    Args:
        name (str): The name of the entity.
        anb_entities (dict): A dictionary containing entity names as keys and their abbreviations as values.

    Returns:
        str or None: The corresponding abbreviation. Returns None if no match is found.
    """
    for key, val in anb_entities.items():
        if key == name:
            return val
    return None

def process_fsgram(entityuniverse,universe,terminals,nonterminals):
    """
    Process FSGram information for verification and handling.

    This function acts as a handler, directing the provided FSGram information to the relevant functions for verification
    and further processing.

    Args:
        entityuniverse (dict): A dictionary containing entity universe information.
        universe: The 'universe' object.
        terminals (dict): A dictionary containing terminal information.
        nonterminals (dict): A dictionary containing nonterminal information.

    Returns:
        None
    """
    verifyGrammar(entityuniverse,terminals,nonterminals)
    # interpreter(terminals,nonterminals)
    # DGUhand.get_symbols(universe,terminals)

    #universehand(universe)
    # show_declarations(terminals,nonterminals)
    #DGUhand.bigbang(universe,terminals)
    # gen_productions_file(nonterminals)
    



