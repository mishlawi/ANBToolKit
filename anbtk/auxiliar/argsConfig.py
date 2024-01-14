import readline
import argparse
import time
import os

from .. import dataControl


def a_tex2dgu():
    parser = argparse.ArgumentParser(
        prog='tex2dgu',
        description='Converts tex file to dgu.',
        epilog='')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', help="Takes 1 or more files defined by the user.", nargs='+')
    return parser.parse_args()


def a_dgubook():  
    parser = argparse.ArgumentParser(
        prog = 'dgubook',
        description = 'Aglomerates a number of .dgu files in a book - pdf format.',
        epilog = 'Results in a pdf file containing generic universal documents aglutinated.')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    group.add_argument('-t','--tree',help="Iterates through the entire tree of documents of the present directory.",action='store_true',default=False)
    group.add_argument('-p','--productions',help="Filter through defined productions",action='store_true')
    parser.add_argument('-md','--markdown',help="Returns a markdown file instead of a pdf (flag)",action="store_true")
    parser.add_argument('-all','--all',help="Returns all the files generated by pdflatex (flag)",action="store_true")
    parser.add_argument('-tf','--timeframe',help="Agregates a new section - Time Frame - to the pdf.\nWarning: This does not work if the desired output is markdown! (flag)",action="store_true")
    parser.add_argument('-o','--output',help="Selects an output folder",nargs=1)

    return parser.parse_args()


