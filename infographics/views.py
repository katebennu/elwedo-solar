from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from infographics.models import *
from django.contrib.auth.decorators import user_passes_test
from django.utils import translation

import csv
from datetime import datetime


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
    # if request.user.username == '':
    #     user = User.objects.get(username='Petja_user_1')
    # else:

    time_frame = request.GET.get('timeFrame')
    building_on = request.GET.get('buildingOn')

    user = request.user

    from pprint import pprint
    pprint(building_on)

    if building_on == 'true':
        obj = Building.objects.first()
    else:
        obj = user.profile.apartment

    if time_frame == 'month':
        query = obj.get_multiple_days_data(31)
    elif time_frame == 'week':
        query = obj.get_multiple_days_data(8)
    else:
        query = obj.get_day_data()

    km_multiplier = KmMultiplier.objects.get(use=True)
    co2_multiplier = CO2Multiplier.objects.get(use=True)
    grid_multiplier = GridPriceMultiplier.objects.get(apartment=user.profile.apartment)
    solar_multiplier = SolarPriceMultiplier.objects.get(apartment=user.profile.apartment)

    data = list()
    multipliers = {
        'CO2Multiplier': co2_multiplier.multiplier,
        'kmMultiplier': km_multiplier.multiplier,
        'gridMultiplier': grid_multiplier.multiplier,
        'solarMultiplier': solar_multiplier.multiplier
    }

    for i in query:
        row = {}
        data.append(row)
        row['timestamp'] = i['timestamp'].isoformat() + 'Z'
        row['consumption'] = float(i['consumption'])
        row['production'] = float(i['production'])
        row['savings'] = float(i['savings'])
        row['consumptionLessSavings'] = float(i['consumptionLessSavings'])

    return JsonResponse({'multipliers': multipliers, 'data': data}, safe=False)


@user_passes_test(lambda u: u.is_superuser)
def summary(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="summary_' + '_' + datetime.now().strftime(
            "%Y-%m-%d %H:00") + '.csv"'
    writer = csv.writer(response)
    writer.writerow(['Timestamp',
                     'Consumption, kWh',
                     'Production, kWh',
                     'CO2 no-solar, kg', 'CO2 with-solar, kg',
                     'Spent no-solar, EUR', 'Spent with-solar, EUR'])
    building = Building.objects.first()
    apartments = Apartment.objects.all()
    co2 = float(CO2Multiplier.objects.filter(use=True)[0].multiplier)
    eur_grid = float(GridPriceMultiplier.objects.filter(use=True)[0].multiplier)
    eur_sol = float(SolarPriceMultiplier.objects.filter(use=True)[0].multiplier)

    writer.writerow(['***Building***'])
    b_data = building.get_day_data()
    for i in b_data:
        n = i['consumption'] * eur_grid - i['production'] * eur_sol
        if n < 0:
            n = 0
        writer.writerow([
            i['timestamp'].strftime("%Y-%m-%d %H:00"),
            i['consumption'],
            i['production'],
            i['consumption'] * co2,
            i['consumptionLessSavings'] * co2,
            i['consumption'] * eur_grid,
            n
        ])
    for a in apartments:
        writer.writerow(['***Apartment ', a.name + '***'])
        a_data = a.get_day_data()
        for i in a_data:
            n = i['consumption'] * eur_grid - i['production'] * eur_sol
            if n < 0:
                n = 0
            writer.writerow([
                i['timestamp'].strftime("%Y-%m-%d %H:00"),
                i['consumption'],
                i['production'],
                i['consumption'] * co2,
                i['consumptionLessSavings'] * co2,
                i['consumption'] * eur_grid,
                n
            ])

    return response
