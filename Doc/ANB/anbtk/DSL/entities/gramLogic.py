import os
import re

# *
# ** Controls the way the grammar can be organized and disposed
# * 


def interpreter(terminals,nonterminals):
    interpretation = {}
    for producao in nonterminals.keys():
        racional = []
        for id in nonterminals[producao]:
            collector = []            
            zoom(id,terminals,nonterminals,collector)
            if id[-1] == '*' or id[-1] == '+' or id[-1] == '?':
                racional.append((collector,id[-1]))
            else:
                racional.append((collector,''))
        if producao in interpretation.keys():
            aux = interpretation[producao]    
            interpretation[producao] = aux.append(racional)
        elif producao not in interpretation.keys():
            interpretation[producao] = racional 
    return interpretation
    

def zoom(value, terminals, nonterminals,buff):
    # Disposal : P, Album* .
    # P : H* , Bio, Foto .
    # Album : Foto*.

    if value[-1] == '*' or value[-1] == '+' or value[-1] == '?':
        elem = value[:-1]
    else:
        elem = value
    if elem in terminals.keys():
        if value[-1] == '*' or value[-1] == '+' or value[-1] == '?':
            buff.append((terminals[elem],value[-1]))
        else:
            buff.append((terminals[elem],''))
    elif elem in nonterminals.keys():
        for id in nonterminals[elem]:
            zoom(id,terminals,nonterminals,buff)



def verifyGrammar(lista,grammar):
    for producao in lista:
        for id in producao:
            if id[-1] == '*' or id[-1] == "+" or id[-1] == '?':
                id = id[:-1]

            if id not in grammar.keys():
                print("Gramatica mal formulada")
                exit()



# instead of receiving the whole grammar, choose a production aka a Universal element
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
            
            elif id[-1]=='?': # optional
                id = id[:-1]
                regex = grammar[id]
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                count = 0
                
                
                for elem in ficheiros:
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:
                        if count == 0:          # can only accept 1 max 
                            disposal.append(elem)
                        if count > 0:
                            print("existem ficheiros a mais")
                            exit()
                        count += 1
                                
        
            else: # 1 one element only
                count=0
                regex = grammar[id]
                print(grammar[id][0])
                regex = re.sub("r\'",'',grammar[id][0])
                regex = re.sub("\'",'',regex)
                
                for elem in ficheiros:
                    if re.match(regex,elem) and  ('.' + re.split(r'\.',elem)[1]) not in ignoredFiles:
                        
                        if count != 1:
                            disposal.append(elem)
                            count+=1
                        
                        if count > 1:
                            print("existem ficheiros a mais")
                            exit()


                        elif count < 1:
                            print("existem ficheiros a menos")
                            exit()
    return disposal
    




    