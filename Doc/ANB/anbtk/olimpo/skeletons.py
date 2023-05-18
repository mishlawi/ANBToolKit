# add path here
def dguStory(title,author,date,id):
    skeleton = rf"""---
id: {id}
format: latex
type: Story
about:
- 
author:
- {author}
date: {date} 
title: {title}
---
%Free text format here to add the story itself.
"""
    return skeleton


# add path here
def dguBio(id,name,born,death):
    skeleton = rf"""---
id: {id}
format: latex
type: Biography
about:
- 
individual: {name}
Birthdate: {born} 
Deathdate: {death}
---
%Free text format here to add more information.
"""
    return skeleton


def genDguImage(id,format,path,about=""):
    skeleton = rf"""---
id: {id}
format: {format}
type: Picture
about: 
- {about}
path: {path}
---
%Free text format here to add more information.
"""
    return skeleton
