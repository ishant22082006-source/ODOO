from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Vehicle
from .forms import VehicleForm


@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()

    return render(
        request,
        "vehicles/vehicle_list.html",
        {
            "vehicles": vehicles,
        },
    )


@login_required
def vehicle_create(request):

    form = VehicleForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle added successfully.")
            return redirect("vehicle_list")

    return render(
        request,
        "vehicles/vehicle_form.html",
        {
            "form": form,
            "title": "Add Vehicle",
        },
    )


@login_required
def vehicle_update(request, pk):

    vehicle = get_object_or_404(Vehicle, pk=pk)

    form = VehicleForm(
        request.POST or None,
        instance=vehicle,
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle updated successfully.")
            return redirect("vehicle_list")

    return render(
        request,
        "vehicles/vehicle_form.html",
        {
            "form": form,
            "title": "Edit Vehicle",
        },
    )


@login_required
def vehicle_delete(request, pk):

    vehicle = get_object_or_404(
        Vehicle,
        pk=pk,
    )

    vehicle.delete()

    messages.success(
        request,
        "Vehicle deleted successfully."
    )

    return redirect("vehicle_list")