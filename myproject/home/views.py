from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

# Create your views here.
def homepage(request):
    return render(request, 'home/home.html')

def dashboard(request):
    return render(request, 'home/dashboard.html')



@login_required
def profile_create(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            return redirect('home:profile')

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'home/profile.html', {
        'form': form,
    })