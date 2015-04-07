from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from map.models import Neighborhood

def user_can_see(user):
    return user.is_superuser or user.groups.filter(name='UsersCentral').exists()

@login_required
@user_passes_test(user_can_see, login_url='/map/')
def central_home(request):
    context = {'user': request.user}
    return render(request, 'central_home.html', context)


def central_create(request):
    neighborhood = Neighborhood.objects.all().order_by('name')
    print 'hola2'
    context = {'user': request.user, 'neighborhood': neighborhood}
    return render(request, 'central_create.html', context)


def central_owner_principal(request):
    context = {'user': request.user}
    return render(request, 'owner_principal.html', context)


def central_individual_load(request):
    context = {'user': request.user}
    return render(request, 'owner_individual_load.html', context)


def central_huge_load(request):
    context = {'user': request.user}
    return render(request, 'owner_huge_load.html', context)
