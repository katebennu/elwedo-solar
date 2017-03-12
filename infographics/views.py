from django.shortcuts import render
from infographics.models import ConsumptionMeasurement, Building, Apartment


def index(request):
    context = dict()
    context['data'] = ConsumptionMeasurement.objects.filter(timestamp__year='2016',
                                                            timestamp__month='05',
                                                            timestamp__day='15')

    return render(request, "infographics/index.html", context)
