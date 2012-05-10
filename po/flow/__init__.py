"""
config.define_flow(name="create-flow", ["input", "confirm", "execute"])

config.add_route("foo_create", "/foo")
config.add_flow(route_name="foo_create", flow="create-flow")
"""

import zope.interface as zi
from pyramid.interfaces import IRequest

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

"""
registry.registerAdapter([IRequest,IDirection], IFlow, <>, route_name)
"""

## request => flow => flow.next_flow_{url, path}

### api
def current_route_name_from_request(request):
    route = getattr(request, 'matched_route', None)
    route_name = getattr(route, 'name', None)
    if route_name is None:
        raise ValueError('Current request matches no route')
    return route_name


def get_flow_from_request(request):
    route_name = current_route_name_from_request(request)
    return request.registry.getAdapter(request, IFlow, name=route_name)
    # factory = request.registry.adapters.lookup([IRequest], IFlow, route_name)
    # return factory(request)

def current_flow_info(request):
    flow = get_flow_from_request(request)
    return (flow.route_name, flow.match_param, flow.current_point)
    
def next_flow_url(request, *elements, **kwargs):
    flow = get_flow_from_request(request)
    kwargs[flow.match_param] = flow.next_flow()
    return request.current_route_url(*elements, **kwargs)


def next_flow_path(request, *elements, **kwargs):
    flow = get_flow_from_request(request)
    kwargs[flow.match_param] = flow.next_flow()
    return request.current_route_path(*elements, **kwargs)


@zi.implementer(IFlow)
class RequestFlowAdapterFactory(object):
    def __call__(self, request):
        self.obj = request
        return self

    def __init__(self, route_name, direction_impl, match_param="action"):
        self.route_name = route_name ## needs?
        self.match_param = match_param
        self.obj = None
        self.mapping = direction_impl

    @property
    def current_point(self):
        return self.obj.matchdict[self.match_param] #request.matchdict["action"]        

    def next_flow(self):
        return self.mapping(self.current_point)

def create_direction_dict_from_seq(seq, cyclic=False):
    D = {}
    for before, after in  zip(seq, seq[1:]):
        D[before] = after

    if cyclic:
        D[seq[-1]] = seq[0]
    return D


@zi.implementer(IDirection)
class FlowDirection(object):
    def __init__(self, seq, cyclic=False):
        self.direction_dict = create_direction_dict_from_seq(seq, cyclic=cyclic)

    def __call__(self, current):
        return self.direction_dict[current]

        
### directive
def get_flow_direction(registry, direction_name):
    return registry.getUtility(IDirection, direction_name)


def define_flow_direction(config, name, seq, cyclic=False):
    direction = FlowDirection(seq, cyclic=cyclic)
    config.registry.registerUtility(direction, IDirection, name)

def add_route_flow(config, route_name, direction=None, direction_name=None, match_param="action"):
    assert direction or direction_name

    registry = config.registry
    if direction_name:
        direction = get_flow_direction(registry,direction_name)

    route_flow = RequestFlowAdapterFactory(route_name, direction, match_param=match_param)
    registry.adapters.register([IRequest], IFlow, route_name, route_flow)

    
def includeme(config):
    pass

if __name__ == "__main__":
    from pyramid import testing
    config = testing.setUp()
    
    define_flow_direction(config, "create-flow", ["input", "confirm", "create"])
    direction = get_flow_direction(config.registry, "create-flow")
    print direction

    config.add_route("demo1", "/demo1/<action>") ## action used by flow
    config.add_route("demo2", "/demo2/<action>") ## action used by flow
    
    add_route_flow(config, "demo1", direction_name="create-flow")
    add_route_flow(config, "demo2", direction=direction)
    
    def make_request(route_name=None, match_param="action", action="input"):
        route = testing.DummyResource(name=route_name)
        request = testing.DummyRequest(matched_route=route, matchdict={match_param: action})
        return zi.provider(IRequest)(request)

    print config.registry.adapters.lookupAll((IRequest, ), IFlow)
    request = make_request("demo1", match_param="action", action="input")
    
    print get_flow_from_request(request)
    print next_flow_path(request)
    request2 = make_request("demo1", match_param="action", action="confirm")
    print next_flow_path(request2)

    print current_flow_info(request)
    print current_flow_info(request2)










