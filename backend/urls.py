from django.urls.conf import include
from django.views.generic.base import RedirectView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Initial Path
    path('', RedirectView.as_view(url='login')),
    path('login', views.signin, name='login',),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),

    # Basic Paths
    path('webpanel/', views.home, name='home'),

    # User Paths
    path('webpanel/', include('account.urls')),
    path('webpanel/projects', include('projects.urls'))
] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)
