from django.conf.urls import url, include
from django.contrib.auth.views import login, logout


from . import views

app_name = 'infographics'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),  # default homepage
    url(r'^timeline-update/$', views.timeline_update),
    url(r'^login/$', login, dict(
        template_name='infographics/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    url(r'^logout/$', logout, dict(next_page='/'), name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^.well-known/pki-validation/godaddy.html$', views.cert, name='cert'),
    url(r'^summary/$', views.summary, name='summary')
]


