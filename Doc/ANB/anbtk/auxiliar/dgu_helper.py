import re
import yaml
import os
import subprocess
import imghdr
from datetime import datetime
from .. import dataControl

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
    



def parseAbstractDgu(filename):

    
    """
    Parses a dgu file and returns a dictionary containing its metadata and body.

    Arguments:
    - filename: a string representing the path to the dgu file.

    Returns: a dictionary containing the metadata and body of the dgu file.
    """

    

    if filename.endswith('.dgu'):
        print(os.path.abspath(filename))
        with open(os.path.abspath(filename)) as f:
            data = f.read()
        headers = re.search(r"(?<=\-\-\-)(.+|\n)+?(?=\-\-\-)", data).group()
        adgu = yaml.full_load(headers)
        text = re.split(r'\-\-\-', data)[2]
        adgu['body'] = text
        return adgu
    else:
        print(f"{filename} is not a dgu file")
        exit()
    
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

def parse_text_denomination(input):
    """
    Parses the universe file specified format and returns a dictionary of the form:
    {'category1': 'abbreviation1', 'category2': 'abbreviation2', ...}
    """

    start_index = input.find('---')
    if start_index == -1:
        return {}

    lines = input[start_index + 3:].strip().split('\n')
    result = {}

    for line in lines:
        line = line.strip()
        if line and not line.startswith('-'):
            category_name, _, abbreviation = line.partition('(')
            category_name = category_name.strip()
            abbreviation = abbreviation.rstrip(')')
            if abbreviation.strip():
                result[category_name] = abbreviation.strip()

    return result

def parse_text(input):
    """
    Parses the universe file specified format and returns a dictionary of the form:
    {'name1': ['item1', 'item2', ...], 'name2': ['item1', 'item2', ...], ...}
    """

    start_index = input.rfind('---')
    if start_index == -1:
        return {}

    lines = input[start_index + 3:].strip().split('\n')
    result = {}
    current_category = None

    for line in lines:
        line = line.strip()
        if line:
            if not line.startswith('-'):
                if '(' in line:
                    current_category = line.split('(')[0].strip()
                else:
                    current_category = line
                result[current_category] = []
            elif current_category:
                attribute = line[1:].strip()
                result[current_category].append(attribute)

    return result


def is_image(path):
    
    """
    Determine if a file is an image based on its content type.

    Args:
        path (str): The file path to check.

    Returns:
        bool: True if the file is an image, False otherwise.
    """
    
    content_type = imghdr.what(path)
    if content_type is not None:
        return True
    else:
        return False
    
def get_filename_no_extension(path):
    
    """
    Get the filename without extension from a file path.

    Args:
        path (str): The file path to process.

    Returns:
        str: The filename without extension.
    """

    file_name = os.path.basename(path) 
    file_name_without_ext = (os.path.splitext(file_name)[0])
    return file_name_without_ext



def isDguImage(path):
    """
    Determine if a file is an image using `is_image()`, after parsing the metadata.

    Args:
        path (str): The file path to check.

    Returns:
        bool: True if the file is an image, False otherwise.
    """
    cwd = os.getcwd()
    os.chdir(dataControl.get_root())
    adgu = parseAbstractDgu(path) 
    if adgu['path'] == '':
        print("path not available")
        return

    os.chdir(cwd)
    if (anbtk_path := dataControl.find_anb()) != None:
        os.chdir(os.path.dirname(anbtk_path))

    if is_image(adgu['path']):
        return True
    else:
        return False
    
def getCurrentTime():
    
    """
    Get the current date and time.

    Returns:
        str: The current date and time in the format 'day of month of year'.
    """
    now = datetime.now()
    formated = now.strftime("%d of %B of %Y")
    return formated
    


def getDate(adgu):
    """
    Extract the year from the 'date' field of the metadata.

    Args:
        adgu (dict): A dictionary containing metadata information.

    Returns:
        dict or None: If the 'date' field is present and contains a valid year, the 'date' field is updated to contain only the year, and the modified dictionary is returned. Otherwise, None is returned.
    """
    if 'date' in adgu.keys():
        pattern = r'\b\d{4}\b'
        matches = re.findall(pattern, str(adgu['date']))
        if matches:
            adgu['date'] = matches[0]
            return adgu
        else:
            return None
    else:
        return None


