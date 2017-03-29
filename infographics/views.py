from infographics.models import ConsumptionMeasurement, Building, Apartment, PanelsToInstall
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from infographics.forms import UserForm
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


def index(request):
    return render(request, "infographics/index.html")


def timeline_update(request):

    # SECOND_STAGE: replace with apartment / or building associated with their request's user
    building = Building.objects.first()

    data = building.get_day_data()

    time_frame = request.GET.get('timeFrame')

    if time_frame == 'month':
        data = building.get_multiple_days_data(29)

    if time_frame == 'week':
        data = building.get_multiple_days_data(6)

    if time_frame == 'day':
        data = building.get_day_data()

    for i in data:
        i['timestamp'] = i['timestamp'].isoformat() + 'Z'
        i['consumption'] = float(i['consumption'])
        i['production'] = float(i['production'])
        i['savings'] = float(i['savings'])
        i['earnings'] = float(i['earnings'])

    return JsonResponse(data, safe=False)


# @sensitive_post_parameters()
# @csrf_protect
# @never_cache
def login(request):
    """ Wrapper view for built in login
    Prevent legitimate users from logging in before verifying their email
    address. Otherwise, forward request to default login.
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            apartment = Apartment.objects.filter(user=request.user)
            return render(request, 'infographics/index.html', {'apartment': apartment})

        else:
            return render(request, 'infographics/login.html', {'error_message': 'Invalid login'})