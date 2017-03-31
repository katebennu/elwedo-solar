from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

app_name = 'infographics'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),  # default homepage
    url(r'^timeline-update/$', views.timeline_update),
    url(r'^login/$', login, {'template_name': 'infographics/login.html'}, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
