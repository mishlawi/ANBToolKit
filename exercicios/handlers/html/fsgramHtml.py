import imghdr
import shutil
import re
import os
from handlers.html.html import *



def travessia(grammar,dirIn,dirOut,ignoredFiles):
    
    # gets files
    ficheiros = []
    for file in os.listdir(dirIn):
        if os.path.isfile(os.path.join(dirIn, file)):
            ficheiros.append(file)
            print(file)

    # gets top production that defines the grammar
    top = list(grammar.values())[0]
    disposal = []
    
    # iterates through the productions that compose the top production
    
    for elem in top:
        
        # verifies types if productions have different elements
        
        for id in elem:
                  
            if id[-1]=='*': # 0 or plus elements
                id = id[:-1]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                
                for elem in ficheiros:
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:    
                        disposal.append(elem)
            
            elif id[-1]=='+': # 1 or plus elements
                id = id[:-1]
                count = 0
                regex = grammar[id]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                
                for elem in ficheiros:
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:
                        disposal.append(elem)
                        count+=1

                if count==0: 
                    print("não existem um ou mais ficheiros do tipo enunciado na gramática")
                    exit()
            
            else: # 1 one element only
                count=0
                regex = grammar[id]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                
                for elem in ficheiros:
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:
                        disposal.append(elem)
                        count+=1
                
                if count > 1:
                    print("existem ficheiros a mais")
                    exit()

                elif count < 1:
                    print("existem ficheiros a menos")
                    exit()
    
    genHtml(disposal,dirOut,dirIn)



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
