import yaml

class DGU(yaml.YAMLObject):
    yaml_tag = u'!Dgu'

    def __init__(self, id="", format="", type="", about="", path=""):
        self.id = id
        self.format = format
        self.type = type
        self.about = about
        self.path = path

    def __repr__(self):
        return "%s(id=%r, format=%r, type=%r, about=%r, path=%r)" % (
            self.__class__.__name__, self.id, self.format, self.type, self.about, self.path)

yaml.emitter.Emitter.process_tag = lambda self, *args, **kw: None


