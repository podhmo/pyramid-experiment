from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound
from .viewhelpers import RegisterPredicate
from pyramid.decorator import reify

from .convertor.schema import SchemaValidationException as AfterInput

class PointViewMixin(object):
    @reify
    def C(self):
        return self.request.convert_map.point
    
@view_defaults(route_name="point_create")
class PointRegisterView(PointViewMixin):
    """ register point model
    """
    def __init__(self, request):
        self.request = request

    @view_config(context=AfterInput, renderer="point/input.mako")
    def _after_input(self):
        return {"form": self.request._schema, "stage": "confirm"}

    @view_config(request_method="GET")
    def input(self):
        self.request._schema = self.C.schema()
        raise AfterInput
        
    @view_config(request_method="POST", renderer="point/confirm.mako",
                 custom_predicates=[RegisterPredicate.confirm_p])
    def confirm(self):
        form = self.C.schema.from_request(self.request, validate=True)
        return {"form": form, "stage": "execute"}

    @view_config(request_method="POST", custom_predicates=[RegisterPredicate.execute_p])
    def execute(self):
        form = self.C.schema.from_request(self.request, validate=True)
        obj = self.C.to.model_from_schema(form)
        self.request.context.add(obj)
        return HTTPFound(location=self.request.route_url("point_list"))
    
@view_defaults(route_name="point_list")
class PointListView(PointViewMixin):
    """ point listing
    """
    
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET",renderer="point/list.mako")
    def listing(self):
        points = self.C.model.query
        return {"points": points}
