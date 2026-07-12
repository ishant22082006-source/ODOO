from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from .models import Trip
from .forms import TripForm


@login_required
def trip_list(request):
    trips = Trip.objects.select_related(
        "vehicle",
        "driver"
    ).all()

    status = request.GET.get("status")

    if status:
        trips = trips.filter(status=status)

    context = {
        "trips": trips,
        "status_choices": Trip.STATUS_CHOICES,
    }

    return render(request, "trips/trip_list.html", context)


@login_required
def trip_create(request):
    form = TripForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        trip = form.save(commit=False)
        trip.status = "Draft"
        trip.save()

        messages.success(
            request,
            "Trip created successfully as Draft."
        )
        return redirect("trip_list")

    return render(
        request,
        "trips/trip_form.html",
        {
            "form": form,
            "title": "Create Trip",
        },
    )


@login_required
@transaction.atomic
def trip_dispatch(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    if request.method == "POST":
        if trip.status != "Draft":
            messages.error(
                request,
                "Only Draft trips can be dispatched."
            )
            return redirect("trip_list")

        if trip.vehicle.status != "Available":
            messages.error(
                request,
                "Vehicle is not available."
            )
            return redirect("trip_list")

        if trip.driver.status != "Available":
            messages.error(
                request,
                "Driver is not available."
            )
            return redirect("trip_list")

        if trip.driver.is_license_expired:
            messages.error(
                request,
                "Driver license has expired."
            )
            return redirect("trip_list")

        if trip.cargo_weight > trip.vehicle.maximum_load_capacity:
            messages.error(
                request,
                "Cargo weight exceeds vehicle capacity."
            )
            return redirect("trip_list")

        trip.status = "Dispatched"
        trip.vehicle.status = "On Trip"
        trip.driver.status = "On Trip"

        trip.vehicle.save()
        trip.driver.save()
        trip.save()

        messages.success(
            request,
            "Trip dispatched successfully."
        )

    return redirect("trip_list")


@login_required
@transaction.atomic
def trip_complete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    if request.method == "POST":
        if trip.status != "Dispatched":
            messages.error(
                request,
                "Only dispatched trips can be completed."
            )
            return redirect("trip_list")

        final_odometer = request.POST.get("final_odometer")

        if not final_odometer:
            messages.error(
                request,
                "Final odometer reading is required."
            )
            return redirect("trip_list")

        try:
            final_odometer = float(final_odometer)
        except ValueError:
            messages.error(
                request,
                "Enter a valid final odometer reading."
            )
            return redirect("trip_list")

        if final_odometer < float(trip.vehicle.odometer):
            messages.error(
                request,
                "Final odometer cannot be less than current odometer."
            )
            return redirect("trip_list")

        trip.final_odometer = final_odometer
        trip.status = "Completed"

        trip.vehicle.odometer = final_odometer
        trip.vehicle.status = "Available"
        trip.driver.status = "Available"

        trip.vehicle.save()
        trip.driver.save()
        trip.save()

        messages.success(
            request,
            "Trip completed successfully."
        )

    return redirect("trip_list")


@login_required
@transaction.atomic
def trip_cancel(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    if request.method == "POST":
        if trip.status in ["Completed", "Cancelled"]:
            messages.error(
                request,
                "This trip cannot be cancelled."
            )
            return redirect("trip_list")

        if trip.status == "Dispatched":
            trip.vehicle.status = "Available"
            trip.driver.status = "Available"

            trip.vehicle.save()
            trip.driver.save()

        trip.status = "Cancelled"
        trip.save()

        messages.success(
            request,
            "Trip cancelled successfully."
        )

    return redirect("trip_list")