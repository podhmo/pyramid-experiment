from . import models
from . import forms

from zope.interface import Interface
from zope.interface import Attribute

class IMapping(Interface):
    kind = Attribute("kind")
    def as_dict():
        pass


class Shape(object):
    schema = SchemaMapping
    model = modelMapping

PointShape = Shape(Point,PointForm)
PointShape.model.from_id(id).as_dict()


class Convertor(object):
    def __init__(self, model, schema):
        self.model = model
        self.schema = schema

    def id_to_obj(self, _id):
        return self.model.query.filter_by(id=_id).one

    def obj_to_schema(self, obj=None):
        return self.schema() if obj is None else self.schema(obj.as_dict())

    def postdata_to_schema(self, postdata):
        return self.schema(postdata)

    def schema_to_obj(self, schema):
        return self.model.from_dict(schema.data)
##ugggggggggly
PointConvertor = Convertor(models.Point, forms.PointForm)
