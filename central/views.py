from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required

def user_can_see(user):
    return user.is_superuser or user.groups.filter(name='UsersCentral').exists()

@login_required
#@user_passes_test(user_can_see)
#@permission_required('auth.change_logentry')
@user_passes_test(user_can_see, login_url='/map/')
def central_home(request):
    context = {'user': request.user}
    return render(request, 'central_home.html', context)

def central_create(request):
    context = {'user': request.user}
    return render(request, 'central_create.html', context)
