from django.db import models
from vehicles.models import Vehicle


class Expense(models.Model):

    EXPENSE_TYPES = [
        ("Toll", "Toll"),
        ("Maintenance", "Maintenance"),
        ("Parking", "Parking"),
        ("Insurance", "Insurance"),
        ("Other", "Other"),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    expense_type = models.CharField(
        max_length=50,
        choices=EXPENSE_TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    date = models.DateField()

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
        return f"{self.vehicle.registration_number} - {self.expense_type}"