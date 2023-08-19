from rdflib import Graph, Literal, Namespace
from rdflib.namespace import OWL, RDF, RDFS, XSD

from .. import dataControl

'''

essence == Ουσία == ousia

.greek

SISTEMA DE REPRESENTACAO DE CONHECIMENTO

'''

"""
==========================================================================================
================== ONTOLOGY INITIALIZATION AND PROPERTIES DEFINITION =====================
==========================================================================================
# """

# For classes and individuals, camel case is used (e.g., ArtifactModel,
# JohnDoe). For properties, each word is lowercase and joined by underscores (e.g., described_by). 

FAMILY = Namespace('http://example.org/family#')
DGU = Namespace('http://example.com/dgu#')

def ontology():

    g = Graph()
    g.bind('',FAMILY)
    g.bind('rdfs', RDFS)

    ont = FAMILY['family-ontology']
    g.add((ont, RDF.type, OWL.Ontology))
    g.add((ont, RDFS.label, Literal('Family Ontology')))

    family_class = FAMILY['Family']
    g.add((family_class, RDF.type, OWL.Class))
    g.add((family_class, RDFS.label, Literal('Family')))


    relationships_ontology(g)

    dgu_ontology(g)

    return g

def relationships_ontology(g):

    # Define the person class
    person_class = FAMILY['Person']
    g.add((person_class, RDF.type, OWL.Class))
    g.add((person_class, RDFS.label, Literal('Person')))

    has_parent_property = FAMILY['hasParent']
    g.add((has_parent_property, RDF.type, OWL.ObjectProperty))
    g.add((has_parent_property, RDFS.label,Literal('has_parent')))
    g.add((has_parent_property, RDFS.domain, person_class))
    g.add((has_parent_property, RDFS.range, person_class))

    # has Child 
    has_child_property = FAMILY['hasChild']
    g.add((has_child_property, RDF.type, OWL.ObjectProperty))
    g.add((has_child_property, RDFS.label,Literal('has_child')))
    g.add((has_child_property, RDFS.domain, person_class))
    g.add((has_child_property, RDFS.range, person_class))

    # has Spouse
    has_spouse_property = FAMILY['hasSpouse']
    g.add((has_spouse_property, RDF.type, OWL.ObjectProperty))
    g.add((has_spouse_property, RDFS.label,Literal('has_spouse')))
    g.add((has_spouse_property, RDFS.domain, person_class))
    g.add((has_spouse_property, RDFS.range, person_class))

    # has Path 
    has_path_property = FAMILY['hasFolder']
    g.add((has_path_property, RDF.type, OWL.DatatypeProperty))
    g.add((has_path_property, RDFS.label, Literal('has_path')))
    g.add((has_path_property, RDFS.domain, person_class))
    g.add((has_path_property, RDFS.range, XSD.string))


    nickname_property = FAMILY['hasNickname']
    g.add((nickname_property, RDF.type, OWL.DatatypeProperty))
    g.add((nickname_property, RDFS.label, Literal('has_nickname')))
    g.add((nickname_property, RDFS.domain, person_class))
    g.add((nickname_property, RDFS.range, XSD.string))


    # birth date
    birth_date_property = FAMILY['birthDate']
    g.add((birth_date_property, RDF.type, OWL.DatatypeProperty))
    g.add((birth_date_property, RDFS.label, Literal('has_birth_date')))
    g.add((birth_date_property, RDFS.domain, person_class))
    g.add((birth_date_property, RDFS.range, XSD.string))

    # death date
    death_date_property = FAMILY['deathDate']
    g.add((death_date_property, RDF.type, OWL.DatatypeProperty))
    g.add((death_date_property, RDFS.label, Literal('death date')))
    g.add((death_date_property, RDFS.domain, person_class))
    g.add((death_date_property, RDFS.range, XSD.string))

    # file path
    has_file_path_property = FAMILY['hasFilePath']
    g.add((has_file_path_property, RDF.type, OWL.DatatypeProperty))
    g.add((has_file_path_property, RDFS.label, Literal('has_file_path')))
    g.add((has_file_path_property, RDFS.domain, person_class))
    g.add((has_file_path_property, RDFS.range, XSD.string))


    subfolder_class = FAMILY['Subfolder']
    g.add((subfolder_class, RDF.type, OWL.Class))
    g.add((subfolder_class, RDFS.label, Literal('Subfolder')))
    #g.add((subfolder_class, RDFS.subClassOf, person_class))


    has_subfolder_property = FAMILY['hasSubfolder']
    g.add((has_subfolder_property, RDF.type, OWL.ObjectProperty))
    g.add((has_subfolder_property, RDFS.label, Literal('has_subfolder')))
    g.add((has_subfolder_property, RDFS.domain, subfolder_class))
    g.add((has_subfolder_property, RDFS.range, subfolder_class))


    # inverse properties
    g.add((has_spouse_property, OWL.inverseOf, has_spouse_property))
    g.add((has_child_property, OWL.inverseOf, has_parent_property))
    g.add((has_parent_property, OWL.inverseOf, has_child_property))


