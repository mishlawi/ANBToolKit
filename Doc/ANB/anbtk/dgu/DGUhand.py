
from .dguObject import DGU as dgu




def dgu_subclass(name, attributes, base_class=dgu):
    def __init__(self, id, format, type, about,path, *args):
        super(self.__class__, self).__init__(id, format, type, about,path)
        for attribute, value in zip(attributes, args):
            setattr(self, attribute, value)
    return type(name, (base_class,), {'__init__': __init__})

