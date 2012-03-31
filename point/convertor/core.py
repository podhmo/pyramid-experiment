class ModelMapping(object):
    def __init__(self,model):
        self.model = model

    def __call__(self, *args, **kwargs):
        return self.model(*args, **kwargs)

    def from_id(self, id_):
        return model.query.filter_by(id=id_).one()

    def as_dict(self, obj):
        from sqlalchemy.sql.operators import ColumnOperators
        return {k: getattr(obj, k) for k, v in obj.__class__.__dict__.iteritems() \
                    if isinstance(v, ColumnOperators)}

    def from_dict(self, D):
        instance = self.model()
        items_fn = D.iteritems if hasattr(D, "iteritems") else D.items
        for k, v in items_fn():
            setattr(instance, k, v)
        return instance

class _ListDict(dict):
    """ dummy multidict
    """
    def getlist(self, k):
        return [self[k]]

class WtformsSchemaMapping(object):
    def __init__(self, schema):
        self.schema = schema

    def __call__(self, *args, **kwargs):
        return self.schema(*args, **kwargs)

    def from_postdata(self, postdata):
        if hasattr(postdata, "getlist"):
            return self.schema(postdata)
        else:
            return self.schema(_ListDict(postdata))

    def from_dict(self, D):
        return self.schema(**D)

    def as_dict(self, schema):
        return schema.data

def convertor_factory(name, modelmapping, schemamapping):
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

    def __init__(self, model, schema):
        self.model = modelmapping(model)
        self.schema = schemamapping(schema)
        self.to = To(self.model, self.schema)

    attr = {}
    attr["__init__"] = __init__
    return type(name, (object, ), attr)

MyConvertor = convertor_factory("MyConvertor", 
                                ModelMapping, 
                                WtformsSchemaMapping)

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
