from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from infographics.models import *
from django.contrib.auth.models import User
from django.utils import translation


def cert(request):
    return render(request, "infographics/godaddy.html")

@login_required
def index(request):
    user_language = 'fi'
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return render(request, "infographics/index.html")


def about(request):
    user_language = 'fi'
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return render(request, "infographics/about.html")


@login_required
def timeline_update(request):
    from pprint import pprint
    pprint(request.user)
    # if request.user.username == '':
    #     user = User.objects.get(username='Petja_user_1')
    # else:
    user = request.user
    building = Building.objects.first()
    apartment = user.profile.apartment

    time_frame = request.GET.get('timeFrame')

    if time_frame == 'month':
        data_building = building.get_multiple_days_data(31)
        data_apartment = apartment.get_multiple_days_data(31)

    elif time_frame == 'week':
        data_building = building.get_multiple_days_data(8)
        data_apartment = apartment.get_multiple_days_data(8)

    else:
        data_building = building.get_day_data()
        data_apartment = apartment.get_day_data()

    km_multiplier = KmMultiplier.objects.get(use=True)
    co2_multiplier = CO2Multiplier.objects.get(use=True)
    grid_multiplier = GridPriceMultiplier.objects.get(apartment=apartment)
    solar_multiplier = SolarPriceMultiplier.objects.get(apartment=apartment)

    data = list()
    multipliers = {
        'CO2Multiplier': co2_multiplier.multiplier,
        'kmMultiplier': km_multiplier.multiplier,
        'gridMultiplier': grid_multiplier.multiplier,
        'solarMultiplier': solar_multiplier.multiplier
    }

    for i in data_building:
        row = {}
        data.append(row)
        row['timestamp'] = i['timestamp'].isoformat() + 'Z'
        row['b_consumption'] = float(i['consumption'])
        row['b_production'] = float(i['production'])
        row['b_savings'] = float(i['savings'])
        row['b_consumptionLessSavings'] = float(i['consumptionLessSavings'])
        for j in data_apartment:
            if i['timestamp'] == j['timestamp']:
                row['a_consumption'] = float(j['consumption'])
                row['a_production'] = float(j['production'])
                row['a_savings'] = float(j['savings'])
                row['a_consumptionLessSavings'] = float(j['consumptionLessSavings'])

    return JsonResponse({'multipliers': multipliers, 'data': data}, safe=False)
