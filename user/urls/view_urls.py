from django.urls import path
from user.views import *

urlpatterns = [
    # view
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('info/', UserInfo.as_view(), name='user-info'),
    path('list/', UserList.as_view(), name='user-list'),
    path('create/', UserCreate.as_view(), name='user-create'),
    path('password/update/', UpdatePassword.as_view(), name='update_pwd'),
    path('delete/<str:id>/', user_delete, name='user-del'),
    path('update/<str:id>/', UpdateUserView.as_view(), name='user-update'),
    path('menu/', MenuListView.as_view()),
    path("url/permission/", UrlPermissionView.as_view()),
    path("role/", RoleView.as_view()),
]

