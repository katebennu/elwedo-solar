from django.conf.urls import url
from . import views

app_name = 'infographics'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),  # default homepage
    url(r'^timeline-update/$', views.timeline_update),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
]
