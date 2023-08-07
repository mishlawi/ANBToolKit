import re 
import yaml
from pathlib import Path


from .dguObject import DGU as dgu


# generates universe.dgu
def bigbang(stringUniverse,terminals):
    uniformats = re.findall(r"^[^-]+",stringUniverse,re.MULTILINE)
    uniatributes = [re.findall(r'\b[^,]+\b', x) for x in re.findall(r"-> (.*)", stringUniverse, re.MULTILINE)]
    universeAbout = "Universe of entities currently being used in this ancestors notebook"
    with open(r'universe.dgu', 'w') as file:
        file.write("---\n")
        yaml.dump(dgu(id = "universe",format = "dgu",type="Universe",about=[universeAbout]),file,default_flow_style=False, sort_keys=False)
        file.write("---\n\n")
        uni = zip(uniformats,uniatributes)
        for (format, attribute), t in zip(uni, terminals.values()):
            t = t.replace(".","")
            file.write(f"{format} ({t})\n")
            for elem in attribute:
                file.write('\t- ' + elem + '\n')
            file.write('\n')

# def get_symbols(stringUniverse,terminals):
#     uniformats = re.findall(r"^[^-]+",stringUniverse,re.MULTILINE)
#     uniatributes = [re.findall(r'\b[^,]+\b', x) for x in re.findall(r"-> (.*)", stringUniverse, re.MULTILINE)]
#     print("!!!!")
#     print(uniformats)    
#     print(uniatributes)
#     print(terminals)
#     print("!!!!")



def dgu_subclass(name, attributes, base_class=dgu):
    def __init__(self, id, format, type, about,path, *args):
        super(self.__class__, self).__init__(id, format, type, about,path)
        for attribute, value in zip(attributes, args):
            setattr(self, attribute, value)
    return type(name, (base_class,), {'__init__': __init__})










