def includeme(config):
    config.add_route("demo_index", "/")

    config.define_flow_direction("create-flow", ["input", "confirm", "create"])

    config.add_route("point_create", "/point/create/{action}", factory=".views.RegisterResource")
    config.add_route_flow("point_create", direction_name="create-flow", match_param="action")
    config.add_view(".views.RegisterView", context=".views.AfterInput", renderer="point:templates/point/input.mako")
    config.add_view(".views.RegisterView", match_param="action=input", attr="input", route_name="point_create")
    config.add_view(".views.RegisterView", match_param="action=confirm", attr="confirm", renderer="point:templates/point/input.mako", route_name="point_create")
    config.add_view(".views.RegisterView", match_param="action=create", attr="execute", route_name="point_create")


    config.scan(".views")

