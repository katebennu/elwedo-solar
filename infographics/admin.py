from django.contrib import admin
from infographics.models import Building, Apartment, Grid, ConsumptionMeasurement, ProductionMeasurement, PanelsToInstall
    # , CO2Multiplier, KmMultiplier, EurMultiplier

admin.site.register(Building)
admin.site.register(Apartment)
admin.site.register(Grid)
admin.site.register(PanelsToInstall)
admin.site.register(ConsumptionMeasurement)
admin.site.register(ProductionMeasurement)
# admin.site.register(CO2Multiplier)
# admin.site.register(KmMultiplier)
# admin.site.register(EurMultiplier)
