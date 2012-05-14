from pyramid.view import view_config

@view_config(route_name="demo_index",renderer="point:templates/demo/index.mak")
def index(request):
    from js.bootstrap import bootstrap
    bootstrap.need()
    return {}

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound
from . import forms

class AfterInput(Exception):
    def __init__(self, form=None, message=None):
        self.form = form
        self.message = message

    def __str__(self):
        return self.message or "error: %s" % self.form

class RegisterResource(object):
    Form = forms.PointForm
    def __init__(self, request):
        self.request = request

    def input_form(self):
        return self.Form()

    def confirmed_form(self):
        confirmed = self.Form(self.request.POST)
        if confirmed.validate():
            return confirmed
        else:
            raise AfterInput(form=confirmed)

class RegisterView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _after_input(self):
        return {"form": self.request._form}

    def input(self):
        raise AfterInput(form=self.context.input_form())
        
    def confirm(self):
        form = self.context.confirmed_form()
        return {"form": form}

    def execute(self):
        form = self.context.confirmed_form()
        self.context.create_model_from_form(form)
        return {}
        return HTTPFound()

    def __call__(self):
        return {"form": self.context.form}
