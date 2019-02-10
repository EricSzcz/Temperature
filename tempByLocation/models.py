from django.db import models

"""
I decided save more information that could be useful in the future to learn more about clients.
"""


class RequestsInfo(models.Model):
    location = models.CharField(max_length=50)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    client_ip = models.CharField(max_length=15)
    dateTime = models.CharField(max_length=50)
    number_access = models.FloatField(default=0)
