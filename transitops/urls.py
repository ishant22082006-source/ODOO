from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('', include('accounts.urls')),

    # Dashboard
    path('dashboard/', include('dashboard.urls')),

    # Vehicle Module
    path('vehicles/', include('vehicles.urls')),

    # Driver Module
    path('drivers/', include('drivers.urls')),

    # Trip Module
    path('trips/', include('trips.urls')),

    # Maintenance Module
    path('maintenance/', include('maintenance.urls')),

    # Fuel Module
    path('fuel/', include('fuel.urls')),

    # Expense Module
    path('expenses/', include('expenses.urls')),

    # Reports
    path('reports/', include('reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)