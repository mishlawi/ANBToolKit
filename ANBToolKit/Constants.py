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

frontdgubook = r"""
\documentclass[12pt]{article}
\usepackage{geometry}
\geometry{letterpaper, margin=1in}

\usepackage{graphicx}
\usepackage{xcolor}

\usepackage{titlesec}
\titleformat*{\section}{\huge\bfseries\color{blue}}
\titleformat*{\subsection}{\LARGE\bfseries\color{orange}}

\title{Auto-Generated Stories}
\author{}
\date{\vspace{-5ex}}

\begin{document}

\maketitle

\section*{Introduction}

Welcome to this collection of auto-generated stories! These tales were created using advanced algorithms and artificial intelligence techniques, and are sure to delight and intrigue readers of all ages.
"""