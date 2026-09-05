from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
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
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
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