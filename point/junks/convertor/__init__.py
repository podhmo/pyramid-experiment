def includeme(config):
    config.add_directive("define_convertor_factory", ".directives.define_convertor_factory")
    config.add_directive("add_convertor", ".directives.add_convertor")
    config.add_directive("add_convertor_from_peaces", ".directives.add_convertor_from_peaces")

def get_convertor_map(request):
    from .interfaces import IConvertorMap
    return request.registry.queryUtility(IConvertorMap)
    
