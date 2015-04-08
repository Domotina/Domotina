from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Permission
from map.models import Neighborhood
from models import File
import sys
import os
import csv
from django.conf import settings

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
        print 'aqui'
        savedNeighborhood = request.POST.get("neighborhood", "")
        savedBuilder = request.POST.get("builder", "")
        savedPlaceName = request.POST.get("placeName", "")
        savedPlace = request.POST.get("place", "")
        savedNumTowers= request.POST.get("numTowers", "")
        savedNumFloors= request.POST.get("numFloors", "")
        savedNumApartments = request.POST.get("numApartments", "")
        savedUrlApto= request.POST.get("urlApto", "")
        savedNumBlocks = request.POST.get("numBlocks", "")
        savedNumFloorsHouse= request.POST.get("numFloorsHouse", "")
        savedNumHouses = request.POST.get("numHouses", "")
        savedUrlHouses1= request.POST.get("urlHouses1", "")
        savedUrlHouses2= request.POST.get("urlHouses2", "")
        print savedNeighborhood
        print 'place'
        print savedPlace
        if savedPlace == '1':
            print 'if 1'
        elif savedPlace == '2':
            print 'if 2'
        elif savedPlace == '3':
            print 'if 3'
        context = {'user': request.user}
        return render(request, 'central_create.html', context)
    else:
        print 'aqui2'
        userbuilder = User.objects.all()
        neighborhood = Neighborhood.objects.all().order_by('name')
        context = {'user': request.user, 'neighborhood': neighborhood, 'userbuilder': userbuilder}
        return render(request, 'central_create.html', context)

@login_required
def central_owner_principal(request):
    context = {'user': request.user}
    return render(request, 'owner_principal.html', context)

@login_required
def central_individual_load(request):
    if 'username' in request.GET and request.GET['username'] and 'name' in request.GET and request.GET['name'] and 'lastname' in request.GET and request.GET['lastname'] and 'email' in request.GET and request.GET['email'] and 'pass' in request.GET and request.GET['pass']:
        userC = User.objects.create_user(username=request.GET['username'], first_name=request.GET['name'], last_name=request.GET['lastname'], email=request.GET['email'], password=request.GET['pass'])
        userC.is_superuser = False
        userC.is_active = True
        userC.is_staff = False
        userC.groups.add(2)
        userC.save()
        context = {'create': True, 'userC': userC}
        return render(request, 'owner_individual_load.html', context)
    else:
        context = {'create': False}
        return render(request, 'owner_individual_load.html', context)

    context = {'user': request.user}
    return render(request, 'owner_individual_load.html', context)

@login_required
def central_huge_load(request):
    print request.POST
    if request.method == 'POST':
        file = File(filename = request.POST['filename'], docfile = request.FILES['file'])
        file.save()
        csv_filepathname = "C:/files/files/file.csv"
        sys.path.append(settings.BASE_DIR)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        dataReader = csv.reader(open(csv_filepathname), delimiter=',')
        for row in dataReader:
            csvFile = User.objects.create_user(username=row[0], first_name=row[1], last_name=row[2], email=row[3], password=row[4])
            csvFile.is_superuser = False
            csvFile.is_active = True
            csvFile.is_staff = False
            csvFile.groups.add(2)
            csvFile.save()
        return redirect('central_owner_principal')
    context = {'user': request.user}
    return render(request, 'owner_huge_load.html', context)