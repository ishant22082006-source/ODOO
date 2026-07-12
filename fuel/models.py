from django.db import models
from vehicles.models import Vehicle


class FuelLog(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="fuel_logs"
    )

    date = models.DateField()

    liters = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    odometer = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    remarks = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.date}"