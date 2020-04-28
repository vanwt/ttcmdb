from django.urls import path
from ..views import *



urlpatterns = [
    path('list/', TaskListView.as_view(), name='plan-list'),
    path('log-list/', LogListView.as_view(), name='log-list'),
    path('log-del/', LogDelView.as_view(), name='log-del'),
    path('show-crons/<int:id>/', show_crons, name='show-crons'),
    path('create-plan/', CreateTimedTaskView.as_view(), name='plan-create'),
    path('update-info/<int:id>/', UpdateTimedTaskView.as_view(), name='plan-info'),
    path('create-many-plan/', CreateManyTimedTaskView.as_view(), name='plan-many-create'),
    path('delete-plan/<int:id>/', DelTimedTask.as_view(), name='plan-del'),
]
