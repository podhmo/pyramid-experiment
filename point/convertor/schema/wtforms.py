from . import SchemaValidationException

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

    def _validate_iff_need(self, schema, validatep, request):
        if not validatep:
            return schema
        elif schema.validate():
            return schema
        else:
            if request:
                # if hasattr(request, "_schema"):
                #     raise Exception("conflict! request._schema")
                request._schema = schema
            raise SchemaValidationException(schema, message=str(schema.errors))

    def from_request(self, request, validate=False, method="POST"):
        data = getattr(request, method)
        return self.from_postdata(data, validate=validate, request=request)

    def from_postdata(self, postdata, validate=False, request=None):
        if hasattr(postdata, "getlist"):
            form = self.schema(postdata)
        else:
            form = self.schema(_ListDict(postdata))
        return self._validate_iff_need(form, validate, request)

    def from_dict(self, D):
        return self.schema(**D)

    def as_dict(self, schema):
        return schema.data
