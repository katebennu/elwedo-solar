from django.shortcuts import render
from infographics.models import ConsumptionMeasurement, Building, Apartment
import json
from django.http import JsonResponse


def index(request):


    return render(request, "infographics/index.html")

def timeline_update(request):

    # SECOND_STAGE: replace with apartment / or building associated with ther request's user
    building = Building.objects.first()

    data = building.get_day_data()
    context_data = {'consumption':[], 'production':[]}
    for i in data['consumption']:
        context_data['consumption'].append({'timestamp': i.timestamp.isoformat() + 'Z', 'value': float(i.value)})

    for i in data['production']:
        context_data['production'].append({'timestamp': i.timestamp.isoformat() + 'Z', 'value_per_unit': float(i.value_per_unit)})


    return JsonResponse(context_data)