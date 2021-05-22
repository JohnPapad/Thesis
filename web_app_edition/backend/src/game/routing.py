# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from game_nmm import consumers #import game_nmm.consumers 

websocket_urlpatterns = [
    re_path(r'ws/game_nmm/(?P<room_name>\w+)/$', consumers.Game_NMMConsumer), #url pattern for game against another player
    re_path(r'ws/gameAI_nmm/(?P<player_marker>\w+)/(?P<difficulty>\w+)/$', consumers.GameAI_NMMConsumer), #url pattern for game against AI
    re_path(r'ws/lobby_nmm/(?P<id>\w+)/(?P<username>\w+)/$', consumers.LobbyConsumer), #url pattern for lobby
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})