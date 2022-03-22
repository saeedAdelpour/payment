from django.contrib import admin

from .models import Person, PersonPayment


class PersonAdmin(admin.ModelAdmin):
    list_display = ["name"]


class PersonPaymentAdmin(admin.ModelAdmin):
    list_display = ["person", "payment", "price", "created_at", "status"]
    list_select_related = ["person", "payment"]


admin.site.register(Person, PersonAdmin)
admin.site.register(PersonPayment, PersonPaymentAdmin)
