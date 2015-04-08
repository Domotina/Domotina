from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

# Create your views here.

def home(request):
    return render(request, 'index.html')


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            print "logueo"
            redirect('map_home')
        else:
            print "no logueo"
    else:
        print "paila"
