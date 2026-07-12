from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_view(request):
    context = {
        "active_vehicles": 0,
        "available_vehicles": 0,
        "vehicles_in_maintenance": 0,
        "active_trips": 0,
        "pending_trips": 0,
        "drivers_on_duty": 0,
        "fleet_utilization": 0,
    }

    return render(request, "dashboard.html", context)