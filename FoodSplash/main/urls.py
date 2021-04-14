from django.conf.urls import url
from FoodSplash.settings import DEBUG
from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),


    url(r'^console/$', views.console, name='console'),

    url(r'^staff/$', views.staff, name='staff'),




]

if DEBUG:
    urlpatterns += [
        url(r'^createsuperuser/$', views.createsuperuser),
    ]
