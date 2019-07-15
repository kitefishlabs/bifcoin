from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone


def dashboard(request):
    return render(request, 'user/dashboard.html', {})


def register(request):
    return render(request, 'user/register.html', {})


def login(request):
    return render(request, 'user/login.html', {})


def logout(request):
    return render(request, 'user/logout.html', {})


def reset_password(request):
    return render(request, 'user/reset-password.html', {})\



def update(request):
    return render(request, 'user/update.html', {})
