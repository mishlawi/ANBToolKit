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

from .auxiliar import argsConfig

from .auxiliar import dgu_helper
from .dgu import dguObject as dgu

from .DSL.entities import gramLogic

import shutil

terminal_width = shutil.get_terminal_size().columns
divider = "=" * terminal_width


def dgu2texbook():
    latex.dgu2texbook()


def tex2dgu(dirout=""):
    latex.tex2dgu(dirout)
    

def dgubook():
    book.dgubook()
    

def genDguImage():
    gen_dgus.genDguImage()


def genStory():
    gen_dgus.genStory()


def genBio():
    gen_dgus.genBio()


def genDgu(title, attributes, nameofthefile, dir):
    gen_dgus.genDgu(title,attributes,nameofthefile,dir)

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

def show_fsgram():
    gramLogic.show_declarations()

def edit_fsgram():
    gramLogic.add_to_fsgram()

    
############################## .anb ################################


def anb_init():


    args= argsConfig.a_anbinit()
    if args.source:
        file = args.source[0]
        dataControl.initanb(os.path.abspath(file))

    else:
        dataControl.initanb()
    print("Successfully generated a new ancestors notebook.")

def anb_genFolders():

    header= "ANbTk PROCESSING STATUS:".center(terminal_width)
    
    args = argsConfig.a_genFolders()    
    print(divider)
    print(header)
    print(divider)

    
    if args.source:
        fsgram = args.source[0]
        if not os.path.exists(fsgram):
            print("✗ The specified file does not exist.")
            exit()
    else:
        fsgram = ""
    

    if args.seed:

        seed = args.seed[0]
    
        if not os.path.exists(seed):
            print("✗ The specified file does not exist.")
            exit()
    
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


def anb_dgu():

    args = argsConfig.a_anbdgu()
    currentdir = os.getcwd()
    

    if dataControl.search_anbtk():
    
            if args.entity:
                entities = gramLogic.get_entities_fsgram()
                att_entities = gramLogic.get_entites_attributes(entities)
                abv_entities = gramLogic.get_entities_abbreviations(entities)
                if args.entity[0] in abv_entities.values():
                    args.entity[0] = gramLogic.get_entity_name_by_abv(args.entity[0],abv_entities)
                if args.entity[0] in entities.keys():     
                    genDgu(args.entity[0], att_entities[args.entity[0]], args.filename[0],currentdir)
                else:
                    print("✗ No entity exists with that name.")
                    exit()

            if not args.entity:
                os.chdir(currentdir)
                empty_dgu = dgu.DGU()
                with open(args.filename[0]+'.dgu',"w") as f:
                    dgu_helper.dguheadercomposer(empty_dgu,f)

    else:
        print("✗ You need to initialize an ancestors notebook")
        exit()

def anb_sync():
    args = argsConfig.a_anbsync()
    path = dataControl.find_anb()  
    if path != None:
        path = os.path.dirname(path)
        ontofile = os.path.join(path,".anbtk/anbsafeonto.rdf")
        g = genealogia.read_onto_file(ontofile)
        controlsystem.version_control(path,g)
        genealogia.gen_onto_file(g,'anbsafeonto')
    else:
        print("✗ Not in any initialized ANB folder.")
        exit()



