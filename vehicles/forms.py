from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle

        fields = [
            "registration_number",
            "vehicle_name",
            "vehicle_type",
            "maximum_load_capacity",
            "odometer",
            "acquisition_cost",
            "status",
            "region",
        ]

        widgets = {
            "registration_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. MP07AB1234",
                }
            ),

            "vehicle_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Tata Ace",
                }
            ),

            "vehicle_type": forms.Select(
                attrs={"class": "form-select"}
            ),

            "maximum_load_capacity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "odometer": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "acquisition_cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "status": forms.Select(
                attrs={"class": "form-select"}
            ),

            "region": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Gwalior",
                }
            ),
        }

    def clean_registration_number(self):
        registration_number = self.cleaned_data[
            "registration_number"
        ].strip().upper()

        return registration_number