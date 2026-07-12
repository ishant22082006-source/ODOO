from django.contrib import admin
from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "license_number",
        "license_category",
        "license_expiry_date",
        "contact_number",
        "safety_score",
        "status",
    )

    list_filter = (
        "status",
        "license_category",
        "license_expiry_date",
    )

    search_fields = (
        "name",
        "license_number",
        "contact_number",
    )