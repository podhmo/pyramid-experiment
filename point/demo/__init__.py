def includeme(config):
    config.add_route("demo_index", "/")
    config.scan(".views")

