from django.shortcuts import render
from infographics.models import ConsumptionMeasurement, Building, Apartment


def index(request):

    data = ConsumptionMeasurement.objects.filter(timestamp__year='2016',
                                                 timestamp__month='05',
                                                 timestamp__day='15')
    context = dict()
    context_data = []

    for i in data:
        context_data.append({'timestamp': i.timestamp.isoformat() + 'Z', 'value': i.value })

    context['context_data'] = context_data

    return render(request, "infographics/index.html", context)
