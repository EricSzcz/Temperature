from django.urls import path
from .views import ShowTemperature

urlpatterns = [
    path('', ShowTemperature.as_view(), name="show-temperature"),
]