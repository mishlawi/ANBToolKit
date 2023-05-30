import os
import re
import yaml 
import subprocess


from ..auxiliar import dgu_helper
from ..auxiliar import argsConfig
from .. import dataControl

from ..dgu import dguObject as dgu



def dgu2texbook():
    
    arguments = argsConfig.a_dgu2texbook()
    
    fo = open("texbook.tex",'w')
    fo.write(f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{imakeidx}}
\\makeindex
\\begin{{document}}\n""")
    
    if arguments.file:
        for file in arguments.file:
            if file.endswith('.dgu'):
                if os.path.dirname(file)!='':
                        os.chdir(os.path.dirname(os.path.abspath(file)))
                temp = open(file,'r').read()
                headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",temp).group()
                adgu = yaml.full_load(headers)
                text = re.split(r'\-\-\-',temp)[2] 
                temptext = dgu_helper.defaultConversion(text)
                adgu['body'] = temptext
                fo.write(dgu_helper.texSkeleton(adgu))
                fo.write("\t")
                fo.write("\n")
                fo.write("\pagebreak")
            

            else:
                raise Exception(file + ' is not a dgu file.')
            
    elif arguments.tree:
        cwd = os.getcwd()
        for (dirpath,_,filenames) in os.walk(cwd):
            for filename in filenames:
                if filename.endswith('.dgu'):
                    temp = open(dirpath+'/'+filename,'r').read()
                    headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",temp).group()
                    adgu = yaml.full_load(headers)
                    text = re.split(r'\-\-\-',temp)[2]
                    temptext = dgu_helper.defaultConversion(text)
                    adgu['body'] = temptext
                    fo.write(dgu_helper.texSkeleton(adgu))
                    fo.write("\t")
                    fo.write("\n")
                    fo.write("\pagebreak")
    fo.write("\end{document}")
    
    fo.close()



def tex2dgu(dirout=""):
    arguments = argsConfig.a_tex2dgu()
    if arguments.file:
        for elem in arguments.file:
            filename = os.path.basename(elem)
            if filename.endswith(".tex"):
                if os.path.dirname(elem)!='':
                    os.chdir(os.path.dirname(os.path.abspath(elem)))
                file = open(filename).read()
                args = ['pandoc','-s', filename, '-o', filename[:-4] + '.md']
                subprocess.check_call(args)
                fo = open(filename[:-4] + '.md').read()
                headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",fo).group()
                adgu = yaml.full_load(headers)
                dgufile = open(filename[:-4]+'.dgu','w')
                id = re.search(r'(?<=\-).+(?=\.)',filename).group()
                text = re.split(r'\-\-\-',fo)[2]
                dgufile.write("---\n")
                format = dgu_helper.getFormat('tex')
                type = dgu_helper.docType(filename)
                abouts = re.findall(r'\\ind\{(.+?| )\}',file)
                path = os.path.abspath(filename)
                #path = dataControl.relative_to_anbtk(path)
                yaml.dump(dgu.DGU(id = id,format = format,type=type,about=abouts,path=path),dgufile,default_flow_style=False, sort_keys=False,allow_unicode=True)
                yaml.dump(adgu,dgufile)
                dgufile.write("---\n")
                dgufile.write(text)
                subprocess.check_call(['rm',filename[:-4]+'.md'])
                if dirout!="":
                    subprocess.check_call(['mv',filename+'.dgu',dirout])
            else:
                print("Not a latex file!")
                exit()