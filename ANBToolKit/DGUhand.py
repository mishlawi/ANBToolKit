import os
import re 
import yaml
import subprocess
import datetime
import sys
from pathlib import Path
import argparse

from DGU import DGU as dgu


#pandoc -s h2-moto4.tex -o h2-moto4.md
#pandoc -f markdown universoConceptual.dgu -o _.pdf


# generates universe.dgu and formats.dgu
def bigbang(stringUniverse,stringFormats):
    uniformats = re.findall(r'\w+',stringUniverse)
    formatformats = re.findall(r'\w+',stringFormats)
    universeAbout = "Universe of entities currently being used in this ancestors notebook"
    formatsAabout = "Accepted types of file formats"
    print(uniformats)
    with open(r'universe.dgu', 'w') as file:
        file.write("---\n")
        yaml.dump(dgu(id = "Universe",format = "dgu",type="universe?",about=[universeAbout]),file,default_flow_style=False, sort_keys=False)
        file.write("---\n\n")
        for elem in uniformats:
            file.write(f"* {elem}\n")

    # usar o objeto dgu para inserir coisas
    with open(r'formats.dgu', 'w') as file:
        file.write("---\n")
        yaml.dump(dgu(id = "Formats",format = "dgu",type="formats?",about=[formatsAabout]),file,default_flow_style=False, sort_keys=False)
        file.write("---\n\n")
        for elem in formatformats:
            file.write(f"* {elem}\n")




dirin = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/ANBToolKit/ClaraVilar"
dirout = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/ANBToolKit/ClaraVilar"
test = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/ANBToolKit/h2-moto4.dgu"
test2 = "/mnt/c/Users/Duarte Vilar/OneDrive/Ambiente de Trabalho/Eu/tese/thesis/Thesis/ANBToolKit/h1-viagemCaboVerde.tex"
