from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import MaintenanceLog
from .forms import MaintenanceLogForm


@login_required
def maintenance_list(request):
    maintenance_logs = MaintenanceLog.objects.select_related(
        "vehicle"
    ).all()

    status = request.GET.get("status")

    if status:
        maintenance_logs = maintenance_logs.filter(status=status)

    context = {
        "maintenance_logs": maintenance_logs,
        "status_choices": MaintenanceLog.STATUS_CHOICES,
    }

    return render(
        request,
        "maintenance/maintenance_list.html",
        context,
    )


@login_required
@transaction.atomic
def maintenance_create(request):
    form = MaintenanceLogForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        maintenance_log = form.save(commit=False)
        maintenance_log.status = "Active"
        maintenance_log.save()

        vehicle = maintenance_log.vehicle
        vehicle.status = "In Shop"
        vehicle.save()

        messages.success(
            request,
            "Maintenance record created. Vehicle is now In Shop."
        )

        return redirect("maintenance_list")

    return render(
        request,
        "maintenance/maintenance_form.html",
        {
            "form": form,
            "title": "Add Maintenance Record",
        },
    )


@login_required
@transaction.atomic
def maintenance_close(request, pk):
    maintenance_log = get_object_or_404(
        MaintenanceLog,
        pk=pk,
    )

    if request.method == "POST":

        if maintenance_log.status == "Completed":
            messages.warning(
                request,
                "This maintenance record is already completed."
            )
            return redirect("maintenance_list")

        maintenance_log.status = "Completed"
        maintenance_log.end_date = timezone.localdate()
        maintenance_log.save()

        vehicle = maintenance_log.vehicle

        if vehicle.status != "Retired":
            vehicle.status = "Available"
            vehicle.save()

        messages.success(
            request,
            "Maintenance completed. Vehicle is now available."
        )

    return redirect("maintenance_list")