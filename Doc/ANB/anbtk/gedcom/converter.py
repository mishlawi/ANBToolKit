'''
Converts anb template to gedcom and gedcom to anbtemplate

INDI (Individual):

Create a new entry in your structure to represent an individual.
Assign a unique identifier to the individual.
Extract relevant information such as name, birth date, and other attributes, and store them in your structure accordingly.
FAM (Family):

Create a new entry in your structure to represent a family.
Assign a unique identifier to the family.
Extract relevant information such as spouses, children, marriage date, and other attributes, and store them in your structure accordingly.
NAME:

Store the name value in your individual's entry within your structure.
BIRT (Birth):

Store the birth date value in your individual's entry within your structure.
MARR (Marriage):

Store the marriage date value in your family's entry within your structure.
HUSB (Husband):

Assign the husband identifier to the appropriate field in your family's entry within your structure.
Update the spouse field in the individual's entry with the family identifier.
WIFE (Wife):

Assign the wife identifier to the appropriate field in your family's entry within your structure.
Update the spouse field in the individual's entry with the family identifier.
CHIL (Child):

Add the child identifier to the list of children in the family's entry within your structure.
Update the child field in the individual's entry with the family identifier.

'''

from ..DSL.family import gramma


