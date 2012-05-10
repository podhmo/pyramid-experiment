from pyramid.view import view_config

@view_config(route_name="demo_index",renderer="point:templates/demo/index.mak")
def index(request):
    from js.bootstrap import bootstrap
    bootstrap.need()
    return {}
