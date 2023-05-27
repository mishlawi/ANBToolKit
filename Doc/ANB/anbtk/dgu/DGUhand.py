import re 
import yaml
from pathlib import Path


from .dguObject import DGU as dgu


# generates universe.dgu and formats.dgu
def bigbang(stringUniverse):
    uniformats = re.findall(r"^[^-]+",stringUniverse,re.MULTILINE)
    uniatributes = [re.findall(r'\b[^,]+\b', x) for x in re.findall(r"-> (.*)", stringUniverse, re.MULTILINE)]
    #formatformats = re.findall(r'\w+',stringFormats,re.MULTILINE)
    universeAbout = "Universe of entities currently being used in this ancestors notebook"
   # formatsAabout = "Accepted types of file formats"
    print(uniformats)   
    with open(r'universe.dgu', 'w') as file:
        file.write("---\n")
        yaml.dump(dgu(id = "universe",format = "dgu",type="Universe",about=[universeAbout]),file,default_flow_style=False, sort_keys=False)
        file.write("---\n\n")
        uni = zip(uniformats,uniatributes)
        for format,atribute in uni:
            file.write(f"{format}\n")
            for elem in atribute:
                file.write('\t- ' + elem + '\n')
            file.write('\n')

    # # usar o objeto dgu para inserir coisas
    # with open(r'formats.dgu', 'w') as file:
    #     file.write("---\n")
    #     yaml.dump(dgu(id = "formats",format = "dgu",type="Format",about=[formatsAabout]),file,default_flow_style=False, sort_keys=False)
    #     file.write("---\n\n")
    #     for elem in formatformats:
    #         file.write(f"* {elem}\n")




def dgu_subclass(name, attributes, base_class=dgu):
    def __init__(self, id, format, type, about,path, *args):
        super(self.__class__, self).__init__(id, format, type, about,path)
        for attribute, value in zip(attributes, args):
            setattr(self, attribute, value)
    return type(name, (base_class,), {'__init__': __init__})










