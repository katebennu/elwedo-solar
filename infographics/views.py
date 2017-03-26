from django.shortcuts import render
from infographics.models import ConsumptionMeasurement, Building, Apartment, PanelsToInstall
import json
from django.http import JsonResponse


def index(request):


    return render(request, "infographics/index.html")

def timeline_update(request):

    # SECOND_STAGE: replace with apartment / or building associated with ther request's user
    building = Building.objects.first()

    data = building.get_month_data()

    # format timestamp only


    # context_data = {'consumption':[], 'production':[]}
    for i in data['consumption']:
        i['timestamp'] = i['timestamp'].isoformat() + 'Z'
        i['value'] = float(i['value'])
    #
    # for i in data['production']:
    #     i.value = i.value_per_unit * PanelsToInstall.objects.filter(name='default')[0].number_of_units
    #     context_data['production'].append({'timestamp': i.timestamp.isoformat() + 'Z', 'value': float(i.value)})


    return JsonResponse(data)