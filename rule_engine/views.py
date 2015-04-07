from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ScheduleDaily
from map.models import Place, Sensor, SensorStatus
# Create your views here.


@login_required
def list_rules(request, place):
    place_obj = get_object_or_404(Place, pk=place)
    rules = ScheduleDaily.objects.filter(sensor__floor__place=place)
    return render(request, 'list_rules.html', {'place': place_obj, 'rules': rules})


@login_required
def create_rule(request, place):
    if request.method == 'POST':
        if request.POST['sensor'] and request.POST['status'] and request.POST['begin_time'] and request.POST['end_time']:
            sensor = Sensor.objects.get(pk=request.POST['sensor'])
            status = SensorStatus.objects.get(pk=request.POST['status'])
            rule = ScheduleDaily(sensor=sensor, status=status, begin_time=request.POST['begin_time'], end_time=request.POST['end_time'])
            rule.save()
            return redirect('list_rules', place=place)
    place_obj = get_object_or_404(Place, pk=place)
    sensors = Sensor.objects.filter(floor__place=place_obj)
    statuses = SensorStatus.objects.all()
    return render(request, 'create_rule.html', {'place': place_obj, 'sensors': sensors, 'statuses': statuses})


@login_required
def edit_rule(request, place, rule_pk):
    place_obj = get_object_or_404(Place, pk=place)
    rule = get_object_or_404(ScheduleDaily, pk=rule_pk)
    if request.method == 'POST':
        if request.POST['sensor'] and request.POST['status'] and request.POST['begin_time'] and request.POST['end_time']:
            rule.sensor = Sensor.objects.get(pk=request.POST['sensor'])
            rule.status = SensorStatus.objects.get(pk=request.POST['status'])
            rule.begin_time = request.POST['begin_time']
            rule.end_time = request.POST['end_time']
            rule.save()
            return redirect('list_rules', place=place)
    sensors = Sensor.objects.filter(floor__place=place_obj)
    statuses = SensorStatus.objects.all()
    return render(request, 'create_rule.html', {'place': place_obj, 'sensors': sensors, 'statuses': statuses, 'rule': rule})


@login_required
def delete_rule(request, place, rule_pk):
    rule = get_object_or_404(ScheduleDaily, pk=rule_pk)
    rule.delete()
    return redirect('list_rules', place=place)
