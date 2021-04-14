"""FoodSplash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from . import settings
from . import views


# Main URL patterns and PAGESERVER
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("main.urls"))
]

if settings.PRODUCTION:
    urlpatterns += [
        url(r'^_ah/', include('djangae.urls'))
    ]

# view error pages in development
if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', views.handle404),
        url(r'^403/$', views.handle403),
        url(r'^500/$', views.handle500),
    ]