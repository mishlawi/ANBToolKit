
import os
import shutil

rm_latex_unecessary = ['latexmk','-c']


def pdflatex(filename):
    """
    Compile a LaTeX file to PDF using pdflatex.

    Args:
        filename (str): The name of the LaTeX file to be compiled.

    Returns:
        list: A list of arguments to be passed to subprocess.check_call()
              to compile the LaTeX file to PDF using pdflatex.

    Raises:
        ValueError: If filename does not end with '.tex'.

    """
    if not filename.endswith('.tex'):
    
        raise ValueError("filename must end with '.tex'")
    
    return ['pdflatex', filename]

def pandoc_latex_to_markdown(infile, outfile):
    """
    Convert a LaTeX file to Markdown using Pandoc.

    Args:
        infile (str): The input LaTeX file to be converted.
        outfile (str): The output Markdown file to be created.

    Raises:
        ValueError: If the input file does not have a .tex extension or if the output file does not have a .md extension.

    Returns:
        list: A list containing the command and arguments to be run by subprocess.call().
    """
    
    if not infile.endswith('.tex'):

        raise ValueError("filename must end with '.tex'")
    
    if not outfile.endswith('.md'):

        raise ValueError("filename must end with '.md'")
    
    return ['pandoc', '-s', infile, '-o', outfile ]

def move_to_output(path, out):
    """
    Move the file at the specified path to the output directory.

    Args:
        path (str): The path to the file to be moved.
        out (str): The path to the output directory.
    """
    if os.path.isfile(path):

        filename = os.path.basename(path)

        if not os.path.isdir(out):
            print(f"Error: Output directory {out} does not exist.")
            return

        shutil.move(path, os.path.join(out, filename))
    else:
        print(f"File not found at {path}")



