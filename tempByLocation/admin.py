from django.contrib import admin
from .models import RequestsInfo

class RequestsInfoAdmin(admin.ModelAdmin):
    fields = ('location', 'temperature', 'client_ip', 'dateTime', 'number_access')

admin.site.register(RequestsInfo, RequestsInfoAdmin)