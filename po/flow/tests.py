import unittest
from pyramid import testing

class FlowDirection(unittest.testCase):
    def setUp(self):
        self.config = testing.setUp()        

    def tearDown(self):
        testing.tearDown()

    def test_define_direction(self):
        pass
if __name__ == "__main__":
    unittest.main()
    
    define_flow_direction(config, "create-flow", ["input", "confirm", "create"])
    direction = get_flow_direction(config.registry, "create-flow")
    print direction

    config.add_route("demo1", "/demo1/<action>") ## action used by flow
    config.add_route("demo2", "/demo2/<action>") ## action used by flow
    
    add_route_flow(config, "demo1", direction_name="create-flow")
    add_route_flow(config, "demo2", direction=direction)
    
    def make_request(route_name=None, match_param="action", action="input"):
        route = testing.DummyResource(name=route_name)
        request = testing.DummyRequest(matched_route=route, matchdict={match_param: action})
        return zi.provider(IRequest)(request)

    print config.registry.adapters.lookupAll((IRequest, ), IFlow)
    request = make_request("demo1", match_param="action", action="input")
    
    print get_flow_from_request(request)
    print next_flow_path(request)
    request2 = make_request("demo1", match_param="action", action="confirm")
    print next_flow_path(request2)

    print current_flow_info(request)
    print current_flow_info(request2)

