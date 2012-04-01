class SchemaValidationException(Exception):
    def __init__(self, schema=None, message=None):
        self.schema = schema
        self.message = message

    def __str__(self):
        return self.message or "error: %s" % self.schema




