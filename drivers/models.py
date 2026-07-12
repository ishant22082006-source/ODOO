from django.db import models
from django.utils import timezone


class Driver(models.Model):

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("On Trip", "On Trip"),
        ("Off Duty", "Off Duty"),
        ("Suspended", "Suspended"),
    ]

    LICENSE_CATEGORY_CHOICES = [
        ("LMV", "LMV"),
        ("HMV", "HMV"),
        ("HGMV", "HGMV"),
        ("Transport", "Transport"),
        ("Other", "Other"),
    ]

    name = models.CharField(
        max_length=100
    )

    license_number = models.CharField(
        max_length=50,
        unique=True
    )

    license_category = models.CharField(
        max_length=50,
        choices=LICENSE_CATEGORY_CHOICES
    )

    license_expiry_date = models.DateField()

    contact_number = models.CharField(
        max_length=15
    )

    safety_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Available"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def is_license_expired(self):
        return self.license_expiry_date < timezone.localdate()

    def __str__(self):
        return f"{self.name} - {self.license_number}"