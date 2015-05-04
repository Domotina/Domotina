from django.core import serializers
import cgi
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from middleware.http import Http403
from .notificator import send_email
from map.models import Neighborhood, Place, Floor, Delegate
from rule_engine.models import ScheduleDaily
from django.contrib.messages import error
from django.shortcuts import render_to_response
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import StreamingHttpResponse, HttpResponse
from report_manager import central_report_gen
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template import RequestContext
from django.template.loader import render_to_string
from report_manager.views import fetch_resources

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
                floor = Floor(place=place, number=(j + 1), map=map_url)
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


@login_required
def central_individual_delegate_load(request):
    if request.method == "POST":
        username = str(request.POST.get("username", ""))
        name = str(request.POST.get("name", ""))
        lastName = str(request.POST.get("lastName", ""))
        emailUser = str(request.POST.get("inputEmail", ""))
        owner = str(request.POST.get("owner", ""))
        property = int(request.POST.get("property", ""))
        choices = request.POST.getlist('choice')

        userCreate = User.objects.create_user(username=username, first_name=name, last_name=lastName, email=emailUser,
                                              password='DOMOTINA123')
        userCreate.is_superuser = False
        userCreate.is_active = True
        userCreate.is_staff = False
        userCreate.groups.add(4)
        send_email(userCreate)

        content_type = ContentType.objects.get_for_model(Place)
        for permi in choices:
            if permi=='viewMap':
                permission = Permission.objects.get(content_type=content_type, codename='add_place')
                userCreate.user_permissions.add(permission)
            elif permi=='viewRules':
                permission = Permission.objects.get(content_type=ContentType.objects.get_for_model(ScheduleDaily), codename='add_scheduledaily')
                userCreate.user_permissions.add(permission)

        userCreate.save()

        delegate = Delegate(place=Place.objects.get(pk=property), delegate=userCreate)
        delegate.save()

        return redirect('central_home')
    else:
        users = User.objects.all()
        context = {'user': request.user, 'users': users}
        return render(request, 'delegates_individual.html', context)


def getHouses(request):
    owner_id = request.GET['owner_id']
    usersearch = User.objects.get(pk=int(owner_id))
    placeOwner = Place.objects.all().filter(owner=usersearch)
    data = serializers.serialize('json', placeOwner)
    return HttpResponse(data, content_type="application/json")

@login_required
def delegateoption(request, place_pk):

    if request.user.is_superuser == False:
        if request.user.groups.filter(name='UsersOwners').exists() == False:
            raise Http403

    place = get_object_or_404(Place, pk=place_pk)
    placesDelegate = Delegate.objects.all().filter(place=place)

    placeSend = Place.objects.get(pk=place_pk)
    onlyUsername = []
    for item in placesDelegate:
        onlyUsername.append(item.getDelegate())
        print onlyUsername
    print placeSend.pk
    context = {'users': onlyUsername, 'place': placeSend}
    return render(request, 'delegateoption.html', context)

@login_required
def editdelegate(request, place_pk, user_pk):
    """
    if request.user.is_superuser == False:
        if request.user.groups.filter(name='UsersOwners').exists() == False:
            raise Http403
    """
    userEdit = User.objects.get(pk= user_pk)

    place = get_object_or_404(Place, pk=place_pk)
    #user = User.objects.filter(pk=user_pk)
    placesDelegate = Delegate.objects.all().filter(place=place)

    onlyUsername = []
    for item in placesDelegate:
        onlyUsername.append(item.getDelegate())
        #print onlyUsername

    permitions = []
    if request.method == "POST":
        choices = request.POST.getlist('choice')
        print choices

        #userEdit = User.objects.get(pk = user_pk)
        print userEdit
        userEdit.user_permissions.clear()

        if 'viewMap' in choices:
            permissionPlace = Permission.objects.get(content_type=ContentType.objects.get_for_model(Place), codename='add_place')
            #permitionsSelect.append(permissionPlace)
            userEdit.user_permissions.add(permissionPlace)
        else:
            permissionPlace1 = Permission.objects.get(content_type=ContentType.objects.get_for_model(Place), codename='add_place')
            userEdit.user_permissions.remove(permissionPlace1)

        if 'viewRules' in choices:
            permission = Permission.objects.get(content_type=ContentType.objects.get_for_model(ScheduleDaily), codename='add_scheduledaily')
            #permitionsSelect.append(permission)
            userEdit.user_permissions.add(permission)
            #userEdit.save()
        else:
            permission1 = Permission.objects.get(content_type=ContentType.objects.get_for_model(ScheduleDaily), codename='add_scheduledaily')
            #permitionsSelect.append(permission)
            userEdit.user_permissions.remove(permission1)
            #userEdit.save()
        userEdit.save()


        context = {'users': onlyUsername, 'place': place, 'user': userEdit, 'permitions': permitions}
        return render(request, 'delegateoption.html', context)


    if userEdit.has_perm('map.add_place') == True:
        permitions.append('viewMap')
    if userEdit.has_perm('rule_engine.add_scheduledaily') == True:
        permitions.append('viewRules')

    print userEdit
    context = {'users': onlyUsername, 'place': place, 'user': userEdit, 'permitions': permitions}
    return render(request, 'edit_delegate.html', context)

