from django.contrib import admin
from infographics.models import Building, Apartment, Grid, ConsumptionMeasurement, ProductionMeasurement, PanelsToInstall

admin.site.register(Building)
admin.site.register(Apartment)
admin.site.register(Grid)
admin.site.register(PanelsToInstall)
admin.site.register(ConsumptionMeasurement)
admin.site.register(ProductionMeasurement)
