from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD

'''

essence == Ουσία == ousia

.greek

'''

FAMILY = Namespace('http://example.org/family#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
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

    # Define the person class
    person_class = FAMILY['Person']
    g.add((person_class, RDF.type, OWL.Class))
    g.add((person_class, RDFS.label, Literal('Person')))

    # has parent
    has_parent_property = FAMILY['hasParent']
    g.add((has_parent_property, RDF.type, OWL.ObjectProperty))
    g.add((has_parent_property, RDFS.label,Literal('has parent')))
    g.add((has_parent_property, RDFS.domain, person_class))
    g.add((has_parent_property, RDFS.range, person_class))

    # has Child 
    has_child_property = FAMILY['hasChild']
    g.add((has_child_property, RDF.type, OWL.ObjectProperty))
    g.add((has_child_property, RDFS.label,Literal('has child')))
    g.add((has_child_property, RDFS.domain, person_class))
    g.add((has_child_property, RDFS.range, person_class))

    # has Spouse
    has_spouse_property = FAMILY['hasSpouse']
    g.add((has_spouse_property, RDF.type, OWL.ObjectProperty))
    g.add((has_spouse_property, RDFS.label,Literal('has spouse')))
    g.add((has_spouse_property, RDFS.domain, person_class))
    g.add((has_spouse_property, RDFS.range, person_class))

    # has Path 
    has_path_property = FAMILY['hasFolder']
    g.add((has_path_property, RDF.type, OWL.DatatypeProperty))
    g.add((has_path_property, RDFS.label, Literal('has path')))
    g.add((has_path_property, RDFS.domain, person_class))
    g.add((has_path_property, RDFS.range, XSD.string))

    # birth date
    birth_date_property = FAMILY['birthDate']
    g.add((birth_date_property, RDF.type, OWL.DatatypeProperty))
    g.add((birth_date_property, RDFS.label, Literal('birth date')))
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
    g.add((has_file_path_property, RDFS.label, Literal('has file path')))
    g.add((has_file_path_property, RDFS.domain, person_class))
    g.add((has_file_path_property, RDFS.range, XSD.string))


    subfolder_class = FAMILY['Subfolder']
    g.add((subfolder_class, RDF.type, OWL.Class))
    g.add((subfolder_class, RDFS.label, Literal('Subfolder')))
    g.add((subfolder_class, RDFS.subClassOf, person_class))


    has_subfolder_property = FAMILY['hasSubfolder']
    g.add((has_subfolder_property, RDF.type, OWL.ObjectProperty))
    g.add((has_subfolder_property, RDFS.label, Literal('has subfolder')))
    g.add((has_subfolder_property, RDFS.domain, subfolder_class))
    g.add((has_subfolder_property, RDFS.range, subfolder_class))


    # inverse properties
    g.add((has_spouse_property, OWL.inverseOf, has_spouse_property))
    g.add((has_child_property, OWL.inverseOf, has_parent_property))
    g.add((has_parent_property, OWL.inverseOf, has_child_property))

    dgu_ontology(g)

    return g

def dgu_ontology(g):
    person_class = FAMILY['Person']

    file_class = DGU['hasPath']
    g.add((file_class, RDF.type, OWL.Class))
    g.add((file_class, RDFS.label, Literal('File')))
    g.add((file_class, RDFS.domain, person_class))
    g.add((file_class, RDFS.range, XSD.string)) # this is the path, since it might be unique

    has_name = DGU['hasName']
    g.add((has_name, RDF.type, OWL.DatatypeProperty))
    g.add((has_name, RDFS.label, Literal('has name')))
    g.add((has_name, RDFS.domain, file_class))
    g.add((has_name, RDFS.range, XSD.string))

    has_format_property = DGU['hasFormat']
    g.add((has_format_property, RDF.type, OWL.DatatypeProperty))
    g.add((has_format_property, RDFS.label, Literal('has format')))
    g.add((has_format_property, RDFS.domain, file_class))
    g.add((has_format_property, RDFS.range, XSD.string))

    has_type_property = DGU['hasType']
    g.add((has_type_property, RDF.type, OWL.DatatypeProperty))
    g.add((has_type_property, RDFS.label, Literal('has type')))
    g.add((has_type_property, RDFS.domain, file_class))
    g.add((has_type_property, RDFS.range, XSD.string))

    has_about_property = DGU['hasAbout']
    g.add((has_about_property, RDF.type, OWL.DatatypeProperty))
    g.add((has_about_property, RDFS.label, Literal('has about')))
    g.add((has_about_property, RDFS.domain, file_class))
    g.add((has_about_property, RDFS.range, XSD.string))

    picture_class = DGU['Picture']
    g.add((picture_class, RDF.type, OWL.Class))
    g.add((picture_class, RDFS.label, Literal('Picture')))
    g.add((picture_class, RDFS.subClassOf, file_class))
    
    
    
    #################

    biography_class = DGU['Biography']
    g.add((biography_class, RDF.type, OWL.Class))
    g.add((biography_class, RDFS.label, Literal('Biography')))
    g.add((biography_class, RDFS.subClassOf, file_class))

    dob_property = DGU['hasDateOfBirth']
    g.add((dob_property, RDF.type, OWL.DatatypeProperty))
    g.add((dob_property, RDFS.label, Literal('has date of birth')))
    g.add((dob_property, RDFS.domain, biography_class))
    g.add((dob_property, RDFS.range, XSD.date))

    dod_property = DGU['hasDateOfDeath']
    g.add((dod_property, RDF.type, OWL.DatatypeProperty))
    g.add((dod_property, RDFS.label, Literal('has date of death')))
    g.add((dod_property, RDFS.domain, biography_class))
    g.add((dod_property, RDFS.range, XSD.date))

    ##################

    story_class = DGU['Story']
    g.add((story_class, RDF.type, OWL.Class))
    g.add((story_class, RDFS.label, Literal('Story')))
    g.add((story_class, RDFS.subClassOf, file_class))

    
    author_property = DGU['hasAuthor']
    g.add((author_property, RDF.type, OWL.DatatypeProperty))
    g.add((author_property, RDFS.label, Literal('has author')))
    g.add((author_property, RDFS.domain, story_class))
    g.add((author_property, RDFS.range, XSD.string))

    date_property = DGU['hasDate']
    g.add((date_property, RDF.type, OWL.DatatypeProperty))
    g.add((date_property, RDFS.label, Literal('has date')))
    g.add((date_property, RDFS.domain, story_class))
    g.add((date_property, RDFS.range, XSD.date))

    title_property = DGU['hasTitle']
    g.add((title_property, RDF.type, OWL.DatatypeProperty))
    g.add((title_property, RDFS.label, Literal('has title')))
    g.add((title_property, RDFS.domain, story_class))
    g.add((title_property, RDFS.range, XSD.string))

"""

Triple insertions to the graph are represented from this point foward.

"""
def gen_dgu_base():
    pass



def add_dgu(params,graph):
    dgu = DGU[params['path']]
    for key,value in params.items():
        graph.add(dgu,DGU[f'has{key}'], Literal(value, datatype=XSD.string))

def add_fileBio(name,db,dd,path,about,graph):
    
    dgu = DGU[path]
    graph.add((dgu, DGU['hasName'], Literal(name, datatype=XSD.string)))
    graph.add((dgu, DGU['hasDateOfBirth'], Literal(db, datatype=XSD.string)))
    graph.add((dgu, DGU['hasDateOfDeath'], Literal(dd, datatype=XSD.string)))
    graph.add((dgu, DGU['hasFormat'], Literal('Latex', datatype=XSD.string)))
    graph.add((dgu, DGU['hasType'], Literal('Biography', datatype=XSD.string)))
    graph.add((dgu, DGU['hasAbout'], Literal(about, datatype=XSD.string)))
    graph.add((dgu, DGU['hasFilePath'],Literal(path, datatype=XSD.string)))

########### folders

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


########### individuals


def add_birthdate(name,date,graph):
    individual = FAMILY[name]

    graph.add((individual, FAMILY['birthDate'], Literal(date, datatype=XSD.string)))

def add_deathdate(name,date,graph):
    individual = FAMILY[name]

    graph.add((individual, FAMILY['deathDate'], Literal(date, datatype=XSD.string)))

def add_individual(individual,OgName, graph):

    individual = FAMILY[individual]
    
    graph.add((individual,RDF.type,FAMILY['Person']))
    graph.add((individual,RDFS.label,Literal(OgName)))


def delete_individual(individual, graph):
    
    individual = FAMILY[individual]
    
    graph.remove((individual, None, None))


############# relations

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



############## files

def add_file(folder,path,graph):
    graph.add((FAMILY[folder], FAMILY['hasFile'], DGU[path]))

def remove_file(folder, path, graph):
    graph.remove((FAMILY[folder], FAMILY['hasFile'], Literal(path, datatype=XSD.string)))

def add_fileBio(name,db,dd,path,about,graph):
    
    dgu = DGU[path]
    graph.add((dgu, DGU['hasName'], Literal(name, datatype=XSD.string)))
    graph.add((dgu, DGU['hasFormat'], Literal('Latex', datatype=XSD.string)))
    graph.add((dgu, DGU['hasType'], Literal('Biography', datatype=XSD.string)))
    graph.add((dgu, DGU['hasFilePath'],Literal(path, datatype=XSD.string)))
    graph.add((dgu, DGU['hasAbout'], Literal(about, datatype=XSD.string)))
    graph.add((dgu, DGU['hasDateOfBirth'], Literal(db, datatype=XSD.string)))
    graph.add((dgu, DGU['hasDateOfDeath'], Literal(dd, datatype=XSD.string)))


def add_fileStory(name,title,path,author,date,about,graph):   
    dgu = DGU[path]
    graph.add((dgu, DGU['hasName'], Literal(name, datatype=XSD.string)))
    graph.add((dgu, DGU['hasFormat'], Literal('Latex', datatype=XSD.string)))
    graph.add((dgu, DGU['hasType'], Literal('Story', datatype=XSD.string)))
    graph.add((dgu, DGU['hasFilePath'],Literal(path, datatype=XSD.string)))
    graph.add((dgu, DGU['hasAbout'], Literal(about, datatype=XSD.string)))
    graph.add((dgu, DGU['hasTitle'], Literal(title, datatype=XSD.string)))
    graph.add((dgu, DGU['hasAuthor'], Literal(author, datatype=XSD.string)))
    graph.add((dgu, DGU['hasDate'], Literal(date, datatype=XSD.string)))

def remove_file_special(path, graph):
    dgu = DGU[path]
    triples_to_remove = list(graph.triples((dgu, None, None))) + list(graph.triples((None, None, dgu)))
    for triple in triples_to_remove:
        graph.remove(triple)



def add_Picture(name,path,format,about,graph):   
    dgu = DGU[path]
    graph.add((dgu, DGU['hasName'], Literal(name, datatype=XSD.string)))
    graph.add((dgu, DGU['hasFormat'], Literal(format, datatype=XSD.string)))
    graph.add((dgu, DGU['hasType'], Literal('Picture', datatype=XSD.string)))
    graph.add((dgu, DGU['hasFilePath'],Literal(path, datatype=XSD.string)))
    graph.add((dgu, DGU['hasAbout'], Literal(about, datatype=XSD.string)))

