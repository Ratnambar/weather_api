from distutils.log import Log
from re import L
from urllib.parse import urlparse
from django.db import router
from django.urls import include,path
from rest_framework import routers
from account.views import SignupViewSet,LoginView,weather_report
from django.contrib.auth import views as auth_views



router = routers.DefaultRouter()
router.register('signup',SignupViewSet)



urlpatterns = [
    path('',include(router.urls)),
    path('login/',LoginView.as_view(),name='login_view'),
    path('weather/limit/<int:limit>/page/<int:page>/',weather_report,name='waether_report'),
    path('',include('django.contrib.auth.urls'))
]
