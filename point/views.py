from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound
from .viewhelpers import RegisterPredicate
from . import forms

class AfterInput(Exception):
    pass

@view_defaults(route_name="point_create")
class PointRegisterView(object):
    """ register point model
    """
    def __init__(self, request):
        self.request = request

    @view_config(context=AfterInput, renderer="point/input.mako")
    def _after_input(self):
        return {"form": self.request._form, "stage": "confirm"}

    def _form_from_postdata(self, postdata):
        form = forms.PointForm(postdata)
        if form.validate():
            return form
        else:
            self.request._form = form
            raise AfterInput

    @view_config(request_method="GET")
    def input(self):
        self.request._form = forms.PointForm()
        raise AfterInput
        
    @view_config(request_method="POST", renderer="point/confirm.mako",
                 custom_predicates=[RegisterPredicate.confirm_p])
    def confirm(self):
        form = self._form_from_postdata(self.request.POST)
        return {"form": form, "stage": "execute"}

    @view_config(request_method="POST", custom_predicates=[RegisterPredicate.execute_p])
    def execute(self):
        form = self._form_from_postdata(self.request.POST)
        context = self.request.context
        point = context.get_point()
        context.update_data(point, form.data)
        context.add(point)
        return HTTPFound(location=self.request.route_url("point_list"))
    
@view_defaults(route_name="point_list")
class PointListView(object):
    """ point listing
    """
    
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET",renderer="point/list.mako")
    def listing(self):
        points = self.request.context.get_point_list()
        return {"points": points}
