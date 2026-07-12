from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from .forms import LoginForm


def login_view(request):
    # If already logged in, go directly to dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request=request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")