from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import redirect

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect('homepage')