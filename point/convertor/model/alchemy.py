class ModelMapping(object):
    def __init__(self, model):
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
