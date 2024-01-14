"""
ASGI config for spider project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from core.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spider.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        'websocket': URLRouter([
            path('ws/chat/', ChatConsumer.as_asgi()),
        ])
    }
)
