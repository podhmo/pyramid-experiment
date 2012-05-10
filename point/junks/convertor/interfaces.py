from zope.interface import Interface
class IConvertorFactory(Interface):
    def create(name, *args, **kwargs):
        pass

class IConvertor(Interface):
    pass

class IConvertorMap(Interface):
    def register(name, convertor):
        pass
