from django.contrib import admin
from detector import models
from .models import *
# Register your models here.
@admin.register(Patients)
class PatientAdmin (admin.ModelAdmin):
    list_display = ['firstname','lastname','gender','email']
