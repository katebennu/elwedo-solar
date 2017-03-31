from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render

from infographics.forms import UserForm
from infographics.models import Building, Apartment


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


# @sensitive_post_parameters()
# @csrf_protect
# @never_cache
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is None:
            return render(request, 'infographics/login.html', {'error_message': 'Invalid login'})
        else:
            login(request, user)
            apartment = Apartment.objects.filter(user=request.user)
            return render(request, 'infographics/index.html', {'apartment': apartment})


def login_page(request):
    return render(request, "infographics/login.html")


def logout_user(request):
    logout(request)
    return render(request, 'infographics/login.html', {
        "form": UserForm(request.POST or None),
    })