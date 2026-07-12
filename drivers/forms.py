from django import forms
from .models import Driver


class DriverForm(forms.ModelForm):

    class Meta:
        model = Driver

        fields = [
            "name",
            "license_number",
            "license_category",
            "license_expiry_date",
            "contact_number",
            "safety_score",
            "status",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter driver name",
                }
            ),

            "license_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter license number",
                }
            ),

            "license_category": forms.Select(
                attrs={"class": "form-select"}
            ),

            "license_expiry_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "contact_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter contact number",
                }
            ),

            "safety_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "100",
                    "step": "0.01",
                }
            ),

            "status": forms.Select(
                attrs={"class": "form-select"}
            ),
        }

    def clean_license_number(self):
        return self.cleaned_data["license_number"].strip().upper()

    def clean_safety_score(self):
        safety_score = self.cleaned_data["safety_score"]

        if safety_score < 0 or safety_score > 100:
            raise forms.ValidationError(
                "Safety score must be between 0 and 100."
            )

        return safety_score