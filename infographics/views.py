from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from infographics.models import *
from django.contrib.auth.decorators import user_passes_test
from django.utils import translation

import csv
from datetime import datetime,timedelta


def cert(request):
    return render(request, "infographics/godaddy.html")


@login_required
def index(request):
    return render(request, "infographics/index.html")


def about(request):
    return render(request, "infographics/about.html")


@login_required
def timeline_update(request):
    # if request.user.username == '':
    #     user = User.objects.get(username='Petja_user_1')
    # else:

    from pprint import pprint

    time_frame = request.GET.get('timeFrame')
    building_on = request.GET.get('buildingOn')
    car = request.GET.get('eCarOn')
    if car == 'true':
        car = True
    else:
        car = False

    user = request.user


    if building_on == 'true':
        obj = Building.objects.get(pk=1)
    else:
        obj = user.profile.apartment

    if time_frame == 'month':
        if building_on == 'true':
            query = obj.get_multiple_days_data(30, car)
        else:
            query = obj.get_multiple_days_data(13, car)

        # pprint(original)

        # stamps = [original[-1]['timestamp']]
        # for i in range(18):
        #     stamps.append(stamps[-1] - timedelta(days=1))
        # stamps.pop(0)
        # pprint(stamps)
        #
        #
        # # project the pattern into the past
        # addition = original + original[:7]
        #
        #
        # for i in range(len(addition)-1):
        #     addition[i]['timestamp'] = stamps[i]
        #     pprint(addition[i]['timestamp'])
        #
        # # query = original + addition
        # pprint(addition)
        #
        # query = original + addition
        # for i in query[1:31]:
        #     i['timestamp'] = i['timestamp'] - timedelta(days=1)
        # query = query[::-1]


    elif time_frame == 'week':
        query = obj.get_multiple_days_data(8, car)
    else:
        query = obj.get_day_data(car)

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
        time = i['timestamp'] + timedelta(hours=3)
        row['timestamp'] = time.isoformat() + 'Z'
        row['consumption'] = float(i['consumption'])
        row['production'] = float(i['production'])
        row['savings'] = float(i['savings'])
        row['consumptionLessSavings'] = float(i['consumptionLessSavings'])
    pprint(data)
    return JsonResponse({'multipliers': multipliers, 'data': data}, safe=False)


def makerow(i, co2, eur_grid, eur_sol):
    return [
        (i['timestamp'] + timedelta(hours=3)).strftime("%Y-%m-%d %H:00"),
        i['consumption'],
        i['production'],
        i['savings'],
        i['consumptionLessSavings'],
        i['consumption'] * co2,
        i['consumptionLessSavings'] * co2,
        i['consumption'] * eur_grid,
        (i['consumption'] - i['savings']) * eur_grid + i['savings'] * eur_sol
    ]


@user_passes_test(lambda u: u.is_superuser)
def summary(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="summary_' + '_' + (datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%d %H:00") + '.csv"'
    writer = csv.writer(response)
    writer.writerow(['Timestamp',
                     'Consumption, kWh',
                     'Production, kWh',
                     'Savings, kWh',
                     'Consumption Less Savings, kW',
                     'CO2 no-solar, kg', 'CO2 with-solar, kg',
                     'Spent no-solar, EUR', 'Spent with-solar, EUR'])
    building = Building.objects.get(pk=1)
    apartments = Apartment.objects.all()[:2]
    co2 = float(CO2Multiplier.objects.filter(use=True)[0].multiplier)
    eur_grid = float(GridPriceMultiplier.objects.filter(use=True)[0].multiplier)
    eur_sol = float(SolarPriceMultiplier.objects.filter(use=True)[0].multiplier)

    writer.writerow(['*******Building*******'])
    writer.writerow(['***Day***'])
    b_day = building.get_day_data()
    for i in b_day:
        writer.writerow(makerow(i, co2, eur_grid, eur_sol))

    writer.writerow(['***Week***'])
    b_week = building.get_multiple_days_data(8)
    for i in b_week:
        writer.writerow(makerow(i, co2, eur_grid, eur_sol))

    for a in apartments:
        writer.writerow(['*******Apartment ', a.name + '*******'])
        writer.writerow(['***Day***'])
        a_day = a.get_day_data()
        for i in a_day:
            writer.writerow(makerow(i, co2, eur_grid, eur_sol))
        writer.writerow(['***Week***'])
        a_week = a.get_multiple_days_data(8)
        for i in a_week:
            writer.writerow(makerow(i, co2, eur_grid, eur_sol))
    return response
