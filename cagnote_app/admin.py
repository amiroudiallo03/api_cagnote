from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Academician)
class AcademicianAdmin(admin.ModelAdmin):
    list_display = ["last_name",'first_name','register_number','picture']


@admin.register(models.Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['academician','reason','montant', 'payment_date', 'reason']
