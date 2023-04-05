import os


def process_family(file):
    
    os.getcwd()
    couples = {}
    with open(file, 'r') as f:
        contents = f.read()
        lines = contents.splitlines()
    aux = []
    current = ''
    for line in lines:
        if '+' in line:
            couples[line] = []
            current = line
        elif line == '':
            couples[current]  = aux
            aux = []
        else:
            aux.append(line.strip())
    print(couples)
    return couples


def gen_structure(file):
    
    couples = process_family(file)

    if not os.path.exists("anb-family"):
        os.mkdir("anb-family")
    os.chdir("anb-family")
    for couple,children in couples.items():
        if not os.path.exists(couple):
            os.mkdir(couple)
        if not os.path.exists(p1:=couple.split('+')[0]):
            os.mkdir(p1)
            os.symlink(f'../{couple}',f'{p1}/{couple}')
        if not os.path.exists(p2:=couple.split('+')[1]):
            os.mkdir(p2)
            os.symlink(f'../{couple}',f'{p2}/{couple}')
        for filho in children:
            if not os.path.exists(filho):
                os.mkdir(filho)
                os.symlink(f'../{filho}',f'{couple}/{filho}')





gen_structure('relations.txt')


