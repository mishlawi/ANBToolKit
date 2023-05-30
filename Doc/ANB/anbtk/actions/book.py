import os
import sys
import datetime
import subprocess

from jinja2 import Environment, FileSystemLoader



from .. import dataControl

from ..auxiliar import dgu_helper
from ..auxiliar import argsConfig
from ..auxiliar import calls


#args = ['pandoc','-s','AncestorsNotebook.tex', '-o', 'AncestorsNotebook.pdf']


def dgubook():
    
    docs = []
    imgs = []
    cronology = []

    dates = {}
    dates['day'] = dgu_helper.getCurrentTime()
    dates['year'] = datetime.date.today().year
    dates['oldest'] = dates['year']

    arguments = argsConfig.a_dgubook()

    if arguments is None:
        print("You need to specify a flag. Use dgubook -h for more info.")
        sys.exit(1)

    with open('AncestorsNotebook.tex', 'w') as tempdgu:
        args =  calls.pdflatex('AncestorsNotebook.tex')
        cwd = os.getcwd()

        if not dataControl.find_anb():
            print("Initialize the ancestors notebook first.")
            sys.exit(1)

        environment = Environment(loader=FileSystemLoader(os.path.join(dataControl.find_anb(),"templates/")))
        dgus2tex = environment.get_template("anb1.j2")

        if arguments.file:
            for elem in arguments.file:
                dgu_helper.parse_individual_dgu(elem, dates, docs, imgs, cronology)           
            os.chdir(cwd)


        if arguments.tree:
            dgu_helper.tree_iteration(cwd, dates, docs, imgs, cronology, dgu_helper.parse_dgu_tree)

            os.chdir(cwd)
                
        try:
            if arguments.timeframe:
                dates['chronology'] = cronology
            
            tempdgu.write(dgus2tex.render(tit="Livro dos antepassados", docs=docs, imgs=imgs, dates=dates))
            tempdgu.flush()
            subprocess.check_call(args)

            if not arguments.all:
    
                subprocess.check_call(calls.rm_latex_unecessary)

            if arguments.output:
                calls.move_to_output('AncestorsNotebook.pdf',arguments.output[0])

            
            if arguments.markdown:

                subprocess.check_call(calls.pandoc_latex_to_markdown('AncestorsNotebook.tex','AncestorsNotebook.md'))
                os.remove("AncestorsNotebook.tex")
            
            os.chdir(cwd)
        
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            sys.exit(1)