from django.shortcuts import render
from infographics.models import ConsumptionMeasurement, Building, Apartment


def index(request):
    context = dict()
    context['data'] = ConsumptionMeasurement.objects.filter(time__year='2016',
                                                 time__month='05',
                                                 time__day='15')

    return render(request, "infographics/index.html", context)

