from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . import forms


def home_view(request):
    return HttpResponse('elo')


def registration_view(request):
    form = forms.RegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()

            if form.cleaned_data.get('is_instructor') is True:
                permission = Permission.objects.get(name='Can add course')
                instructor_group = Group.objects.get(name='instructors')
                user.groups.add(instructor_group)
                user.user_permissions.add(permission)
            else:
                permission = Permission.objects.get(name='Can view course')
                students_group = Group.objects.get(name='students')
                user.groups.add(students_group)
                user.user_permissions.add(permission)

            return redirect(reverse_lazy('user:login'))

    return render(request, 'user/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(email=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse_lazy('contact:form'))

    else:
        form = forms.LoginForm()

    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('user:login'))
