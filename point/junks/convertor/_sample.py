"""
from . import convertor_factory
from .model.alchemy import ModelMapping
from .schema.wtforms import SchemaMapping
MyConvertor = convertor_factory("MyConvertor", 
                                ModelMapping, 
                                SchemaMapping)

if __name__ == "__main__":
    from point.forms import PointForm
    from point.models import Point
    C = MyConvertor(Point, PointForm)
    print C.model()
    print C.schema()
    form = C.schema(name="foo")
    print C.model.as_dict(C.model(name="foo"))
    print C.schema.as_dict(C.schema(name="foo"))
    print C.to.schema_from_model(C.model(name="foo"))
    form = C.schema.from_postdata(dict(name="foo", x=100, y=20))
    print form.validate()
    print C.to.model_from_schema(form)
"""
