from django.urls import path
from channels.routing import URLRouter
from realtime_chat.consumer import *

ws_application = URLRouter([
    path("chat/",ChatConsumer.as_asgi()),
    path('home/',HomeConsumer.as_asgi()),
])