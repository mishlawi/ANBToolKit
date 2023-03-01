defaultFsgram= """Pessoa : H* , Bio, Foto .
Album : Foto*.

H : r'h[0-9]+\-\w+\.\w+'
Bio : r'b[0-9]+\-\w+\.\w+'
Foto : r'p[0-9]+\-\w+\.\w+'

UNIVERSE

Story -> Title,Author,Date
Biography -> Name,Birthday,Birthplace,Occupation,Death
Pessoa -> Name,Age

FORMATS

markdown
latex


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

markdownbook= """# Ancestors Notebook

<sup>*Automatically generated*</sup>

## Table of Contents"""


defaultdgu = """
---
id:

---"""



template1 = r"""
---
title: {{tit}}
author:
 - remider that i need to pass the author
variables:
    section-titles: false
#    header-includes: \usepackage{natslides}


toc: true
number-sections: true

---
\newpage
# Ancestors Notebook

![]({{cover}})

\newpage
{% for  h in hs %}
## {{h.titulo}}
   {{ h.corpo }}
\newpage    
{% endfor %}

![Foto]({{img}})"""