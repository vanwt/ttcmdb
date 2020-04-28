from django.urls import path
from .customer import *

websocket_urlpatterns = [
    path('ssh/web/',SSHClient)
]