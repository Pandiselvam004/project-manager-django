import re
from django.core.exceptions import PermissionDenied
from django.urls import resolve
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import is_safe_url
import numpy as np

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required Middleware"
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                redirect_to = settings.LOGIN_URL
                # 'next' variable to support redirection to attempted page after login
                if len(path) > 0 and is_safe_url(
                        url=request.path_info, allowed_hosts=request.get_host()):

                    # if next needed
                    # redirect_to = f"{settings.LOGIN_URL}?next={request.path_info}"
                    redirect_to = f"{settings.LOGIN_URL}"

                return HttpResponseRedirect(redirect_to)


class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.groups.filter(name = "admin").exists():
            current_url = resolve(request.path_info).url_name
            common_urls = ['home','login','logout','register']
            if request.user.is_authenticated and current_url not in common_urls and not request.is_ajax():
                permissions = [];
                for group in request.user.groups.all():
                    for permission in group.permissions.all():
                        permissions.append(permission.codename)
                if current_url in list(permissions):
                    return None
                else:
                    raise PermissionDenied
                # return None
            else:
                return None
