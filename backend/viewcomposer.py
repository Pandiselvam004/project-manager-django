from django.utils.http import is_safe_url
from django.urls import resolve, reverse
from django.http.response import HttpResponse
from django.conf import settings


def page_title(request):
    view_name = resolve(request.path_info).url_name
    model = view_name.split('_')[-1]
    moduel_name = model + ' Management' if view_name != "home" else "Dashboard"
    page_title = moduel_name.title()
    return {"page_title": page_title}
