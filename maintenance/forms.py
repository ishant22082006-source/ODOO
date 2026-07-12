from django import forms
from django.utils import timezone

from .models import MaintenanceLog
from vehicles.models import Vehicle


class MaintenanceLogForm(forms.ModelForm):

    class Meta:
        model = MaintenanceLog

        fields = [
            "vehicle",
            "maintenance_type",
            "description",
            "start_date",
            "cost",
        ]

        widgets = {
            "vehicle": forms.Select(
                attrs={"class": "form-select"}
            ),

            "maintenance_type": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Oil Change, Engine Repair",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter maintenance details",
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # On Trip and Retired vehicles cannot enter maintenance.
        self.fields["vehicle"].queryset = Vehicle.objects.filter(
            status__in=["Available", "In Shop"]
        )

        if not self.instance.pk:
            self.fields["start_date"].initial = timezone.localdate()