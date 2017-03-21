from django.shortcuts import render
from infographics.models import ConsumptionMeasurement, Building, Apartment
import json
from django.http import JsonResponse


def index(request):


    return render(request, "infographics/index.html")

def timeline_update(request):
    data = request.

    for i in data:
        context_data.append({'timestamp': i.timestamp.isoformat() + 'Z', 'value': float(i.value)})

    context['context_data'] = context_data
    return JsonResponse(context)