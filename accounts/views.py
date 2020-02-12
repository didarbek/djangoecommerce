from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm,ProfileRegistrationForm
from core.models import Profile
from django.contrib import messages

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        p_reg_form = ProfileRegistrationForm(request.POST)
        if form.is_valid() and p_reg_form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            p_reg_form = ProfileRegistrationForm(request.POST, instance=user.profile)
            p_reg_form.full_clean()
            p_reg_form.save()
            messages.success(request, f'Your account has been sent for approval!')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
        p_reg_form = ProfileRegistrationForm()
        context = {
        'form': form,
        'p_reg_form': p_reg_form
        }
    return render(request, 'registration/signup.html', context)