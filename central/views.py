from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .notificator import send_email
from map.models import Neighborhood, Place, Floor
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import StreamingHttpResponse,HttpResponse

def user_can_see(user):
    return user.is_superuser or user.groups.filter(name='UsersCentral').exists()


@login_required
@user_passes_test(user_can_see, login_url='/map/')
def central_home(request):
    context = {'user': request.user}
    return render(request, 'central_home.html', context)


@login_required
def central_create(request):
    if request.method == "POST":
        neigh_unicode = request.POST.get("neighborhood", "")
        neighborhood = get_object_or_404(Neighborhood, pk=neigh_unicode)
        name = str(request.POST.get("name", ""))
        floors = int(request.POST.get("floors", "0"))
        places = int(request.POST.get("places", "0"))
        map_url = str(request.POST.get("map", ""))

        for _ in range(places):
            place = Place(owner=request.user, neighborhood=neighborhood, name=name)
            place.save()
            for j in range(floors):
                floor = Floor(place=place, number=(j+1), map=map_url)
                floor.save()
        return redirect('central_home')
    else:
        neighborhoods = Neighborhood.objects.all().order_by('name')
        context = {'neighborhoods': neighborhoods}
        return render(request, 'central_create.html', context)


@login_required
def central_owner_principal(request):
    context = {'user': request.user}
    return render(request, 'owner_principal.html', context)


@login_required
def central_individual_load(request):
    if request.GET.get('username') \
            and request.GET.get('name') \
            and request.GET.get('lastname') \
            and request.GET.get('email'):
        userC = User.objects.create_user(username=request.GET['username'], first_name=request.GET['name'],
                                         last_name=request.GET['lastname'], email=request.GET['email'],
                                         password='DOMOTINA123')
        userC.is_superuser = False
        userC.is_active = True
        userC.is_staff = False
        userC.groups.add(2)
        userC.save()
        send_email(userC)
        context = {'create': True, 'userC': userC}
        return render(request, 'owner_individual_load.html', context)
    else:
        context = {'create': False}
        return render(request, 'owner_individual_load.html', context)

    context = {'user': request.user}
    return render(request, 'owner_individual_load.html', context)


@login_required
def central_huge_load(request):
    if request.method == 'POST':
        file = request.FILES['file']
        for row in file:
            data = row.split(',')
            user = User.objects.create_user(username=data[0], first_name=data[1], last_name=data[2], email=data[3],
                                            password='DOMOTINA123')
            user.is_superuser = False
            user.is_active = True
            user.is_staff = False
            user.groups.add(2)
            user.save()
            send_email(user)
        return redirect('central_owner_principal')
    context = {'user': request.user}
    return render(request, 'owner_huge_load.html', context)



@login_required
def central_delegate(request):
    context = {'user': request.user}
    return render(request, 'delegates_owner_principal.html', context)

#completar
@login_required
def central_individual_delegate_load(request):
    if request.method == "POST":
        username = str(request.POST.get("username", ""))
        name = str(request.POST.get("name", ""))
        lastName = str(request.POST.get("lastName", ""))
        emailUser = str(request.POST.get("inputEmail", ""))
        owner = str(request.POST.get("owner", ""))
        property = str(request.POST.get("property", ""))
        print owner
        print property

        # userCreate = User.objects.create_user(username=username, first_name=name, last_name=lastName, email=emailUser,
        #                                     password='DOMOTINA123')
        # userCreate.is_superuser = False
        # userCreate.is_active = True
        # userCreate.is_staff = False
        # userCreate.groups.add(4)
        # userCreate.save()
        # send_email(userCreate)
        return redirect('central_home')
    else:
        users = User.objects.all()
        #place = Place.objects.all().order_by('name')
        context = {'user': request.user, 'users': users}
        return render(request, 'delegates_individual.html', context)

def getHouses(request):
    owner_id = request.GET['owner_id']
    usersearch = User.objects.get(pk=int(owner_id))
    placeOwner = Place.objects.all().filter(owner=usersearch)
    data = serializers.serialize('json', placeOwner)
    return HttpResponse(data, content_type="application/json")

@login_required
def central_huge_delegate_load(request):
    context = {'user': request.user}
    return render(request, 'delegates_huge_load.html', context)

@login_required
def central_building_neigh(request):
    context = {'user': request.user}
    return render(request, 'central_buildings_list.html', context)


@login_required
def central_building_create(request):
    context = {'user': request.user}
    return render(request, 'central_buildings_create.html', context)


@login_required
def central_month_report(request):
    context = {'user': request.user}
    return render(request, 'central_month_report.html', context)
