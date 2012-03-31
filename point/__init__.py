from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.include(".convertor")

    from .convertor.core import ModelSchemaConvertorFactory
    from .convertor.model.alchemy import ModelMapping
    from .convertor.schema.wtforms import SchemaMapping
    config.define_convertor_factory(ModelSchemaConvertorFactory(ModelMapping, SchemaMapping))
    config.set_request_property(".convertor.get_convertor_map", "C", reify=True)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('point_create', '/point/create', factory="point.resouces.PointResources")
    config.add_route('point_list', '/point/list', factory="point.resouces.PointResources")
    config.add_convertor_from_peaces("point", model=".models.Point", schema=".forms.PointForm")
    config.scan()
    return config.make_wsgi_app()

