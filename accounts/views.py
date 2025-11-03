from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timesince import timesince
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import CustomUser
from .forms import CustomUserChangeForm


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            django_login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', context={"form": form})


def profile(request, username):
    def status(active, banned):
        if banned:
            return 'Banned'
        else:
            if active:
                return 'Active'
            else:
                return 'Inactive'

    user = get_object_or_404(CustomUser, username=username)

    isself = request.user.is_authenticated \
        and request.user.username == user.username

    context = {
        'username': user.username,
        'about': user.about,
        'status': status(user.is_active, user.is_banned),
        'joined_since': timesince(user.date_joined, timezone.now(), depth=1),
        'isself': isself
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def preferences(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Preferences updated.")
            return redirect('preferences')
        else:
            # this is the only point of failure within the form
            errors = form.errors.get("username")
            messages.error(request, errors[0])
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/preferences.html', {'form': form})
