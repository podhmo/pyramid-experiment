from pyramid.view import view_config
from pyramid.view import view_defaults
from .viewhelpers import RegisterPredicate
from . import forms

class AfterInput(Exception):
    pass

@view_defaults(route_name="point_create")
class PointRegisterView(object):
    """ register point model
    """
    
    def __init__(self,request):
        self.request = request
        
    @view_config(request_mehod="GET")
    def input(self):
        form = forms.PointForm()
        return {"form": form}

    @view_config(request_mehod="POST", custom_predicates=[RegisterPredicate.confirm_p])
    def confirm(self):
        form = forms.PointForm(self.request.POST)
        if form.validate():
            return {"form": form, "stage": "execute"}
        else:
            self.request._form = form
            raise AfterInput

    @view_config(request_method="POST", context=AfterInput)
    def _reinput(self):
        return {"form": self.request._form}

    @view_config(request_mehod="POST", custom_predicates=[RegisterPredicate.execute_p])
    def execute(self):
        pass


        
        

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    one = DBSession.query(MyModel).filter(MyModel.name=='one').first()
    return {'one':one, 'project':'point'}
