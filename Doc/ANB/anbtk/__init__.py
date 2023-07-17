""" ANB toolkit - a module for sorting and managing documents and material from different family branches"""

__version__ = "0.0.2"

import os
import shutil
import argparse


from . import genealogia
from . import dataControl
from . import controlsystem
from .anbPE import projectionEditor
from .anbPE import blocks
from .filters import filters

from .actions import latex
from .actions import book
from .actions import gen_dgus

from .auxiliar import dgu_helper
from .dgu import dguObject as dgu



##############################################################################################################
##############################################################################################################
##############################################    NOTES    ###################################################
##############################################################################################################
##############################################################################################################

#? DUVIDAS
# * error handling nas gramáticas
# * usar path para a ontologia como URI


#*TODO

# ! FIX TEX2DGU regarding the UTF8
# * maybe add specs to dont do anything if there are no differences in the sync command
#!  update the onto file so that new entities can be added
# * anbvc has the absolute path 
# * show commands : show entities, etc
# * erro de ja estar numa pasta  já inicializada como anb, quando na realidade apenas se está um nivel acima de uma pasta inicializada
# * tex2dgu puts author false
# * maybe, moving a file updates its path?
# * refactor dgubook individual and generic functions
# * ontology for dgus and ontology for relations
# * be careful with new couples for the same individual (ex spouse)
# * revise the command for dgu generation for generic dgus
# * gedcom
# * add two ontologies
# * gen filesystem structure through ontology
# * template html
# * verificar a existencia de erros 1o, e só depois executar efetivamente as coisas, senao pastas sao geradas mesmo quando é dado um mau input
# * "anb individuo" e aparecerem elementos relativos ao individuo 
# * add comments for the seed file and entities file
# * testar projection editor (check individual function annotations)
# * use default editor

# ! individual dgubook not working
# ! todo : gedcom; show family tree
# ! data updates and nickname updates should be presented in the anbtemplate when two references exist -> if i add a nickname to jose in the child position, it should appear in the parent position 

#? Done, but re check:
# * i want it so that story and bio (and others) are default formats but the users can create their ones x
# * auto sync when creating dgus x

##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################


#! readline bib para completação

def dgu2texbook():
    latex.dgu2texbook()


#* dont forget to add the path if needed in the future
def tex2dgu(dirout=""):
    latex.tex2dgu(dirout)
    

def dgubook():
    book.dgubook()
    

def genDguImage():
    gen_dgus.genDguImage()


# usage : -title -author? -date -dgu
def genStory():
    gen_dgus.genStory()


def genBio():
    gen_dgus.genBio()


def genDgu(title, attributes, nameofthefile, dir):
    gen_dgus.genDgu(title,attributes,nameofthefile,dir)

#check if .anbtk exists
def anbedit():
    projectionEditor.action()

def createCouple():
    projectionEditor.add_couple()

def query():
    filters.anb_search()

def folder_cd():
    filters.anb_cd()

def folder_ls():
    filters.anb_ls()

def show_entities():
    pass

def get_about():
    filters.search_by_about_files()

############################## .anb ################################


def anb():
    
    parser = argparse.ArgumentParser(prog='ancestors notebook')
    subparsers = parser.add_subparsers(dest='subcommand',required=True,help='List of subcommands accepted')
    init_parser = subparsers.add_parser('init')
    init_parser.add_argument('-s','--source',help='Specify a source fsgram file to generate an ancestors notebook', nargs=1)
    dguCommands_parser = subparsers.add_parser('dgu',help='Creates a default dgu or a entity based dgu')
    dguCommands_parser.add_argument('-e','--entity',help='Specify an entity as described in your FSGram file or the default file',nargs=1)
    dguCommands_parser.add_argument('-f','--filename',help='Name of the dgu',type=str,dest='filename',required=True,nargs=1)

    genSync = subparsers.add_parser('sync')

    genFolderStructure = subparsers.add_parser('genFolders',help="gen folder structure from seed file.")
    genFolderStructure.add_argument('--seed','-s',required=True, help="path to seed file to be converted.",nargs=1)
    genFolderStructure.add_argument('--source','-src',help = "path to source fsgram file to generat ancestors notebook entities")
    genFolderStructure.add_argument('--family','-fam',help = "name of the family to be created!",nargs=1)
    genFolderStructure.add_argument('--filename','-fn', help= "give a custom name to the ontology file. If not used, only a safe hidden file will be generated.",nargs='?')
    genFolderStructure.add_argument('--out','-o',help="output the ontology file to a certain directory.",nargs='?')

    args = parser.parse_args()
    currentdir = os.getcwd()

    if args.subcommand == 'init':
    
        if args.source:
            file = args.source[0]
            dataControl.initanb(os.path.abspath(file))
    
        else:
            dataControl.initanb()
    
    elif args.subcommand == 'dgu':
        if dataControl.search_anbtk():

            if args.entity:            
                with open('universe.dgu') as universe:
                    entities = dgu_helper.parse_text(universe.read())
                    if args.entity[0] in entities.keys():
                        genDgu(args.entity[0], entities[args.entity[0]], args.filename[0],currentdir)
                    else:
                        print("✗ No entity exists with that name")
            if not args.entity:
                os.chdir(currentdir)
                empty_dgu = dgu.DGU()
                with open(args.filename[0]+'.dgu',"w") as f:
                    dgu_helper.dguheadercomposer(empty_dgu,f)

        else:
            print("✗ You need to initialize an ancestors notebook")


    elif args.subcommand == 'genFolders':
        print(" ---  Ancestors Notebook processing status  --- \n")
        
        if args.source:
            fsgram = args.source[0]
        else:
            fsgram = ""
        

        if args.seed:

            seed = args.seed[0]
        
            if not os.path.exists(seed):
                print("✗ The specified file does not exist.")
                exit(1)
        
            else:
                if args.family:
                    family = args.family[0]
                else:
                    family= "anb-family"
                g ,(fam_structure,fam_ids) = genealogia.onto_folders_correspondence(seed,family=family,entities=fsgram)
                #! error handling needed here for errors in the seed file
            
                file_structure = blocks.dict_to_file(fam_structure,fam_ids)
                
                with open(os.path.join(dataControl.find_anb(),'anbtemp.txt'),'w') as anbtemp:             
                    anbtemp.write(file_structure)

            
            if args.filename:
                genealogia.gen_onto_file(g,args.filename[0])
                
                if args.out:
                    shutil.move(f"{args.filename[0]}.n3", args.out[0])
                    shutil.move(f"{args.filename[0]}.rdf", args.out[0])

            genealogia.gen_onto_file(g,"anbsafeonto")


    elif args.subcommand == 'sync':
        
        path = dataControl.find_anb()
       
        if path != None:
            path = os.path.dirname(path)
            ontofile = os.path.join(path,".anbtk/anbsafeonto.rdf")
            g = genealogia.read_onto_file(ontofile)
            controlsystem.version_control(path,g)
            genealogia.gen_onto_file(g,'anbsafeonto')
        else:
            print("✗ Not in any initialized ANB folder.")
        
    else:
        args.func(args.name, args.attributes, args)