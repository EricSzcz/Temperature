from django.views import View
from django.shortcuts import render
from .models import RequestsInfo
from ipware import get_client_ip
import datetime
import requests

"""
I have created this class based view because you can execute directly method post or get without if statement the check
request, and because the django community are implementing Class based view as standard.
GET: will just return the main page: temperature
POST: will call the function to get location and temperature also will save the client information on database before
      return the temperature of location to client 
"""


class ShowTemperature(View):
    def get(self, request):
        return render(request, 'temperature.html')

    def post(self, request):
        if request.POST['location']:
            temperature = self.get_temperature_from_lat_lng(self.get_lat_lng_from_location(request.POST['location']))
            location_name = self.get_location_name(request.POST['location'])
            info = RequestsInfo.objects.filter(client_ip=self.get_client_ip(request))
            if info:
                info = RequestsInfo.objects.get(client_ip=self.get_client_ip(request))
                info.number_access += 1
                info.location = location_name
                info.save()
            else:
                RequestsInfo.objects.create(
                    location=location_name,
                    number_access=1,
                    temperature=temperature,
                    client_ip=self.get_client_ip(request),
                    dateTime=datetime.datetime.now()
                )
            return render(request, 'temperature.html', {'temperature': temperature, 'location_name': location_name,
                                                        'location': request.POST['location']})
        else:
            return render(request, 'temperature.html')

    """
    The function 'get_client_ip' will get the client IP who made the request.
    I have decided to use ipware package because the function to get the client IP is already implemented on this
    package
    """
    def get_client_ip(self, request):
        ip, is_routable = get_client_ip(request)
        if ip:
            client_ip = ip

        return client_ip

    """
    The function 'get_lat_lng_from_location' will get the informed location and will find the latitude and longitude
    of the place and return it as concatenated string, I did it to return the parameter ready to 'get_temperature_from_lat_lng'
    that will receive this string.
    I also separate the key in a variable to make easy to change in the future
    """
    def get_lat_lng_from_location(self, location):
        key = 'AIzaSyAg6rz9WIBVRKGEo-Zqx9tjDxSTF4Yk6rs'
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (location, key))
        position = r.json()['results'][0]['geometry']['location']
        lat_lng = str(position['lat']) + ',' + str(position['lng'])

        return lat_lng

    """
    The function 'get_temperature_from_lat_lng' will receive the latitude and longitude from 'get_lat_lng_from_location'
    and will return the temperature, the Dark Sky API return the temperature as fahrenheit so I also convert it to
    celsius and return it as integer to remove the decimals character
    as you can see I separate the key again like 'get_lat_lng_from_location' for the same reason
    """
    def get_temperature_from_lat_lng(self, lat_lng):
        key = '96b47f43f97fdc8f03d64785b9816c5f'
        r = requests.get('https://api.darksky.net/forecast/%s/%s' % (key, lat_lng))
        temperature = int(((r.json()['currently']['temperature'] - 32) * 5.0) / 9.0)

        return temperature

    """
    The function 'get_location_name' will return the name of the place requested by the client, I have created this
    function because the client can input zip code or city name so when the client inform zip code the google API return
    a JSON with different format than the city are informed. to return always the name of the city I create this function
    the check if was informed zip code or city name, I could use the function 'get_lat_lng_from_location' to return it
    too but I prefer separate the things to not create a huge function
    """
    def get_location_name(self, location):
        key = 'AIzaSyAg6rz9WIBVRKGEo-Zqx9tjDxSTF4Yk6rs'
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (location, key))
        if location[-3:].isdigit():
            location = r.json()['results'][0]['address_components'][2]['long_name']
        else:
            location = r.json()['results'][0]['address_components'][0]['long_name']

        return location
