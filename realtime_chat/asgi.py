"""
ASGI config for realtime_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from .routing import ws_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtime_chat.settings')

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(ws_application))
})
