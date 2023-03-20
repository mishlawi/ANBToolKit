import re
import yaml
import os
import subprocess
import imghdr




###################################### headings 

def heading2Latex(temp,tempdgu):

    """
    Converts a Markdown header and text into LaTeX format and writes it to a file.
    
    Arguments:
    - temp: a string containing the Markdown header and text to be converted.
    - tempdgu: a file object opened in write mode where the LaTeX output will be written.
    """

    headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",temp).group()
    adgu = yaml.full_load(headers)
    for elem in adgu['about']:
        tempdgu.write(f"\\footnote{{{elem}}}")
    if adgu['type'] == 'Story':
        tempdgu.write(f"\\section{{{adgu['title']}}}\n")
        tempdgu.write("Date: \t" + str(adgu['date']))
    else:
        tempdgu.write(f"\\section{{{adgu['id']}}}\n")
        
    tempdgu.write("""\\begin{center}
$\\ast$~$\\ast$~$\\ast$
\\end{center}""")
    text = re.split(r'\-\-\-',temp)[2]
    tempdgu.write("\t")
    tempdgu.write(text)
    tempdgu.write("\n") 
    tempdgu.write("\pagebreak\n\n")


def heading2markdown(temp,tempdgu):

    """
    Converts a YAML header and text into Markdown format and writes it to a file.
    
    Arguments:
    - temp: a string containing the YAML header and text to be converted.
    - tempdgu: a file object opened in write mode where the Markdown output will be written.
    """    

    headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)",temp).group()
    adgu = yaml.full_load(headers)
    
    if adgu['type'] == 'Story':
        tempdgu.write(f"# {{{adgu['title']}}}\n")
        tempdgu.write(f"### A story written or falling back to _{{{adgu['date']}}}_\n")

    elif adgu['type'] == 'Biography':
        tempdgu.write(f"## _A suscint Biography regarding:_\n")
    else:
        tempdgu.write(f"### {{{adgu['id']}}}\n")
        
    tempdgu.write("---\n")
    for elem in adgu.get('about',''):
        if elem == '':
            pass
        else:
            tempdgu.write(f"* {elem}\n")
    tempdgu.write("---\n")
    text = re.split(r'\-\-\-',temp)[2]
    tempdgu.write(text)
    tempdgu.write('\n<div class="page-break"></div>\n')   


def dguheadercomposer(newDgu,fileObject):

    """
    Writes the YAML header to a DGU file.

    Args:
    newDgu (dict): A dictionary containing the metadata information for the DGU file.
    fileObject (file object): The file object of the DGU file.
    """

    fileObject.write("---\n")
    yaml.dump(newDgu,fileObject,default_flow_style=False, sort_keys=False,allow_unicode=True)
    fileObject.write("---\n")
    fileObject.close()

######################################  metadata handlers

def docType(file):

    """
    Determines the type of document based on its filename.
    
    Arguments:
    - file: a string representing the filename of the document. 
    """

    if file.startswith("h"):
        return 'Story'
    elif file.startswith("p"):
        return 'Picture'
    elif file.startswith("b"):
        return 'Biography' 
    

def getFormat(string):

    """
    Determines the format of a document based on its file extension.
    
    Arguments:
    - string: a string representing the file extension of the document.
    """

    if string == 'tex':
        return 'latex'
    elif string == 'txt':
        return 'text'
    elif string == 'md':
        return 'markdown'
    else:
        return string
    



#!NEEDS MAINTANCE
def parseAbstractDgu(filename):
    

    """
    Parses a dgu file and returns a dictionary containing its metadata and body.

    Arguments:
    - filename: a string representing the path to the dgu file.

    Returns: a dictionary containing the metadata and body of the dgu file.
    """

    base, ext = os.path.splitext(filename)

    if ext == '.dgu':
        with open(os.path.abspath(filename)) as f:
            data = f.read()
        headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)", data).group()
        adgu = yaml.full_load(headers)
        text = re.split(r'\-\-\-', data)[2]
        adgu['body'] = text
        return adgu
    else:
        raise ValueError("File format is invalid")
    
###################################### latex

def aboutism(abouts):

    """
    Formats a list of strings as an itemized LaTeX string.
    
    Arguments:
    - abouts: a list of strings representing the items to be itemized.
    
    Returns: a string representing the formatted itemized list.
    """

    string="\\begin{itemize}"
    if len(abouts)>0:
        for elem in abouts:
            string+= f"\\item {elem}\n"
        string+="\\end{itemize}"
        return string
    else:
        return ""
    


def texSkeleton(texadgu):

    """
    Creates a LaTeX skeleton for a DGU item.
    
    Arguments:
    - texadgu: a dictionary containing information about the DGU item in a LaTeX-friendly format.
    
    Returns: a string representing a complete LaTeX skeleton for the DGU item.
    """

    string = f"""\\section{{{texadgu.get('title',"missing title")}}}
{aboutism(texadgu.get('about',[]))}
\\  
    \\begin{{center}}
        $\\ast$~$\\ast$~$\\ast$
    \\end{{center}}
    {texadgu.get('body',"")}
    """
    return string


def defaultConversion(text):
    """
    This function converts a given text from markdown format to latex format. It creates a temporary markdown file with the
    input text, uses the pandoc tool to convert it to latex format and returns the resulting latex text.
    
    Args:
    text (str): A string containing the text to be converted from markdown to latex.
    
    Returns:
    str: A string containing the converted latex text.
    """
    with open('temp.md', 'w') as temp_md:
        temp_md.write(text)
    subprocess.check_call(['pandoc', '-f', 'markdown', '-t', 'latex', 'temp.md', '-o', 'temp.tex'])
    with open('temp.tex') as temp_tex:
        temptext = temp_tex.read()

    return temptext


def parse_text(input):
    
    """
    Parses a string containing lines of text and returns a dictionary of the form:
    {'name1': ['item1', 'item2', ...], 'name2': ['item1', 'item2', ...], ...}
    """

    lines = input.strip().split('\n')
    result = {}   
    i = 0
    while i < len(lines):
        if lines[i].startswith('*'):
            name = lines[i][1:].strip().split()[0]            
            items = []
            i += 1
            while i < len(lines) and lines[i].startswith('\t*'):
                item = lines[i][2:].strip()               
                items.append(item)       
                i += 1       
            result[name] = items
        i += 1
    
    return result

def is_image(path):
    content_type = imghdr.what(path)
    if content_type is not None:
        return True
    else:
        return False
    
def get_filename_no_extension(path):
    file_name = os.path.basename(path) 
    file_name_without_ext = os.path.splitext(file_name)[0]  
    return file_name_without_ext



def isDguImage(path):
    adgu = parseAbstractDgu(path)    
    if is_image(adgu['path']):
        return True
    else:
        return False
    
