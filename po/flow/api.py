import zope.interface as zi

from .interfaces import IFlow
from .interfaces import IDirection


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
