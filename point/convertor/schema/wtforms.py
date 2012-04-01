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

    def _validate_iff_need(self, form, validatep):
        if not validatep:
            return form
        elif form.validate():
            return form
        else:
            raise SchemaValidationException(form, message=str(form.errors))
        
    def from_postdata(self, postdata, validate=False):
        if hasattr(postdata, "getlist"):
            form = self.schema(postdata)
        else:
            form = self.schema(_ListDict(postdata))
        return self._validate_iff_need(form, validate)

    def from_dict(self, D):
        return self.schema(**D)

    def as_dict(self, schema):
        return schema.data
