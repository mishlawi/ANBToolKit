
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
    
    if not infile.endswith('.tex'):

        raise ValueError("filename must end with '.tex'")
    
    if not outfile.endswith('.md'):

        raise ValueError("filename must end with '.md'")
    
    return ['pandoc', '-s', infile, '-o', outfile ]

import os
import shutil

def move_to_output(path, out):
    """Move file at `path` to the output directory specified by `out`."""
    if os.path.isfile(path):

        filename = os.path.basename(path)

        if not os.path.isdir(out):
            print(f"Error: Output directory {out} does not exist.")
            return

        shutil.move(path, os.path.join(out, filename))
    else:
        print(f"File not found at {path}")



