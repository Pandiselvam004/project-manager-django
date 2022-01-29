from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from . import forms
from account.forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

User = get_user_model()


def register(request):
    form = UserForm
    exception = ""

    if request.user.is_authenticated:
        return HttpResponseRedirect('/webpanel')

    if request.method == "POST":
        form = UserForm(request.POST or None)
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                User.objects.create_user(
                    first_name=obj.first_name,
                    last_name=obj.last_name,
                    username=obj.username,
                    password=obj.password,
                    email=obj.email,
                )
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=email, password=raw_password)
                login(request, user)
                return redirect('/webpanel')
            except Exception as error:
                exception = ValueError('Caught this error: ' + repr(error))
    return render(request, 'pages/register.html', {'form': form, 'error': exception})


def signin(request):
    form = forms.LoginForm

    if request.user.is_authenticated:
        return HttpResponseRedirect('/webpanel')

    if request.method == "POST":
        form = forms.LoginForm(request.POST or None)
        if form.is_valid():
            credentials = form.cleaned_data
            user = authenticate(
                username=credentials['email'], password=credentials['password'])

            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next') if request.GET.get('next') else '/webpanel')
            else:
                messages.add_message(request, messages.INFO,
                                     'Wrong credentials please try again')
                return HttpResponseRedirect('/login')

    return render(request, 'pages/login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('/login')


def home(request):
    return render(request, 'pages/index.html')
