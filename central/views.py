from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Permission
from map.models import Neighborhood
from models import File

def user_can_see(user):
    return user.is_superuser or user.groups.filter(name='UsersCentral').exists()

@login_required
@user_passes_test(user_can_see, login_url='/map/')
def central_home(request):
    context = {'user': request.user}
    return render(request, 'central_home.html', context)

@login_required
def central_create(request):
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
    # if request.method == 'POST':
    #     form = UploadForm(request.POST, request.FILES)
    #     if form.is_valid():
    #     	newdoc = File(filename = request.POST['filename'],docfile = request.FILES['docfile'])
    #     	newdoc.save(form)
    #     	return redirect("uploads")
    # else:
    #     form = UploadForm()
    context = {'user': request.user}
    return render(request, 'owner_huge_load.html', context)
