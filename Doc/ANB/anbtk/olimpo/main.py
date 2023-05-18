import argparse
import shutil
import time
import os 

from . import dgu
from . import genealogia
from . import controlsystem

# python onto.py genFolders --seed complexfam.txt -onto

# todo:
# if possible make it so that images can  automatically generate its dgus by using the sync command
# warnings for when u create a bio for an individual and there is information that is contraditory, specially the age

def main():
    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand',required=True,help='List of subcommands.')
    genSeedFile = subparsers.add_parser('genSF', help="genSeedFile from folder structure.",
                                        description="Generate a seed file from a set of folders correctly connected. Note: this is overly specific and not recommended.")
    genSeedFile.add_argument('--folder','-f', help="source folder to seed file.",nargs=1)
    genSeedFile.add_argument('--filename','-fn', help="name of the generated seed file.", nargs=1)
    genFolderStructure = subparsers.add_parser('genFolders',help="gen folder structure from seed file.")
    genFolderStructure.add_argument('--seed','-s',required=True, help="path to seed file to be converted.",nargs=1)
    genFolderStructure.add_argument('--filename','-fn', help="give a custom name to the ontology file. If not used, only a safe hidden file will be generated.",nargs='?')
    genFolderStructure.add_argument('--out','-o',help="output the ontology file to a certain directory.",nargs='?')

    
    genSync = subparsers.add_parser('sync')
    genSync.add_argument('-s','--source',nargs=1)

    genStory = subparsers.add_parser('genStory', help='generate a dgu story.')
    genStory.add_argument('-t', '--title', required=True, help='Title of the story')
    genStory.add_argument('-a', '--author', default="", help='Author of the story', nargs='+')
    genStory.add_argument('-d', '--date', default=time.strftime('%Y-%m-%d'), help='Date of the story')
    genStory.add_argument('-ab', '--about',default="",help="Details regarding what the Story is about - p.e. Individuals, Locations, ...",nargs='+')

    genBio = subparsers.add_parser('genBio', help='generate a dgu Biography.')
    genBio.add_argument('-n', '--name', required=True, help='Name of the individual')
    genBio.add_argument('-b', '--born', default="'?'", help='Year of birth (this will not have influence on the ontology itself.)', nargs=1)
    genBio.add_argument('-d', '--death', default="'?'", help='Year of death (this will not have influence on the ontology itself.)', nargs=1)


    genImage = subparsers.add_parser('genImage', help='generate dgu pictures.')
    group = genImage.add_mutually_exclusive_group()
    group.add_argument('-f','--file',help="Takes 1 or more files defined by the user.",nargs='+')
    group.add_argument('-t','--tree',help="Iterates through the entire tree of documents of the present directory.",action='store_true',default=False)
    genImage.add_argument('-ab', '--about',default="",help="Details regarding what the Picture(s) is/are about - p.e. Individuals, Locations, ...",nargs='+')


    args = parser.parse_args()
    
    if args.subcommand == 'genFolders':
        if args.seed:
            seed = args.seed[0]
            g = genealogia.onto_folders_correspondence(seed)
            if args.filename:
                genealogia.gen_onto_file(g,args.filename[0])
                if args.out:
                    shutil.move(f"{args.filename[0]}.n3", args.out[0])
                    shutil.move(f"{args.filename[0]}.rdf", args.out[0])

            genealogia.gen_onto_file(g,"anbsafeonto")
                
    elif args.subcommand == 'sync':
        
        path = dgu.find_anb()
        
        if path != None:
            path = os.path.dirname(path)
            ontofile = os.path.join(path,".anbtk/anbsafeonto.rdf")
            g = genealogia.read_onto_file(ontofile)
            controlsystem.version_control(path,g)
            genealogia.gen_onto_file(g,'anbsafeonto')
        else:
            print("Not in any initialized folder.")
        

    elif args.subcommand == 'genStory':
        date = args.date
        if args.author:
            dgu.genStory(args.title,args.author[0])
        else:
            dgu.genStory(args.title,date)

    elif args.subcommand == 'genImage':
        if args.file:
            if args.about:
                dgu.genDguImage_individual(args.file,args.about)
            else:
                dgu.genDguImage_individual(args.file,args.about)
        elif args.tree:
            if args.about:
                dgu.genDguImage_tree(args.about)
            else:
                dgu.genDguImage_tree()
        else:
            print("No arguments passed, please use --help to see the correct usage of this command")
      
    elif args.subcommand == 'genBio':
        name = args.name
        db = args.born
        dd = args.death
        dgu.genBio(name,db,dd)
         
                        
if __name__ == '__main__':

    main()
