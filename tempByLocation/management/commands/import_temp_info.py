from django.core.management.base import BaseCommand
from django.core import serializers
from ...models import RequestsInfo

"""
The command import_temp_info will return a JSON with all information about clients requests from database
to run it you just need to type: python manage.py import_temp_info
"""


class Command(BaseCommand):
    help = 'Show temperature requests info'

    def handle(self, *args, **kwargs):
        qs = RequestsInfo.objects.all()
        info = serializers.serialize('json', qs)
        return info
