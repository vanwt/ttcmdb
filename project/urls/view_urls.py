from django.urls import path
from ..views import *

urlpatterns = [
    path('project/', ProjectView.as_view(), name='project'),
    path('create-project/', CreateProjectView.as_view(), name='create-project'),
    path('update-project/<str:id>/', UpdateProjectView.as_view(), name='project-update'),
]
