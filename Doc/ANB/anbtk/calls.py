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


rm_latex_unecessary = ['latexmk','-c']


