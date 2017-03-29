from infographics.models import ConsumptionMeasurement, Building, Apartment, PanelsToInstall
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic import View
from infographics.forms import UserForm
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


def index(request):
    return render(request, "infographics/index.html")


def timeline_update(request):

    building = Building.objects.first()
    apartment = Apartment.objects.filter(user=request.user)[0]

    time_frame = request.GET.get('timeFrame')

    if time_frame == 'month':
        data_building = building.get_multiple_days_data(29)
        data_apartment = apartment.get_multiple_days_data(29)

    if time_frame == 'week':
        data_building = building.get_multiple_days_data(6)
        data_apartment = apartment.get_multiple_days_data(6)

    else:
        data_building = building.get_day_data()
        data_apartment = apartment.get_day_data()

    data = []

# TODO: if possible, rewrite to cut O

    for i in data_building:
        row = {}
        data.append(row)
        row['timestamp'] = i['timestamp'].isoformat() + 'Z'
        row['b_consumption'] = float(i['consumption'])
        row['b_production'] = float(i['production'])
        row['b_savings'] = float(i['savings'])
        row['b_earnings'] = float(i['earnings'])
        for j in data_apartment:
            if i['timestamp'] == j['timestamp']:
                row['a_consumption'] = float(j['consumption'])
                row['a_production'] = float(j['production'])
                row['a_savings'] = float(j['savings'])
                row['a_earnings'] = float(j['earnings'])

    return JsonResponse(data, safe=False)


# @sensitive_post_parameters()
# @csrf_protect
# @never_cache
def login_user(request):
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

def login_page(request):
    return render(request, "infographics/login.html")


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'infographics/login.html', context)