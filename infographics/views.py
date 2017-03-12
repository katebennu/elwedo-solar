from django.shortcuts import render
from infographics.models import ConsumptionMeasurement, Building, Apartment


def index(request):
    data = ConsumptionMeasurement.objects.filter(time__year='2016',
                                                 time__month='05')
    return render(request, "infographics/index.html", data)