def dgu_ontology(g):
    
    person_class = FAMILY['Person']

    file_class = DGU['DGU']
    g.add((file_class, RDF.type, OWL.Class))
    g.add((file_class, RDFS.label, Literal('dgufile')))
    g.add((file_class, RDFS.domain, person_class))
    g.add((file_class, RDFS.range, XSD.string)) # this is the path, since it might be unique

    has_name = DGU['has_dgu_Name']
    g.add((has_name, RDF.type, OWL.DatatypeProperty))
    g.add((has_name, RDFS.label, Literal('has_name')))
    g.add((has_name, RDFS.domain, file_class))
    g.add((has_name, RDFS.range, XSD.string))

    has_format_property = DGU['has_dgu_Format']
    g.add((has_format_property, RDF.type, OWL.DatatypeProperty))
    g.add((has_format_property, RDFS.label, Literal('has_format')))
    g.add((has_format_property, RDFS.domain, file_class))
    g.add((has_format_property, RDFS.range, XSD.string))

    has_type_property = DGU['has_dgu_Type']
    g.add((has_type_property, RDF.type, OWL.DatatypeProperty))
    g.add((has_type_property, RDFS.label, Literal('has_type')))
    g.add((has_type_property, RDFS.domain, file_class))
    g.add((has_type_property, RDFS.range, XSD.string))

    has_about_property = DGU['has_dgu_About']
    g.add((has_about_property, RDF.type, OWL.DatatypeProperty))
    g.add((has_about_property, RDFS.label, Literal('has_about')))
    g.add((has_about_property, RDFS.domain, file_class))
    g.add((has_about_property, RDFS.range, XSD.string))




"""
==========================================================================================
========================================== DGUS ==========================================
==========================================================================================
"""

def dgu_base(entities,g):

    file_class = DGU['DGU']
    for key, value in entities.items():
        main_class = DGU[f'is{key}']
        g.add((main_class, RDF.type, OWL.Class))
        g.add((main_class, RDFS.label, Literal(key)))
        g.add((main_class, RDFS.subClassOf, file_class))   
        for elem in value:
            elem = elem.capitalize()
            temp_property = DGU[f'has{elem}']
            g.add((temp_property, RDF.type, OWL.DatatypeProperty))
            g.add((temp_property, RDFS.label, Literal(f'has_{elem}')))
            g.add((temp_property, RDFS.domain, main_class))
            g.add((temp_property, RDFS.range, XSD.string))
    


    
def format_names(input_list):
    if isinstance(input_list, str):
        return input_list
    elif isinstance(input_list, list):
        if len(input_list) == 1:
            return input_list[0]
        else:
            return ', '.join(input_list)
    else:
        return None

def add_dgu_file(adgu_path,attributes,graph):
    adgu_path = dataControl.relative_to_anbtk(adgu_path)
    dgu = DGU[adgu_path]
    print(attributes)
    for key,value in attributes.items():
        if isinstance(value,list):
            value = format_names(value)
        onto_name = key.capitalize()
        graph.add((dgu,DGU[f'has{onto_name}'],Literal(value,datatype=XSD.string)))


# def add_dgu_file(attributes,graph):
#     attributes['path'] = dataControl.relative_to_anbtk(attributes['path'])
#     dgu = DGU['dgufile']
#     for key,value in attributes.items():
#         onto_name = key.capitalize()
#         graph.add((dgu,DGU[f'has{onto_name}'],Literal(value,datatype=XSD.string)))

#comparar attributos, havendo diferenças eliminar o antigo e adicionar um novo, é mais rapido, ao usar o add_dgu_file



