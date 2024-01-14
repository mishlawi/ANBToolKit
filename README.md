# Ancestors Notebook Toolkit

The *Ancestors Notebook* is a versatile toolkit designed to streamline the management and organization of documents and information associated with family history and heritage.
This toolkit operates seamlessly within the Linux file system, employing conventions, commands, and Domain Specific Languages (DSLs) to name and organize directories.
 Its primary focus is on documents in a specific format known as DGU, exclusively created for the Ancestors Notebook toolkit. 

The overarching goal is to empower users with customized organizational control, ensuring a cohesive flow of ideas interwoven with the accumulation of genealogical data.

## Key Features

- **DGU Format**: The toolkit emphasizes a specific format, DGU, for document storage, facilitating a standardized and efficient approach to genealogical data.

- **Customized Organization**: Utilizing DSLs and conventions, the toolkit enables users to tailor their data organization, defining representative entities for different elements.

- **Template Generation**: Ancestors Notebook generates customizable templates in PDF format, offering a visually appealing and familiar view of genealogical information, organized by entities.

- **Version Control System**: The toolkit incorporates a version control system, leveraging a knowledge representation system in the form of an ontology. A projection editor allows users to view and manipulate the genealogical structure within the file system.

- **Python Implementation**: Developed in the Python programming language, the toolkit provides file system commands and utilizes Python modules for defining user views. Template creation is facilitated by the Jinja2 template generation engine.

- **Installation via pip**: Download and install the pyproject.toml using pip

## List of commands

- **anbsearch**
  - Command to retrieve information related to different family members within the Ancestors Notebook. Various flags allow querying specific relationships.
    ```bash
    anbsearch [-h] [-s] [-p] [-ua] [-gp] [-c] -i INDIVIDUAL [INDIVIDUAL ...]
    ```

- **anbcd**
  - Command to navigate between different directories within the Ancestors Notebook, considering familial connections. Flags represent different relationships.
    ```bash
    anbcd [-h] [-s] [-p] [-ua] [-gp] [-c] -i INDIVIDUAL [INDIVIDUAL ...]
    ```

- **anbdgu**
  - Command to generate a universal document with a generic structure or associated with a created entity.
    ```bash
    anbdgu [-h] [-e ENTITY] -f FILENAME
    ```

- **anbfolders**
  - Command to force synchronization of the different elements within the Ancestors Notebook.
    ```bash
    anbsync [-h]
    ```

- **anbls**
  - Command to quickly view content between different directories within the Ancestors Notebook, considering familial connections.
    ```bash
    anbls [-h] [-s] [-p] [-ua] [-gp] [-c] -i INDIVIDUAL [INDIVIDUAL ...]
    ```

- **anbsync**
  - Command to force synchronization of the different elements within the Ancestors Notebook.
    ```bash
    anbsync [-h]
    ```

- **dgubook**
  - Command to aggregate a number of .dgu files into a PDF book.
    ```bash
    dgubook [-h] [-f FILE [FILE ...] | -t | -p] [-md] [-all] [-tf] [-o OUTPUT]
    ```

- **dgu2texbook**
  - Command to aggregate a number of .dgu files into a LaTeX book.
    ```bash
    dgu2texbook [-h] [-f FILE [FILE ...] | -t]
    ```

- **genBio**
  - Command to generate a DGU with the structure of the Biography entity.
    ```bash
    genBio [-h] -n NAME -b BIRTH -d DEATH -bp BIRTHPLACE -o OCCUPATION
    ```

- **genDguImage**
  - Command to generate DGU files for image files.
    ```bash
    genDguImage [-h] [-f | -t]
    ```

- **genStory**
  - Command to generate a DGU with the structure of the Story entity.
    ```bash
    genStory [-h] -t TITLE [-a AUTHOR [AUTHOR ...]] [-d DATE] [-dgu]
    ```

- **tex2dgu**
  - Command to convert one or more DGUs into their equivalent LaTeX format.
    ```bash
    tex2dgu [-h] [-f FILE [FILE ...]]
    ```

- **anbinit**
  - Command to initialize an Ancestors Notebook without any genealogical structure.
    ```bash
    anbinit [-h] [-s SOURCE]
    ```
  - ![anbinit_full](https://github.com/mishlawi/ANBToolKit/assets/48862635/703d7593-3eab-4aaa-8817-38fd97cd7a33)


- **anbgrammar**
  - Command to edit and adapt different entities and aggregators to the FSGram grammar defining an Ancestors Notebook.
    ```bash
    anbgrammar
    ```
  - ![anbgrammar](https://github.com/mishlawi/ANBToolKit/assets/48862635/b6b84120-1f02-440e-b771-05e50b8fc1b7)
 

- **anbfsgram**
  - Command to display the different entities defined in the Ancestors Notebook FSGram.
    ```bash
    anbfsgram
    ```

- **anbedit**
  - Command to initialize the Projection Editor for family editing.
    ```bash
    anbedit
    ```
  - ![anbedit](https://github.com/mishlawi/ANBToolKit/assets/48862635/6d8c371e-dace-46f5-bd8f-eb4e64266fe8)

- **anbadd**
  - Command to initialize the Projection Editor for adding a new couple.
    ```bash
    anbadd
    ```
  - ![anbadd](https://github.com/mishlawi/ANBToolKit/assets/48862635/b921136d-e168-4783-b184-310e2c0bc559)
 

