from django.shortcuts import render,redirect
from django.db import transaction
from .forms import UserForm,ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.

def home(request):
    return render(request,'home.html')

def product_page(request):
    return render(request,'product-page.html')

def cart(request):
    return render(request,'cart.html')

def profile(request):
    return render(request,'profile.html')

@login_required
@transaction.atomic
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('core:profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'account_update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
