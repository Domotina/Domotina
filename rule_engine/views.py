from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import ScheduleDaily
# Create your views here.


def list_rules(request, place):
    rules = ScheduleDaily.objects.filter(sensor__floor__place=place)
    return render(request, 'list_rules.html', {'place_pk': place, 'rules': rules})


def create_rule(request, place, rule_pk):
    return render(request, 'create_rule.html', {})


def edit_rule(request, place, rule):
    return render(request, 'create_rule.html', {})


def delete_rule(request, place, rule):
    return render(request, 'create_rule.html', {})
