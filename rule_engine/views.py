from django.shortcuts import render

# Create your views here.


def list_rules(request, place):
    return render(request, 'list_rules.html', {})