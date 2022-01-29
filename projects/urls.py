from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'/fetch', views.ProjectDatatable)

app_name = 'projects'

urlpatterns = [
    path('/', views.index, name='view_projects'),
    path('/api', include(router.urls)),
    path('/create', views.create, name='add_projects'),
    path('/<int:id>', views.edit, name='change_user'),
    path('/delete/<int:id>', views.delete, name='delete_user'),
]
