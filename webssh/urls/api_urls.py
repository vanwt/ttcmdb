from django.urls import path
from ..api import *

urlpatterns = [
    path("get-asset/", GetAssetSystemUserView.as_view()),
    path("make-link/", MakeLinkView.as_view())
]