def get_dgu_attributes(dgu_path,g):
    path = dataControl.relative_to_anbtk(dgu_path)
    triples_with_subject  = g.triples((DGU[path], None, None))
    subject_exists = any(triples_with_subject)
    if not subject_exists:
        print(f"Subject {path} does not exist in the graph.")
        
    else:
        attributes = []
        for s, p, o in g.triples((DGU[path], None, None)):
            attributes.append(o)
        return attributes


def remove_dgu_file(dgu_path,g):
    path = dataControl.relative_to_anbtk(dgu_path)
    for s, p, o in g.triples((DGU[path], None, None)):
        g.remove((s, p, o))

def new_dgu_object(name,attributes,g):
    file_class = DGU['DGU']
    main_class = DGU[f'is{name}']
    g.add((main_class, RDF.type, OWL.Class))
    g.add((main_class, RDFS.label, Literal(name)))
    g.add((main_class, RDFS.subClassOf, file_class)) 
    for elem in attributes:  
        elem = elem.capitalize()
        temp_property = DGU[f'has{elem}']
        g.add((temp_property, RDF.type, OWL.DatatypeProperty))
        g.add((temp_property, RDFS.label, Literal(f'has_{elem}')))
        g.add((temp_property, RDFS.domain, main_class))
        g.add((temp_property, RDFS.range, XSD.string))


# def add_dgu(params,graph):
#     dgu = DGU[params['path']]
#     for key,value in params.items():
#         graph.add(dgu,DGU[f'has{key}'], Literal(value, datatype=XSD.string))


# def add_fileBio(name,db,dd,path,about,graph):
    
#     dgu = DGU[path]
#     graph.add((dgu, DGU['hasName'], Literal(name, datatype=XSD.string)))
#     graph.add((dgu, DGU['hasDateOfBirth'], Literal(db, datatype=XSD.string)))
#     graph.add((dgu, DGU['hasDateOfDeath'], Literal(dd, datatype=XSD.string)))
#     graph.add((dgu, DGU['hasFormat'], Literal('Latex', datatype=XSD.string)))
#     graph.add((dgu, DGU['hasType'], Literal('Biography', datatype=XSD.string)))
#     graph.add((dgu, DGU['hasAbout'], Literal(about, datatype=XSD.string)))
#     graph.add((dgu, DGU['hasFilePath'],Literal(path, datatype=XSD.string)))

"""
==========================================================================================
======================================= FOLDERS ==========================================
==========================================================================================


"""

def add_subfolder(parent_folder_name, subfolder_name, subfolder_path, graph):
    parent_folder_uri = FAMILY[parent_folder_name]
    subfolder_uri = FAMILY[subfolder_name]
    
    # Create a new Subfolder class instance with the specified name and path
    graph.add((subfolder_uri, RDF.type, FAMILY['Subfolder']))
    graph.add((subfolder_uri, FAMILY['hasFolderName'], Literal(subfolder_name, datatype=XSD.string)))
    graph.add((subfolder_uri, FAMILY['hasFolderPath'], Literal(subfolder_path, datatype=XSD.string)))
    
    # Add the subfolder instance as a value of the hasSubfolder property of the parent folder
    graph.add((parent_folder_uri, FAMILY['hasSubfolder'], subfolder_uri))


def remove_subfolder(parent_folder_name, subfolder_name, graph):
    parent_folder_uri = FAMILY[parent_folder_name]
    subfolder_uri = FAMILY[subfolder_name]
    
    # Remove the hasSubfolder property linking the parent folder to the subfolder
    graph.remove((parent_folder_uri, FAMILY['hasSubfolder'], subfolder_uri))
    
    # Remove all statements where the subfolder is the subject or object
    for s, p, o in graph.triples((subfolder_uri, None, None)):
        graph.remove((s, p, o))
    for s, p, o in graph.triples((None, None, subfolder_uri)):
        graph.remove((s, p, o))


def add_folder(name, path,graph):
    
    graph.add((FAMILY[name], FAMILY['hasFolderPath'], Literal(path, datatype=XSD.string))) 

"""
==========================================================================================
==================================== INDIVIDUALS =========================================
==========================================================================================
"""

def add_complete_individual(name,og_name,bd,dd,graph):
    add_individual(name,og_name,graph)
    add_birthdate(name,bd,graph)
    add_deathdate(name,dd,graph)


def add_nickname(name,nickname,graph):
    individual = FAMILY[name]

    graph.add((individual, FAMILY['nickname'], Literal(nickname, datatype=XSD.string)))

def update_nickname(name,nickname,graph):
    individual = FAMILY[name]
    graph.remove((individual,FAMILY['nickname'],None))
    add_nickname(name,nickname,graph)

