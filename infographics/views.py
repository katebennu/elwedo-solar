from django.shortcuts import render
from infographics.models import ConsumptionMeasurement, Building, Apartment, PanelsToInstall
import json
from django.http import JsonResponse


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