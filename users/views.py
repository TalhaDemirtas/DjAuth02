from django.shortcuts import render, redirect
from .forms import UserProfileForm, UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'users/home.html')

def register(request):

    form_user = UserForm(request.POST or None)
    form_profile = UserProfileForm(request.POST or None)
    if form_user.is_valid() and form_profile.is_valid():

        user = form_user.save()

        profile = form_profile.save(commit=False)
        profile.user = user

        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']

        profile.save()
        messages.success(request, "Register successful")
        return redirect('home')

    context = {
        'form_profile': form_profile,
        'form_user': form_user
    }

    return render(request, 'users/register.html', context)


def user_login(request):

    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            messages.success(request, "Login successful")
            login(request, user)
            return redirect('home')

            # if user.is_active:
            #     messages.success(request, "Login successful")
            #     login(request, user)
            #     return redirect('home')
            # else:
            #     messages.error(request, "Account is not active")
            #     return render(request, 'users/user_login.html', {"form": form})
        else:
            messages.error(request, "Password or Username is wrong!")
            return render(request, 'users/user_login.html', {"form": form})
    return render(request, 'users/user_login.html', {"form": form})

def user_logout(request):
    messages.success(request, "You Logout!")
    logout(request)
    return redirect('home')