from .interfaces import IConvertorMap
from .interfaces import IConvertor
from .interfaces import IConvertorFactory
from zope.interface import implements

class ConvertorMap(object):
    implements(IConvertorMap)
    def __init__(self, constructor):
        self.constructor = constructor

    def register(self, name, convertor):
        setattr(self, name, convertor)

    def register_from_peaces(self, name, *args, **kwargs):
        convertor = self.constructor.create(*args, **kwargs)
        self.register(name, convertor)

## model schema convertor
class ModelSchemaConvertorFactory(object):
    implements(IConvertorFactory)
    def __init__(self, modelmapping, schemamapping):
        self.modelmapping = modelmapping
        self.schemamapping = schemamapping
        self.create = self.create_factory()

    def create_factory(self):
        me = self
        class Convertor(object):
            implements(IConvertor)
            def __init__(self, model, schema):
                self.model = me.modelmapping(model)
                self.schema = me.schemamapping(schema)
                self.to = To(self.model, self.schema)
        return Convertor

class To(object):
    def __init__(self, mmapping,  smapping):
        self.mmapping = mmapping
        self.smapping = smapping

    def model_from_schema(self, schema):
        D = self.smapping.as_dict(schema)
        return self.mmapping.from_dict(D)

    def schema_from_model(self, model):
        D = self.mmapping.as_dict(model)
        return self.smapping.from_dict(D)
