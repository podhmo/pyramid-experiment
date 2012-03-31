from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('point_create', '/point/create', factory="point.resouces.PointResources")
    config.add_route('point_list', '/point/list', factory="point.resouces.PointResources")
    config.scan()
    return config.make_wsgi_app()

