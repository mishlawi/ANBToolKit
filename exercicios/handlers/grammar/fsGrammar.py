

def verifyGrammar(lista,grammar):
    for producao in lista:
        for id in producao:
            if id[-1] == '*' or id[-1] == "+":
                id = id[:-1]

            if id not in grammar.keys():
                print("Gramatica mal formulada")