def updateTitleforId(adgu):
    """
    Update the 'title' field of the abstract representations of the dgu to be the same as the 'id' field if the former is missing or empty.

    Args:
        adgu (dict): A dictionary containing metadata information.

    Returns:
        None: The 'title' field of the input dictionary is modified in place.
    """
    if not "title" in adgu.keys() or adgu['title'] == '':
        adgu['title'] = adgu['id']






def parse_individual_dgu(dgu_path, dates, docs, imgs, cronology):
    """
    Parse a single .dgu file and add the data to the appropriate lists.

    Args:
        dgu_path (str): Path to the .dgu file.
        dates (dict): Dictionary containing various date-related information.
        docs (list): List of parsed document metadata.
        imgs (list): List of parsed image metadata.
        cronology (list): List of parsed document dates.

    Raises:
        Exception: If the file is not a .dgu file.

    Returns:
        None
    """

    if not dgu_path.endswith('.dgu'):
        print (f"{dgu_path} is not a dgu file!")
        exit()
    elif dgu_path == '':
        print(f"A error must have occurred")
        return 
    
    if isDguImage(os.path.relpath(dgu_path,dataControl.get_root())):
        adgu = parseAbstractDgu(dgu_path)
        adgu['path'] = os.path.relpath(parseAbstractDgu(dgu_path)['path'], os.getcwd()) # gets relative path
        imgs.append(adgu)
    else:
        elem_path = os.path.abspath(dgu_path)
        
        with open(elem_path) as elem_file:
            temp = elem_file.read()
            if aux:= re.split('---',temp):
                _, cabecalho, corpo = aux
                meta = yaml.safe_load(cabecalho)
                meta['corpo'] = corpo
                date = getDate(meta)
                if date is not None:
                    cronology.append(date)
                    if int(date['date']) < int(dates['oldest']):
                        dates['oldest'] = date['date']
                    updateTitleforId(meta)
                docs.append(meta)



def parse_dgu_tree(dgu_path,dirpath,dates,docs,imgs,cronology):

    """
    Parse a DGU tree, appending metadata to docs and images to imgs.

    Args:
    - dgu_path (str): path to the DGU file
    - dirpath (str): path to the directory containing the DGU file
    - dates (dict): dictionary with keys 'oldest' (str) and 'newest' (str)
                    representing the oldest and newest dates encountered
                    in the metadata
    - docs (list): list of metadata dictionaries
    - imgs (list): list of image dictionaries
    - cronology (list): list of dates encountered in the metadata
    """
    
    if dgu_path.endswith('.dgu'):
        elem_path = os.path.join(dirpath, dgu_path)
        
        if isDguImage(elem_path):
            adgu = parseAbstractDgu(elem_path)

                
            adgu['path'] = os.path.relpath(parseAbstractDgu(elem_path)['path'], os.getcwd())
            imgs.append(adgu)
        else:
            with open(elem_path) as elem_file:
                temp = elem_file.read()
                if aux:= re.split('---',temp):
                    (_,cabecalho,corpo) = aux
                    meta = yaml.safe_load(cabecalho) 
                    meta['corpo'] = corpo
                    if getDate(meta) is not None:
                        cronology.append(getDate(meta))
                        if int((old := getDate(meta)['date'])) < int(dates['oldest']):
                            dates['oldest'] = old 
                    if not "title" in meta.keys() or meta['title'] =='':
                        meta['title'] = meta['id']
                    docs.append(meta)


def tree_iteration(cwd,dates,docs,imgs,cronology,dgufunc):
    """
    Recursively iterates through a directory tree starting from the specified directory path.

    Args:
        cwd (str): The path to the directory to start iterating from.
        dates (list): A list to store date information.
        docs (list): A list to store document information.
        imgs (list): A list to store image information.
        cronology (list): A list to store chronological information.
        dgufunc (function): A function to process each file encountered during iteration.

    Returns:
        None
    """
    visited = set()
    for dirpath, _, filenames in os.walk(cwd):
        realpath = os.path.realpath(dirpath)

        if realpath in visited or os.path.basename(dirpath) == '.anbtk':
            continue
        visited.add(realpath)
        for filename in filenames:

            dgufunc(filename,dirpath,dates,docs,imgs,cronology)