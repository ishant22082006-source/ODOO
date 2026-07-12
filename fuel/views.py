from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import FuelLog
from .forms import FuelLogForm


@login_required
def fuel_list(request):

    fuel_logs = FuelLog.objects.select_related("vehicle").all()

    context = {
        "fuel_logs": fuel_logs,
    }

    return render(
        request,
        "fuel/fuel_list.html",
        context,
    )


@login_required
def fuel_create(request):

    form = FuelLogForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fuel log added successfully."
            )

            return redirect("fuel_list")

    return render(
        request,
        "fuel/fuel_form.html",
        {
            "form": form,
            "title": "Add Fuel Log",
        },
    )