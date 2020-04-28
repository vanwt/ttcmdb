from django.urls import path
from ..views import (SessionListView, ClientView, SessionLogView, ConnectionLogInfoView)

urlpatterns = [
    path('client/', ClientView.as_view(), name='ssh-client'),
    path('connection/online/log/', SessionListView.as_view(), name='session-list'),
    path('connection/log/', SessionLogView.as_view(), name='session-log'),
    path("connection/log/<str:id>/", ConnectionLogInfoView.as_view(), name="connection-log")
]
