class SchemaValidationException(Exception):
    def __init__(self, schema, message=None):
        self.schema = schema
        self.message = message

    def __str__(self, value):
        return self.message or "error: %s" % self.schema




