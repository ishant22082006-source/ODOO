from django.db import models


class Vehicle(models.Model):

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("On Trip", "On Trip"),
        ("In Shop", "In Shop"),
        ("Retired", "Retired"),
    ]

    TYPE_CHOICES = [
        ("Truck", "Truck"),
        ("Van", "Van"),
        ("Bus", "Bus"),
        ("Car", "Car"),
        ("Other", "Other"),
    ]

    registration_number = models.CharField(
        max_length=50,
        unique=True
    )

    vehicle_name = models.CharField(
        max_length=100
    )

    vehicle_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )

    maximum_load_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Maximum load capacity in KG"
    )

    odometer = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Current odometer reading in KM"
    )

    acquisition_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Available"
    )

    region = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.registration_number} - {self.vehicle_name}"