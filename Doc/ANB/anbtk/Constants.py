defaultFsgram= """Pessoa : H* , Bio, Foto .
Album : Foto*.

H : r'h[0-9]+\-\w+\.\w+'
Bio : r'b[0-9]+\-\w+\.\w+'
Foto : r'p[0-9]+\-\w+\.\w+'

UNIVERSE

Story -> title,author,date
Biography -> name,birthday,birthplace,occupation,death
Pessoa -> name,age

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
- {{autor}}
variables:
    section-titles: false
#    header-includes: \usepackage{natslides}


toc: true
number-sections: true

---

\newpage
{% for h in hs %}
\begin{center}

    \section{  {{h.title}}  }

    {% if h.author is defined and h.author != '' %}
            {% if h.author|length > 1 %}
                \textit{by}
                {% for a in h.author[:-1] %}
                    {{ a }},
                {% endfor %}
                {{ h.author[-1] }}
            {% else %}
                \textit{by} {{ h.author[0] }}
            {% endif %}
        {% endif %}

     

    \fbox{\begin{minipage}{0.9\textwidth}
        \vspace{0.2cm}
        \textbf{\textit{About}}
        \begin{itemize}
        {% for about in h.about %}
            \item \textit{ {{about}} }
        {% endfor %}
        \end{itemize}
    \end{minipage}}
    

$\ast$~$\ast$~$\ast$

\end{center}

\vspace{0.5cm}

\begin{center}
    \begin{minipage}{0.9\textwidth}
        \setlength{\parskip}{0.2cm}
        \setlength{\parindent}{0cm}
        \fontsize{12pt}{14pt}\selectfont
        {{h.corpo}}
    \end{minipage}
\end{center}
   
\newpage    
{% endfor %}
"""