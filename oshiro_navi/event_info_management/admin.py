from django.contrib import admin

from .models import AdminEvent, OperatorEvent

admin.site.register(AdminEvent)

admin.site.register(OperatorEvent)