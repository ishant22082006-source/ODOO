from django.contrib import admin
from .models import MaintenanceLog


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):

    list_display = (
        "vehicle",
        "maintenance_type",
        "start_date",
        "end_date",
        "cost",
        "status",
    )

    list_filter = (
        "status",
        "start_date",
    )

    search_fields = (
        "vehicle__registration_number",
        "maintenance_type",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )