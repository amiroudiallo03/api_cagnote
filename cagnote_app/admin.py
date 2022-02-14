from django.contrib import admin
from . import models
from django.utils.html import mark_safe

# Register your models here.


@admin.register(models.Academician)
class AcademicianAdmin(admin.ModelAdmin):
    list_display = [
        # "photo",
        "last_name", 
        "first_name", 
        "register_number",
        "overall_payment"
        ]
    list_display_links = ['last_name', 'first_name']
    
    def photo(self, obj):
        return mark_safe(
            f"<img src={obj.picture.url} style=width:100px; height:100px>"
        )


@admin.register(models.Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["academician", "reason", "montant", "payment_date"]
