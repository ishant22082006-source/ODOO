from django.db import models
from vehicles.models import Vehicle


class MaintenanceLog(models.Model):

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Completed", "Completed"),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="maintenance_logs"
    )

    maintenance_type = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
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
        return f"{self.vehicle.registration_number} - {self.maintenance_type}"