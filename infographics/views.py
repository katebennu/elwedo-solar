from django.contrib.auth import logout as do_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from infographics.models import Building, Apartment


@login_required
def index(request):
    return render(request, "infographics/index.html")


def timeline_update(request):

    building = Building.objects.first()
    apartment = Apartment.objects.filter(user=request.user)[0]

    time_frame = request.GET.get('timeFrame')

    if time_frame == 'month':
        data_building = building.get_multiple_days_data(29)
        data_apartment = apartment.get_multiple_days_data(29)

    elif time_frame == 'week':
        data_building = building.get_multiple_days_data(6)
        data_apartment = apartment.get_multiple_days_data(6)

    else:
        data_building = building.get_day_data()
        data_apartment = apartment.get_day_data()

    data = []

# TODO: if possible, rewrite to cut O

# Possibly repack as two dictionaries: building and apartment if easier to implement the B/A switch

    for i in data_building:
        row = {}
        data.append(row)
        row['timestamp'] = i['timestamp'].isoformat() + 'Z'
        row['b_consumption'] = float(i['consumption'])
        row['b_production'] = float(i['production'])
        row['b_savings'] = float(i['savings'])
        row['b_earnings'] = float(i['earnings'])
        row['b_consumptionLessSavings'] = float(i['consumptionLessSavings'])
        for j in data_apartment:
            if i['timestamp'] == j['timestamp']:
                row['a_consumption'] = float(j['consumption'])
                row['a_production'] = float(j['production'])
                row['a_savings'] = float(j['savings'])
                row['a_earnings'] = float(j['earnings'])
                row['a_consumptionLessSavings'] = float(j['consumptionLessSavings'])

    return JsonResponse(data, safe=False)


def logout(request):
    do_logout(request)
    return redirect("index")