def a_notes():
    parser = argparse.ArgumentParser(
        prog = 'genNote',
        description = 'Generates a note for a specific Ancestors Notebook Element.',
        epilog = 'Composes a note to be filled by the user.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    return parser.parse_args()


def a_genStory():
    parser = argparse.ArgumentParser(
        prog = 'genStory',
        description = 'Generates a Story in the accepted format for Ancestors Notebook.',
        epilog = 'Composes a story to be filled by the user.')

    # Optional flags '-t', '-a', '-d'
    parser.add_argument('-t', '--title',required=True, help='Title of the story')
    parser.add_argument('-a', '--author', default="", help='Author of the story',nargs='+')
    parser.add_argument('-d', '--date', default=time.strftime('%Y-%m-%d'), help='the date of the story')
    parser.add_argument('-dgu',action='store_true',help='generates a Story dgu in Latex format')
    
    return parser.parse_args()


def a_genBio():
    parser = argparse.ArgumentParser(
        prog = 'genBio',
        description = 'Generates a Biography in the accepted format for Ancestors Notebook',
        epilog = 'Composes a Biography to be filled by the user.')

    parser.add_argument('-n', '--name',required=True, help='Name of the individual')
    parser.add_argument('-b', '--birth',default="", help='Date of Birth')
    parser.add_argument('-d', '--death',default="", help='Date of Death')
    parser.add_argument('-bp', '--birthplace',default="", help='BirthPlace')
    parser.add_argument('-o', '--occupation',default="", help="Individual's Job or Occupation")
    return parser.parse_args()


def a_dgu2texbook():
    parser = argparse.ArgumentParser(
        prog = 'dgu2texbook',
        description = 'Aglomerates a number of .dgu files in a latex book.',
        epilog = 'In a latex file with diferent latex files aglutinated in one')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    #parser.add_argument('-o','--out',help="output destination",nargs=1)
    group.add_argument('-t','--tree',help="Iterates through the entire tree of document of the present directory.",action='store_true',default=False)
    return parser.parse_args()


def a_image():
    parser = argparse.ArgumentParser(
        prog = 'dguImage',
        description = 'Generates DGU files for image files.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",action='store_true')
    group.add_argument('-t','--tree',help="Iterates through the entire tree of documents of the present directory.",action='store_true',default=False)
    return parser.parse_args()


def a_search():
    
    class CustomAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not 'ordered_args' in namespace:
                setattr(namespace, 'ordered_args', [])
            previous = namespace.ordered_args
            previous.append((self.dest, values))
            setattr(namespace, 'ordered_args', previous)

    parser = argparse.ArgumentParser(
        prog = 'anbsearch',
        description = 'Allows to query informations regarding the different familiar connections of the current ancestors notebook.',
        epilog = 'By chosing an individual A you can filter the different family members that have a specific (either direct or composed) connection - for visual purpouses only.')
    parser.add_argument('-s','--siblings',help="Individual's siblings.",nargs=0,action=CustomAction)
    parser.add_argument('-p','--parents',help="Individual's parents.",nargs=0,action=CustomAction)
    parser.add_argument('-ua','--unclesaunts',help="Individual's uncles and aunts.",nargs=0,action=CustomAction)
    parser.add_argument('-gp','--grandparents',help="Individual's grandparents.",nargs=0,action=CustomAction)
    parser.add_argument('-c','--children',help="Individual's children.",nargs=0,action=CustomAction)
    parser.add_argument('-i','--individual',help="Individual to be queried.",nargs="+",required=True)

    return parser.parse_args()



def a_cd():
    
    class CustomAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not 'ordered_args' in namespace:
                setattr(namespace, 'ordered_args', [])
            previous = namespace.ordered_args
            previous.append((self.dest, values))
            setattr(namespace, 'ordered_args', previous)

    parser = argparse.ArgumentParser(
        prog = 'anbcd',
        description = 'Allows to easily change directories inside the current Ancestors Notebook by taking into consideration the different familiar connections that exist.',
        epilog = 'From folder A you go to folder B by specifying the familiar relation between A and B')
    parser.add_argument('-s','--siblings',help="Individual's siblings.",nargs=0,action=CustomAction)
    parser.add_argument('-p','--parents',help="Individual's parents.",nargs=0,action=CustomAction)
    parser.add_argument('-ua','--unclesaunts',help="Individual's uncles and aunts.",nargs=0,action=CustomAction)
    parser.add_argument('-gp','--grandparents',help="Individual's grandparents.",nargs=0,action=CustomAction)
    parser.add_argument('-c','--children',help="Individual's children.",nargs=0,action=CustomAction)
    parser.add_argument('-i','--individual',help="Individual to be queried.",nargs="+",required=True)

    return parser.parse_args()



def a_ls():
    
    class CustomAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not 'ordered_args' in namespace:
                setattr(namespace, 'ordered_args', [])
            previous = namespace.ordered_args
            previous.append((self.dest, values))
            setattr(namespace, 'ordered_args', previous)

    parser = argparse.ArgumentParser(
        prog = 'anbcd',
        description = 'Allows to easily list directories and files inside individuals in the current Ancestors Notebook by taking into consideration the different familiar ties.',
        epilog = 'From folder A you go to folder B by specifying the familiar relation between A and B')
    parser.add_argument('-s','--siblings',help="Individual's siblings.",nargs=0,action=CustomAction)
    parser.add_argument('-p','--parents',help="Individual's parents.",nargs=0,action=CustomAction)
    parser.add_argument('-ua','--unclesaunts',help="Individual's uncles and aunts.",nargs=0,action=CustomAction)
    parser.add_argument('-gp','--grandparents',help="Individual's grandparents.",nargs=0,action=CustomAction)
    parser.add_argument('-c','--children',help="Individual's children.",nargs=0,action=CustomAction)
    parser.add_argument('-i','--individual',help="Individual to be queried.",nargs="+",required=True)
    
    return parser.parse_args()


def a_genFolders():
    parser = argparse.ArgumentParser(description="Ancestors Notebook generate folder structure")

    parser.add_argument('--seed', '-s', required=True, help="Path to the anbtemp file to be converted.", nargs=1)
    parser.add_argument('--source', '-src', help="Path to source fsgram file to generate ancestor's notebook entities")
    parser.add_argument('--family', '-fam', help="Name of the family to be created!", nargs=1)
    parser.add_argument('--filename', '-fn', help="Give a custom name to the ontology file. If not used, only a safe hidden file will be generated.", nargs='?')
    parser.add_argument('--out', '-o', help="Output the ontology file to a certain directory.", nargs='?')

    return parser.parse_args()

def a_anbinit():
    parser = argparse.ArgumentParser(description="Initializes a non structurized structurized Ancestors Notebook.")

    parser.add_argument('-s', '--source', help='Specify a source fsgram file to generate an ancestors notebook', nargs=1)


    return parser.parse_args()

def a_anbdgu():
    parser = argparse.ArgumentParser(description="Creates a default dgu or a entity based dgu")

    parser.add_argument('-e', '--entity', help='Specify an entity as described in your FSGram file or the default file', nargs=1)
    parser.add_argument('-f', '--filename', help='Name of the dgu', type=str, required=True, nargs=1)


    return parser.parse_args()


def a_anbsync():
    parser = argparse.ArgumentParser(description="Used to force the syncronization of the different elements of the Ancestors Notebook.")

    return parser.parse_args()


def input_with_completion(prompt):
    os.chdir(dataControl.get_root())
    folders = ['banana', 'salt']

    if prompt == "Enter -i: ":
        def completer(text, state):
            matches = [name for name in folders if name.startswith(text)]
            if state < len(matches):
                return matches[state]
            else:
                return None

        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")
        return input("")
    else:
        return input(prompt)
    


    