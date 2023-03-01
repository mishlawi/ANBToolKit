import argparse
import time


################## tex2dgu ###################


def a_tex2dgu():
    parser = argparse.ArgumentParser(
        prog='dgubook',
        description='Converts tex file to dgu.',
        epilog='')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', help="Takes 1 or more files defined by the user.", nargs='+')
    return parser.parse_args()


################## dgubooks ##################


def a_dgubookmd():  
    parser = argparse.ArgumentParser(
        prog = 'dgubook',
        description = 'Aglomerates a number of .dgu files in a book - pdf format.',
        epilog = 'Results in a pdf file containing generic universal documents aglutinated.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    group.add_argument('-t','--tree',help="Iterates through the entire tree of documents of the present directory.",action='store_true',default=False)
    parser.add_argument('-md','--markdown',help="Returns a markdown file instead of a pdf",action="store_true")
    parser.add_argument('-o','--output',help="Selects an output folder",nargs=1) #! is not being used
    return parser.parse_args()


################### notes ####################


def a_notes():
    parser = argparse.ArgumentParser(
        prog = 'genNote',
        description = 'Generates a note for a specific Ancestors Notebook Element',
        epilog = 'Composes a note to be filled by the user.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    return parser.parse_args()



################## genStory ###################

def a_genStory():
    parser = argparse.ArgumentParser(
        prog = 'genStory',
        description = 'Generates a Story in the accepted format for Ancestors Notebook',
        epilog = 'Composes a story to be filled by the user.')

    # Optional flags '-t', '-a', '-d'
    parser.add_argument('-t', '--title',required=True, help='Title of the story')
    parser.add_argument('-a', '--author', default="", help='Author of the story',nargs='+')
    parser.add_argument('-d', '--date', default=time.strftime('%Y-%m-%d'), help='the date of the story')
    parser.add_argument('-dgu',action='store_true',help='generates a Story dgu in Latex format')
    
    return parser.parse_args()


################## genBio ##################

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