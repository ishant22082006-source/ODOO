from django import forms
from django.utils import timezone

from .models import Expense
from vehicles.models import Vehicle


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense

        fields = [
            "vehicle",
            "expense_type",
            "amount",
            "date",
            "remarks",
        ]

        widgets = {

            "vehicle": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "expense_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
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