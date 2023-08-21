"""
Structures of different documents
"""


def story(title,author,date):
      
    skeleton = rf"""\documentclass{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage{{imakeidx}}
\makeindex
\title{{{title}}}
\author{{{author}}}
\date{{{date}}}
\begin{{document}}

\maketitle

% Here starts the story

\printindex
\end{{document}}
"""
    return skeleton

def dguStory(title,author,date,id,path):
    skeleton = rf"""---
id: {id}
format: latex
type: Story
about: ''
path: {path} 
author: {author}
date: {date} 
title: {title}
---
%Add the story here
"""
    return skeleton




def note(notename,title,author,date):
    skeleton=f"""---
name: {notename}
title: {title}
author: {author}
date: {date}
---

# Relevant info


===
#""" + """{}"""
    return skeleton




def dguBio(name,birth="Month Day, Year",death="Month Day, Year",bp="City, Country",occupation="Field of work"):
    skeleton = rf"""---
id: {id}
format: latex
type: Biography
about:
- 
author:
- {author}
date: {date} 
title: {title}
---
%Add the Biography info here
"""
    return skeleton

def biography(name,birth="Month Day, Year",death="Month Day, Year",bp="City, Country",occupation="Field of work"):
    skeleton=rf"""# {name}

_Simplistic description of the individual._

## Individual Info

- **Birthday:** {birth}
- **Birthplace:** {bp}
- **Occupation:** {occupation}
- **Death:** {death}

## Biography

_Individual's life and achievements._


## Familiar Bonds

_Relevant Family Correlations._

## Legacy

_Individual impact and legacy._

## Sources

_If possible, relevant sources, in different formats (links,bibliography,etc)._

"""
    return skeleton