@login_required
def central_huge_delegate_load(request):
    context = {'user': request.user}
    return render(request, 'delegates_huge_load.html', context)


@login_required
def central_building_neigh(request):
    urbanization = Neighborhood.objects.all().filter(type_neighborhood="U")
    buildings = Neighborhood.objects.all().filter(type_neighborhood="B")
    urbanization2 = Place.objects.all().filter(neighborhood=urbanization)
    buildings2 = Place.objects.all().filter(neighborhood=buildings)

    context = {'user': request.user, 'urbanizations': urbanization2, 'buildings': buildings2}
    return render(request, 'central_buildings_list.html', context)


@login_required
def central_building_create(request):
    if request.method == 'POST':
        name = str(request.POST.get("name", ""))
        type = str(request.POST.get("type", "0"))
        neighborhood = Neighborhood(name=name, type_neighborhood=type)
        neighborhood.save()
        return render(request, 'central_home.html')
    context = {'user': request.user}
    return render(request, 'central_buildings_create.html', context)


@login_required
def central_month_report(request):
    neighborhoods = central_report_gen.get_neighborhood
    context = {'user': request.user, 'neighborhoods': neighborhoods}
    return render(request, 'central_month_report.html', context)


@login_required
def generate_monthly_report(request):
    year = int(request.POST['year'])
    month = int(request.POST['month'])
    neighborhoods = request.POST.getlist('neighborhood')
    if neighborhoods[0] in '0':
        neighborhoods = []

    if central_report_gen.validation_entry(year, month):
        start_date = central_report_gen.get_start_date(year, month)
        end_date = central_report_gen.get_end_date(year, month)
        events = central_report_gen.find_events(start_date, end_date, neighborhoods)
        if central_report_gen.are_events_to_report(events):
            html = render_to_string('report.html',
                                    {'pagesize': 'A4', 'events': events, 'start': start_date, 'end': end_date, 'year': year,
                                     'month': month}, context_instance=RequestContext(request))
            result = StringIO.StringIO()
            pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, link_callback=fetch_resources)
            if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
            return HttpResponse('PDF document cannot be generated: %s' % cgi.escape(html))
        else:
            error(request, "No events to generate report.")
            return redirect('central_month_report')
    else:
        error(request, "Error: Please, check if you selected correctly the month, year and buildings/urbanizations of interest to you.")
        return redirect('central_month_report')

# Metodos para Administracion de urbanizaciones y/o edificios

# @login_required
def list_neighborhoods(request):
    # TO-DO
    # Modificar, solo valido para las pruebas iniciales

    # Deberia retrnar un query set
    neighborhoods = []
    n1 = Neighborhood(name="name1")
    n2 = Neighborhood(name="name1")
    neighborhoods.append(n1)
    neighborhoods.append(n2)
    return render(request, 'neighborhood.html', {'neighborhoods': neighborhoods})


# @login_required
def create_neighborhood(request):
    # TO-DO, implementacion temporal valida solo para las pruebas iniciales
    # print(request)
    print(request.POST['name'])
    # Render temporal, solo importa el context
    return render(request, 'neighborhood.html', {'created': True})


# @login_required
def delete_neighborhood(request, neighborhood_pk):
    # TO-DO, implementacion temporal valida solo para las pruebas iniciales
    # print(request)
    print(neighborhood_pk)
    # Render temporal, solo importa el context
    return render(request, 'neighborhood.html', {'deleted': True})


# @login_required
def edit_neighborhood(request, neighborhood_pk):
    neighborhood = get_object_or_404(Neighborhood, pk=neighborhood_pk)
    return render(request, 'neighborhood.html', {'edited': True, 'neighborhood': neighborhood})

