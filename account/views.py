from curses.ascii import US
from xmlrpc.client import ResponseError
from django.shortcuts import render

# Create your views here.
import urllib.request
import json

from django.contrib.auth.models import User
from account.serializers import SignupSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import viewsets,serializers,mixins
from rest_framework.decorators import permission_classes,authentication_classes,api_view
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.renderers import JSONRenderer
from decouple import config

# from rest_framework.renderers import JSONRenderer





class SignupViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    permission_classes = [AllowAny,]
    queryset = User.objects.all()
    serializer_class = SignupSerializer



class LoginView(APIView):
    permission_classes = [AllowAny,]
# @api_view(['POST'])
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(username=serializer.data['username'])
            except BaseException as e:
                raise ValidationError({"message":"user does not exist."})
            if user:
                # print(serializer.data['username'])
                if user.check_password(serializer.data['password']):
                    print(serializer.data['username'])
                    token = Token.objects.get(user=user)
                    # return Response({'message':'login successfull'})
                    return Response({'token':str(token)})
                return Response({"message":"incorrect password."})
            return Response({"message":"User does not exist."})
        return Response({'message':serializer.errors})


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def weather_report(request,limit,page):
    cities = ['Delhi','Lucknow','Varanasi','Kanpur','Noida','Agra','Aligarh','Mumbai','Kolkata','Gurgaon','Surat','Pune','Jaunpur']
    city_dict = {}
    city_list = []
    print(limit,page)
    weather_api_key = config('weather_api_key')
    for city in cities:
        url = "https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}".format(city,weather_api_key)
        response = urllib.request.urlopen(url)
        data = response.read()
        dict = json.loads(data)
        city_dict[city] = dict
        city_list.append(city_dict[city])
    
    for i in range(len(city_list)):
        if i == (int(page)*int(limit))-int(limit):
            city_list = city_list[i:(int(page)*int(limit))]
            return Response({'json_city_llist' :city_list})
    return Response({"error":"some problem has occur."})
