from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users/fetch', views.UserDatatable)
router.register(r'roles/fetch', views.RoleDatatable)

app_name = 'account'

urlpatterns = [
    # User Paths
    path('', include(router.urls)),
    path('users/', views.index, name='view_user'),
    path('users/create', views.create, name='add_user'),
    path('users/<int:id>', views.edit, name='change_user'),
    path('users/delete/<int:id>', views.delete, name='delete_user'),
    path('roles/', views.roleIndex, name='view_group'),
    path('roles/create', views.roleCreate, name='add_group'),
    path('roles/<int:id>', views.roleUpdate, name='change_group'),
]
