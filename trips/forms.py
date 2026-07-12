from django import forms
from django.utils import timezone

from .models import Trip
from vehicles.models import Vehicle
from drivers.models import Driver


class TripForm(forms.ModelForm):

    class Meta:
        model = Trip
        fields = [
            "source",
            "destination",
            "vehicle",
            "driver",
            "cargo_weight",
            "planned_distance",
        ]

        widgets = {
            "source": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter source location",
                }
            ),
            "destination": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter destination location",
                }
            ),
            "vehicle": forms.Select(
                attrs={"class": "form-select"}
            ),
            "driver": forms.Select(
                attrs={"class": "form-select"}
            ),
            "cargo_weight": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0.01",
                    "step": "0.01",
                }
            ),
            "planned_distance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0.01",
                    "step": "0.01",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["vehicle"].queryset = Vehicle.objects.filter(
            status="Available"
        )

        self.fields["driver"].queryset = Driver.objects.filter(
            status="Available",
            license_expiry_date__gte=timezone.localdate(),
        )

    def clean(self):
        cleaned_data = super().clean()

        vehicle = cleaned_data.get("vehicle")
        driver = cleaned_data.get("driver")
        cargo_weight = cleaned_data.get("cargo_weight")

        if vehicle and cargo_weight:
            if cargo_weight > vehicle.maximum_load_capacity:
                self.add_error(
                    "cargo_weight",
                    "Cargo weight exceeds the vehicle's maximum load capacity."
                )

        if vehicle and vehicle.status != "Available":
            self.add_error(
                "vehicle",
                "This vehicle is not available for dispatch."
            )

        if driver:
            if driver.status != "Available":
                self.add_error(
                    "driver",
                    "This driver is not available for dispatch."
                )

            if driver.is_license_expired:
                self.add_error(
                    "driver",
                    "This driver's license has expired."
                )

        return cleaned_data