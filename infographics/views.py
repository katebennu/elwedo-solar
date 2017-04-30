from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from infographics.models import Building, Apartment\
    # , KmMultiplier, CO2Multiplier, EurMultiplier
from django.contrib.auth.models import User


@login_required
def index(request):
    return render(request, "infographics/index.html")


def about(request):
    return render(request, "infographics/about.html")

@login_required
def timeline_update(request):
    from pprint import pprint
    pprint(request.user)
    if request.user.username == '':
        user = User.objects.get(username='user_5')
    else:
        user = request.user
    building = Building.objects.first()
    apartment = Apartment.objects.get(user=user)

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

    # km_multiplier = KmMultiplier.objects.filter(use=True)
    # co2_multiplier = CO2Multiplier.objects.filter(use=True)
    # eur_multiplier = EurMultiplier.objects.filter(apartment=apartment)

    data = []
    # data.append({'CO2Multiplier': co2_multiplier, 'eurMultiplier': eur_multiplier, 'co2Multiplier': co2_multiplier})

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


    return JsonResponse(data, safe=False)
