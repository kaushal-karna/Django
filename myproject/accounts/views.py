from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from home.models import Profile


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:home_page')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
             # --- ADD THIS PART ---
            # Look for 'next' in the URL query parameters (e.g., ?next=/teachers/teacher-lists/)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect('home:home_page')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form
    })



def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def register_view(request):

    if request.user.is_authenticated:
        return redirect('home:home_page')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            Profile.objects.create(user=user)

            login(request, user)

            return redirect('home:home_page')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })