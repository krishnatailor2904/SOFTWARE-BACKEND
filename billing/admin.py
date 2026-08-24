from django.contrib import admin
from .models import Bill, Measurement

admin.site.register(Bill)
admin.site.register(Measurement)
