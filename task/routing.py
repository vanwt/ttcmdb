from django.urls import path
from .customer import *

websocket_urlpatterns = [
    path('ws/playbook-run/', PlaybookConsumer),
    path("ws/run-module/", RunModuleConsumer)
]
