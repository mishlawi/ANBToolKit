
#? This module represents all the control version of the files and entities


import json
import os

from . import Constants
"""
Inicialization of anbtk.json file - present in the .anbtk hidden folder
"""
def initData():
    data = {}
    
    data['Biography'] = 0
    data['Story'] = 0
    
    # > more formats tba
    with open('anbtk.json','w') as anbtkfo:
        json.dump(data,anbtkfo)

"""
Updates the different entities on the json file
"""
def dataUpdate(file_type, name):
    
    with open('anbtk.json', 'r') as f:
        data = json.load(f)
    
    if file_type not in data:
        data[file_type] = 0
    
    data[file_type] += 1
    
    if file_type =='Biography':
        id = f"b{data[file_type]}-{name}"
    
    elif file_type == 'Story':
        id = f"h{data[file_type]}-{name}"
    
    # > more formats tba

    with open('anbtk.json', 'w') as f:
        json.dump(data, f)

    return id


def templateGen():
    os.mkdir('templates')
    os.chdir('templates')

    with open('anb1.j2','w') as f:
        f.write(Constants.template1)



