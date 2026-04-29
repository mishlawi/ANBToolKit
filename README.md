# Ancestors Notebook Toolkit

ANBToolKit is a Python CLI toolkit for organizing genealogical and family-history material inside a Linux filesystem. It combines:

- a family-structure seed DSL
- an FSGram grammar for document/entity conventions
- DGU files with YAML-style metadata
- Jinja2/LaTeX-based book generation
- ontology-backed synchronization and relationship queries
- interactive projection editing tools

The project is oriented toward Linux users, researchers, and genealogists working with structured local archives.

## Install

Install the package from the repository root:

```bash
pip install .
```

Python dependencies are declared in `pyproject.toml`. Some commands also rely on external tools that are not installed by `pip`, especially:

- `pandoc`
- `pdflatex`
- `latexmk`

## Command overview

### Notebook setup

- `anbinit`
  Initialize an Ancestors Notebook in the current directory.

  ```bash
  anbinit [-h] [-s SOURCE]
  ```

- `anbfolders`
  Generate a new notebook folder structure from a family seed file.

  ```bash
  anbfolders [-h] -s SEED [-src SOURCE] [-fam FAMILY] [-fn [FILENAME]] [-o [OUT]]
  ```

- `anbsync`
  Force synchronization between the filesystem and the notebook ontology.

  ```bash
  anbsync [-h]
  ```

### Navigation and queries

- `anbsearch`
  Query relatives of an individual using relationship flags.

  ```bash
  anbsearch [-h] [-s] [-p] [-ua] [-gp] [-c] -i INDIVIDUAL [INDIVIDUAL ...]
  ```

- `anbcd`
  Resolve and print a related folder path.

  ```bash
  anbcd [-h] [-s] [-p] [-ua] [-gp] [-c] -i INDIVIDUAL [INDIVIDUAL ...]
  ```

  `anbcd` prints the target directory; it does not mutate the parent shell by itself. Use it like this:

  ```bash
  cd "$(anbcd -p -i 'Maria Silva')"
  ```

- `anbls`
  List the contents of a related folder.

  ```bash
  anbls [-h] [-s] [-p] [-ua] [-gp] [-c] -i INDIVIDUAL [INDIVIDUAL ...]
  ```

### DGU and document generation

- `anbdgu`
  Create an empty DGU or one based on a known FSGram entity.

  ```bash
  anbdgu [-h] [-e ENTITY] -f FILENAME
  ```

- `genBio`
  Generate a biography DGU.

  ```bash
  genBio [-h] -n NAME [-b BIRTH] [-d DEATH] [-bp BIRTHPLACE] [-o OCCUPATION]
  ```

- `genStory`
  Generate a story skeleton as `.tex` or `.dgu`.

  ```bash
  genStory [-h] -t TITLE [-a AUTHOR [AUTHOR ...]] [-d DATE] [-dgu]
  ```

- `genDguImage`
  Generate DGU files for image files.

  ```bash
  genDguImage [-h] [-f | -t]
  ```

### Conversions and books

- `tex2dgu`
  Convert one or more `.tex` files into DGU files.

  ```bash
  tex2dgu [-h] [-f FILE [FILE ...]]
  ```

- `dgu2texbook`
  Aggregate one or more DGUs into a LaTeX book.

  ```bash
  dgu2texbook [-h] [-f FILE [FILE ...] | -t]
  ```

- `dgubook`
  Aggregate DGU files into a PDF or Markdown notebook.

  ```bash
  dgubook [-h] [-f FILE [FILE ...] | -t | -p] [-md] [-all] [-tf] [-o OUTPUT]
  ```

### Grammar and projection editing

- `anbgrammar`
  Interactively edit entities and aggregators in the notebook FSGram.

  ```bash
  anbgrammar
  ```

- `anbfsgram`
  Show the current notebook FSGram declarations.

  ```bash
  anbfsgram
  ```

- `anbedit`
  Open the projection editor for family editing.

  ```bash
  anbedit
  ```

- `anbadd`
  Add a new couple through the projection editor flow.

  ```bash
  anbadd
  ```

## Notes

- The project currently assumes a Linux-style filesystem workflow.
- Notebook commands expect to run inside an initialized notebook unless explicitly creating one.
- Example data and sample DGUs are available under [`Data/`](/home/mishlawi/projects/ANBToolKit/Data).
