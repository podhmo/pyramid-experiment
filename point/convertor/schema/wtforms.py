class _ListDict(dict):
    """ dummy multidict
    """
    def getlist(self, k):
        return [self[k]]

class SchemaMapping(object):
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
