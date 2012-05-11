import zope.interface as zi

class IDirection(zi.Interface):
    def __call__(current):
        pass


class IFlow(zi.Interface):
    obj = zi.Attribute("a object constructs a flow")
    mapping = zi.Attribute("direction at each check point A to B")

    def next_flow():
        pass

    def current_flow():
        pass