def add_birthdate(name,date,graph):
    individual = FAMILY[name]

    graph.add((individual, FAMILY['birthDate'], Literal(date, datatype=XSD.string)))

def update_birthdate(name,date,graph):
    individual = FAMILY[name]
    graph.remove((individual,FAMILY['birthDate'],None))
    add_birthdate(name,date,graph)

def add_deathdate(name,date,graph):
    individual = FAMILY[name]

    graph.add((individual, FAMILY['deathDate'], Literal(date, datatype=XSD.string)))

def update_deathdate(name,date,graph):
    individual = FAMILY[name]
    graph.remove((individual,FAMILY['deathDate'],None))
    add_deathdate(name,date,graph)

def add_individual(individual,OgName, graph):
    
    individual = FAMILY[individual]
    
    graph.add((individual,RDF.type,FAMILY['Person']))
    graph.add((individual,RDFS.label,Literal(OgName)))


def delete_individual(individual, graph):
    
    individual = FAMILY[individual]
    
    graph.remove((individual, None, None))
    graph.remove((None,None,individual))


def delete_children_individual(individual,graph):
    #delete a individual that is children of a couple
    individual = FAMILY[individual]

    is_parent = False
    for s, p, o in graph.triples((individual, None, None)):
        if p == FAMILY['hasChild']:
            is_parent = True

    if is_parent:
        # it is not someone's children anymore, so all the connections regarding that can be removed

        graph.remove((individual,FAMILY['hasParent'],None))
        # if it is not a parent it doesnt exist in other instances
    else:
        graph.remove((individual, None, None))
        graph.remove((None,None,individual))

"""
==========================================================================================
==================================== RELATIONS =========================================
==========================================================================================
"""


def add_hasSpouse(individual1,individual2,graph):
    individual1 = FAMILY[individual1]
    individual2 = FAMILY[individual2]

    graph.add((individual1,FAMILY['hasSpouse'],individual2))
    graph.add((individual2,FAMILY['hasSpouse'],individual1))

def add_parent_children(parent1,parent2,child,graph):
    parent1 = FAMILY[parent1]
    parent2 = FAMILY[parent2]
    child =  FAMILY[child]

    graph.add((parent1, FAMILY['hasChild'], child))
    graph.add((parent2, FAMILY['hasChild'], child))
    graph.add((child, FAMILY['hasParent'], parent1))
    graph.add((child, FAMILY['hasParent'], parent2))


def switch_individual(old_individual, new_individual, name,db,dd, graph):
       
    add_individual(new_individual,name,graph)
    is_child = False
    for s, p, o in graph.triples((FAMILY[old_individual], None, None)):
        if p == FAMILY['hasParent']:
            is_child = True
        elif is_child == True and p == FAMILY['hasChild'] :
            graph.remove((s,p,o))
            graph.remove((None,FAMILY['hasParent'],s))
            graph.add((FAMILY[new_individual],p,o))
            graph.add((o,FAMILY['hasParent'],FAMILY[new_individual]))
        elif  is_child == True and p == FAMILY['hasSpouse'] :
            graph.remove((s,p,o))
            graph.remove((None,FAMILY['hasSpouse'],s))
            graph.add((FAMILY[new_individual],p,o))
            graph.add((o,FAMILY['hasSpouse'],FAMILY[new_individual]))

   
    if is_child == False:
        graph.remove((None,None,FAMILY[old_individual]))    
        graph.remove((FAMILY[old_individual],None,None))    

    
    graph.add((FAMILY[new_individual], FAMILY['birthDate'], Literal(db, datatype=XSD.string)))
    graph.add((FAMILY[new_individual], FAMILY['deathDate'], Literal(dd, datatype=XSD.string)))
    graph.add((FAMILY[new_individual], RDFS.label, Literal(name)))

"""
==========================================================================================
======================================= FILES ============================================
==========================================================================================
"""

def add_file(folder,path,graph):
    graph.add((FAMILY[folder], FAMILY['hasFile'], DGU[path]))

def remove_file(folder, path, graph):
    graph.remove((FAMILY[folder], FAMILY['hasFile'], Literal(path, datatype=XSD.string)))


def remove_file_special(path, graph):
    dgu = DGU[path]
    triples_to_remove = list(graph.triples((dgu, None, None))) + list(graph.triples((None, None, dgu)))
    for triple in triples_to_remove:
        graph.remove(triple)
