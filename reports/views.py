from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from vehicles.models import Vehicle
from trips.models import Trip
from fuel.models import FuelLog
from expenses.models import Expense
from maintenance.models import MaintenanceLog


@login_required
def reports_dashboard(request):

    total_vehicles = Vehicle.objects.count()

    available_vehicles = Vehicle.objects.filter(
        status="Available"
    ).count()

    on_trip = Vehicle.objects.filter(
        status="On Trip"
    ).count()

    in_shop = Vehicle.objects.filter(
        status="In Shop"
    ).count()

    retired = Vehicle.objects.filter(
        status="Retired"
    ).count()

    completed_trips = Trip.objects.filter(
        status="Completed"
    ).count()

    fuel_cost = FuelLog.objects.aggregate(
        total=Sum("cost")
    )["total"] or 0

    expense_cost = Expense.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    maintenance_cost = MaintenanceLog.objects.aggregate(
        total=Sum("cost")
    )["total"] or 0

    operational_cost = (
        fuel_cost +
        expense_cost +
        maintenance_cost
    )

    fleet_utilization = 0

    if total_vehicles > 0:
        fleet_utilization = round(
            (on_trip / total_vehicles) * 100,
            2
        )

    context = {

        "total_vehicles": total_vehicles,
        "available_vehicles": available_vehicles,
        "on_trip": on_trip,
        "in_shop": in_shop,
        "retired": retired,

        "completed_trips": completed_trips,

        "fuel_cost": fuel_cost,

        "expense_cost": expense_cost,

        "maintenance_cost": maintenance_cost,

        "operational_cost": operational_cost,

        "fleet_utilization": fleet_utilization,

    }

    return render(
        request,
        "reports/reports.html",
        context,
    )