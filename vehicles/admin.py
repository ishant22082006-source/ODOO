from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "registration_number",
        "vehicle_name",
        "vehicle_type",
        "maximum_load_capacity",
        "odometer",
        "status",
        "region",
    )

    list_filter = (
        "status",
        "vehicle_type",
        "region",
    )

    search_fields = (
        "registration_number",
        "vehicle_name",
        "region",
    )