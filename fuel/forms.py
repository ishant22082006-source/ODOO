from django import forms
from django.utils import timezone

from .models import FuelLog
from vehicles.models import Vehicle


class FuelLogForm(forms.ModelForm):

    class Meta:
        model = FuelLog

        fields = [
            "vehicle",
            "date",
            "liters",
            "cost",
            "odometer",
            "remarks",
        ]

        widgets = {

            "vehicle": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "liters": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "odometer": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "remarks": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional remarks",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["vehicle"].queryset = Vehicle.objects.exclude(
            status="Retired"
        )

        self.fields["date"].initial = timezone.localdate()