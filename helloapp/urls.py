"""helloapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
import notifications.urls
from howdy import views
#from howdy.notificate_views import make_readed, notifihome
import notifications.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ola/', include('howdy.urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('ola/owner/printing/', views.printing_department, name='printing_department'),
    path('ola/owner/cutting/', views.cutting_department, name='cutting_department'),
    path('ola/owner/extruder/', views.extruder_department, name='extruder_department'),
    path('api/chart/data/printing/', views.ChartData.as_view()),
    path('api/chart/data/cutting/', views.ChartDataCutting.as_view()),
    path('api/chart/data/extruder/', views.ChartDataExtruder.as_view()),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
#############################################
 #   path('read/<pk>/', make_readed, name='read'),
  #  path('notifications/', notifihome, name='nothome'),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
