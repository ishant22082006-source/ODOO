from django.core.exceptions import ValidationError
from django.db import models

from vehicles.models import Vehicle
from drivers.models import Driver


class Trip(models.Model):

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Dispatched", "Dispatched"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    source = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="trips"
    )

    driver = models.ForeignKey(
        Driver,
        on_delete=models.PROTECT,
        related_name="trips"
    )

    cargo_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Cargo weight in KG"
    )

    planned_distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Planned distance in KM"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Draft"
    )

    final_odometer = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.cargo_weight > self.vehicle.maximum_load_capacity:
            raise ValidationError(
                "Cargo weight cannot exceed vehicle maximum load capacity."
            )

        if self.status in ["Draft", "Dispatched"]:
            if self.vehicle.status in ["In Shop", "Retired"]:
                raise ValidationError(
                    "In Shop or Retired vehicles cannot be assigned to a trip."
                )

            if self.driver.status == "Suspended":
                raise ValidationError(
                    "Suspended drivers cannot be assigned to a trip."
                )

            if self.driver.is_license_expired:
                raise ValidationError(
                    "Driver license has expired."
                )

    def __str__(self):
        return f"{self.source} → {self.destination}"