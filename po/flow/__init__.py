def includeme(config):
    """
    in configuration phase:
    ----------------------------

    define view-flow: "create-flow"  /foo/create/input => /foo/create/confirm => /foo/create/execute
    and binds at foo_create route

    >>> config.define_flow_direction(name="create-flow", ["input", "confirm", "execute"])
    >>> config.add_route("foo_create", "/foo/create/<action>")
    >>> config.add_route_flow("foo_create", direction="create-flow", match_param="action")


    in view function:
    -----------------------------

    >>> api.next_flow_url(request, *args, **kwargs) ## almost same at request.current_route_url(*args, **kwargs)
    >>> api.next_flow_path(request, *args, **kwargs) ## almost same at request.current_route_path(*args, **kwargs)
    """

    config.add_directive("define_flow_direction", ".directives.define_flow_direction")
    config.add_directive("add_route_flow", ".directives.add_route_flow")
    config.set_request_property(".api.next_flow_url", name="next_flow_url", reify=True)
    config.set_request_property(".api.next_flow_path", name="next_flow_path", reify=True)
