from pyramid.config.util import action_method
from .core import ConvertorMap
from .interfaces import IConvertorMap
from .interfaces import IConvertorFactory

class DirectiveException(Exception):
    pass

def _find_convertor_constructor(config):
    constrctor = config.registry.queryUtility(IConvertorFactory)
    if constrctor is None:
        raise DirectiveException("convertor factory is not found. use config.define_convertor_factory")
    return constrctor

def _find_convmap(config):
    cnvmap = config.registry.queryUtility(IConvertorMap)
    if cnvmap is None:
        constructor = _find_convertor_constructor(config)
        cnvmap = ConvertorMap(constructor)
        config.registry.registerUtility(cnvmap, IConvertorMap)
    return cnvmap

@action_method
def define_convertor_factory(config, factory):
    config.registry.registerUtility(factory, IConvertorFactory)

@action_method
def add_convertor(config, name, convertor):
    cnvmap = _find_convmap(config)
    cnvmap.register(name, convertor)

@action_method
def add_convertor_from_peaces(config, name, model=None, schema=None, classname=None):
    classname = classname or name
    cnvmap = _find_convmap(config)
    cnvmap.register_from_peaces(classname, name, model, schema)

