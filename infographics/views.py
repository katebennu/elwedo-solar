from django.shortcuts import render
from infographics.models import ConsumptionMeasurement, Building, Apartment
from django.forms.models import model_to_dict


def index(request):
    context = dict()
    context['data'] = ConsumptionMeasurement.objects.filter(time__year='2016',
                                                 time__month='05',
                                                 time__day='15')
    # context = {}
    # for i in data:
    #     instance = model_to_dict(i)
    #     context.update({instance['time']: instance['value']})

    return render(request, "infographics/index.html", context)

