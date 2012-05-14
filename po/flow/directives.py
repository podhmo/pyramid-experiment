import zope.interface as zi
from pyramid.interfaces import IRequest
from pyramid.config.util import action_method

from .interfaces import IFlow
from .interfaces import IDirection
from .api import FlowDirection


def get_flow_direction(registry, direction_name):
    return registry.getUtility(IDirection, direction_name)


@action_method
def define_flow_direction(config, name, seq, cyclic=False):
    direction = FlowDirection(seq, cyclic=cyclic)
    config.registry.registerUtility(direction, IDirection, name)

@action_method
def add_route_flow(config, route_name, direction=None, direction_name=None, match_param="action"):
    assert direction or direction_name

    registry = config.registry
    if direction_name:
        direction = get_flow_direction(registry,direction_name)
    if isinstance(direction, basestring):
        direction = config.maybe_dotted(direction)
    route_flow = RequestFlowAdapterFactory(route_name, direction, match_param=match_param)
    registry.adapters.register([IRequest], IFlow, route_name, route_flow)

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

