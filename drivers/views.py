from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Driver
from .forms import DriverForm


@login_required
def driver_list(request):
    drivers = Driver.objects.all().order_by("-created_at")

    status = request.GET.get("status")
    license_category = request.GET.get("category")
    search = request.GET.get("search")

    if status:
        drivers = drivers.filter(status=status)

    if license_category:
        drivers = drivers.filter(license_category=license_category)

    if search:
        drivers = drivers.filter(name__icontains=search)

    context = {
        "drivers": drivers,
        "status_choices": Driver.STATUS_CHOICES,
        "category_choices": Driver.LICENSE_CATEGORY_CHOICES,
    }

    return render(request, "drivers/driver_list.html", context)


@login_required
def driver_create(request):
    form = DriverForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Driver added successfully.")
        return redirect("driver_list")

    return render(
        request,
        "drivers/driver_form.html",
        {
            "form": form,
            "title": "Add Driver",
        },
    )


@login_required
def driver_update(request, pk):
    driver = get_object_or_404(Driver, pk=pk)

    form = DriverForm(
        request.POST or None,
        instance=driver,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Driver updated successfully.")
        return redirect("driver_list")

    return render(
        request,
        "drivers/driver_form.html",
        {
            "form": form,
            "title": "Edit Driver",
        },
    )


@login_required
def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)

    if request.method == "POST":
        driver.delete()
        messages.success(request, "Driver deleted successfully.")
        return redirect("driver_list")

    return render(
        request,
        "drivers/driver_confirm_delete.html",
        {"driver": driver},
    )