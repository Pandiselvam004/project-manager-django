from django.contrib.auth.models import Group, Permission
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import RoleForm, UserForm
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django.core.files.storage import FileSystemStorage
from .datatables import RoleSerializer, UserSerializer
from django.contrib.auth.decorators import permission_required
# User Module

User = get_user_model()


class UserDatatable(viewsets.ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().exclude(id=user.id).exclude(email="admin@admin.com")


class RoleDatatable(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = RoleSerializer


def index(request):
    return render(request, 'pages/users/index.html')


def create(request):
    form = UserForm()
    exception = ""
    if request.method == "POST":
        form = UserForm(request.POST or None)
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                uploaded_file_url = upload_profile_image(request, None)
                user = User.objects.create_user(
                    first_name=obj.first_name,
                    last_name=obj.last_name,
                    username=obj.username,
                    password=request.POST.get('password'),
                    email=obj.email,
                    profile_img=uploaded_file_url
                )
                user.groups.add(request.POST.get('groups'))
                return redirect('/webpanel/users')
            except Exception as error:
                exception = ValueError('Caught this error: ' + repr(error))
    return render(request, 'pages/users/form.html', {'form': form, 'error': exception})


def edit(request, id):
    id = int(id)
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return redirect('/webpanel/users')
    form = UserForm(request.POST or None, instance=user)
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            uploaded_file_url = upload_profile_image(request, user)
            obj.profile_img = uploaded_file_url
            obj.save()
            user.groups.clear()
            user.groups.add(request.POST.get('groups'))
            return redirect('/webpanel/users')
    return render(request, 'pages/users/form.html', {'form': form, 'user': user})

def delete(request, id):
    id = int(id)
    try:
        user = User.objects.get(id=id).delete()
        return HttpResponse("User delete successfully")
    except Exception as error:
        exception = ValueError('Caught this error: ' + repr(error))
    return HttpResponse(exception)

def upload_profile_image(request, model):
    uploaded_file_url = model.profile_img if model else None
    if request.FILES and request.FILES['profile_img']:
        myfile = request.FILES['profile_img']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

    return uploaded_file_url

# Role Modules


def roleIndex(request):
    return render(request, 'pages/roles/index.html')


def roleCreate(request):
    form = RoleForm()
    exception = ""
    if request.method == "POST":
        form = RoleForm(request.POST or None)
        if form.is_valid():
            try:
                obj = form.save()
                permissions = request.POST.getlist('permissions')
                obj.permissions.add(*permissions)
            except Exception as error:
                exception = ValueError('Caught this error: ' + repr(error))
            return redirect('/webpanel/roles')
    return render(request, 'pages/roles/form.html', {'form': form, 'error': exception})


def roleUpdate(request, id):
    id = int(id)
    exception = ""
    try:
        role = Group.objects.get(id=id)
    except Group.DoesNotExist:
        return redirect('/webpanel/roles')
    form = RoleForm(request.POST or None, instance=role)
    if request.method == "POST":
        if form.is_valid():
            try:
                obj = form.save()
                obj.permissions.clear()
                permissions = request.POST.getlist('permissions')
                obj.permissions.add(*permissions)
            except Exception as error:
                exception = ValueError('Caught this error: ' + repr(error))
            return redirect('/webpanel/roles')
    return render(request, 'pages/roles/form.html', {'form': form, 'error': exception, 'group': role})
