from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response


def central_home(request):
    return render_to_response('central_home.html')

def central_create(request):
    return render_to_response('central_create.html')
