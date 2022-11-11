import imghdr
import shutil
import re
import os
from handlers.html.html import *

#Todo add more file formats

def genHtml(files,dirOut,dirIn):
    
    directory = "public"
    path = os.path.join(dirOut,directory)
    if not os.path.exists(path):
        os.mkdir(path)
    
    #? it might be important to define case by case for each format the equivalent converter, unless a more simple aproach can be pursued      
    
    indexFile = os.path.join(dirOut,'index.html') # index.html
    fo = open(indexFile,'w')
    fo.write(header)
    fo.write(str(os.path.basename(dirIn) + '</h1>\n'))

    for file in files:
        consideredFile = os.path.join(dirIn,file)
        fileName = re.split(r'\.',file)[0]
        format = re.split(r'\.',file)[1]
    
        if imghdr.what(consideredFile): # verifies if it is an image file
            imageOriginalPath = os.path.join(dirIn,file) # original image path
            newImagePath = 'public/' + file
            shutil.copy(imageOriginalPath,path) # copies image to the specified path
            fo.write(f'<img src="{newImagePath}"')   
            fo.write(f'width="200"\nheight="250"/>')
            fo.write('\n<hr>')
    
        elif ('.' + format) == ".tex":
            os.system(f"make4ht -l -u -d {os.path.basename(dirOut)}/public {os.path.basename(dirIn)}/{file}") #! Cannot be OUT/public because its specific
            os.system("rm h*.*") #! this should be changed
            newHtml = fileName + '.html'
            htmlInfo = htmlFrame1 + f"public/{newHtml}" + htmlFrame2
            fo.write(htmlInfo + '<hr>')
        
        elif ('.' + format) == ".md":
            newHtml = fileName + '.html'
            os.system(f"pandoc -o  {os.path.basename(dirOut)}/public/{newHtml} {os.path.basename(dirIn)}/{file} ")
            htmlInfo = htmlFrame1 + f"public/{newHtml}" + htmlFrame2
            fo.write(htmlInfo + '<hr>')



    fo.write(endHtml)
    fo.close()        
