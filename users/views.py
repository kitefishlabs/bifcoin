from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView

from .forms import EmailUserCreationForm


class RegistrationView(CreateView):
    form_class = EmailUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'user/register.html'


def dashboard(request):
    return render(request, 'user/dashboard.html', {'claimable': linked_email})


def update(request):
    return render(request, 'user/update.html', {})
