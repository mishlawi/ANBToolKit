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
    header-includes: 
    - \usepackage{subcaption}




toc: true
number-sections: true

---
\newpage
\newcounter{tablecounter}

{% for h in hs %}
\begin{center}

    \section{  {{h.title}}  }

    {% if h.author is defined and h.author != 'False' %}
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

     
    {% if h.about is defined and h.about|length > 0 %}
    \fbox{\begin{minipage}{0.9\textwidth}
        \vspace{0.2cm}
        \textbf{\textit{About}}
        \begin{itemize}
        {% for about in h.about %}
            \item \textit{ {{about}} }
        {% endfor %}
        \end{itemize}
        \vspace{0.2cm}
    \end{minipage}}
    {% endif %}

$\ast$~$\ast$~$\ast$



\end{center}

\begin{center}
    \begin{minipage}{0.9\textwidth}
        \setlength{\parskip}{0.2cm}
        \setlength{\parindent}{0cm}
        \fontsize{12pt}{14pt}\selectfont
        {{h.corpo}}
    \end{minipage}
\end{center}

\stepcounter{tablecounter}
{% if h|length > 3 %}
\hyperref[table:\arabic{tablecounter}]{See metadata here}
{% endif %}
\newpage
{% endfor %}

\newcounter{tablecounter2}

\section{Tables}

{% for h in hs %}
\stepcounter{tablecounter2}
\begin{table}[h]
    \centering
    \begin{tabular}{|c|c|}
        \hline
        {% for k, v in h.items() if k not in ['title', 'author', 'corpo', 'about'] %}
            \textbf{ {{ k }} } & \textit{ {{ v }} } \\
            \hline
        {% endfor %}
    \end{tabular}
    \caption{Table \arabic{tablecounter2}} % Add a caption to the table with the current table counter value
    \label{table:\arabic{tablecounter2}} % Use the current table counter value as the label name
\end{table}
{% endfor %}

"""