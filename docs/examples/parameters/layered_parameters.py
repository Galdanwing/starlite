from typing import Dict, Union

from starlite import Controller, Router, Starlite, get
from starlite.params import Parameter


class MyController(Controller):
    path = "/controller"
    parameters = {
        "controller_param": Parameter(int, lt=100),
    }

    @get("/{path_param:int}")
    def my_handler(
        self,
        path_param: int,
        local_param: str,
        router_param: str,
        controller_param: int = Parameter(int, lt=50),
    ) -> Dict[str, Union[str, int]]:
        return {
            "path_param": path_param,
            "local_param": local_param,
            "router_param": router_param,
            "controller_param": controller_param,
        }


router = Router(
    path="/router",
    route_handlers=[MyController],
    parameters={
        "router_param": Parameter(str, regex="^[a-zA-Z]$", header="MyHeader", required=False),
    },
)

app = Starlite(
    route_handlers=[router],
    parameters={
        "app_param": Parameter(str, cookie="special-cookie"),
    },
)
