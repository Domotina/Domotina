from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ScheduleDaily
# Create your views here.


@login_required
def list_rules(request, place):
    rules = ScheduleDaily.objects.filter(sensor__floor__place=place)
    return render(request, 'list_rules.html', {'place_pk': place, 'rules': rules})


@login_required
def create_rule(request, place):
    return render(request, 'create_rule.html', {'place_pk': place})


@login_required
def edit_rule(request, place, rule_pk):
    rule = get_object_or_404(ScheduleDaily, pk=rule_pk)
    return render(request, 'create_rule.html', {'place_pk': place})


@login_required
def delete_rule(request, place, rule_pk):
    rule = get_object_or_404(ScheduleDaily, pk=rule_pk)
    rule.delete()
    return redirect('list_rules', place=place)
