defaultFsgram= """P : H* , Bio, Foto .
Album : Foto*.
H : r'h[0-9]+\-\w+\.\w+'
Bio : r'b[0-9]+\-\w+\.\w+'
Foto : r'p[0-9]+\-\w+\.\w+'

EXECUTABLE

def main():
    print("Hello")

main()

UNIVERSE

Pessoa
História/Story
Biografia/Biography
Foto
Album
Ramo Familiar
Instituição
Casa
Arquivo
Genealogia
Notas


FORMATS

markdown
latex
text
yaml

IGNORE
.py 
.out
.fsgram
"""