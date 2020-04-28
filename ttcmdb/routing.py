from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import webssh.routing
import task.routing

# import task.routing

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            webssh.routing.websocket_urlpatterns + task.routing.websocket_urlpatterns
        )
    )
})
