from django.contrib import admin
from infographics.models import Building, Apartment, ExampleGrid, ConsumptionMeasurement, ProductionMeasurement, TargetCapacity
    # , CO2Multiplier, KmMultiplier, EurMultiplier

admin.site.register(Building)
admin.site.register(Apartment)
admin.site.register(ExampleGrid)
admin.site.register(TargetCapacity)
admin.site.register(ConsumptionMeasurement)
admin.site.register(ProductionMeasurement)
# admin.site.register(CO2Multiplier)
# admin.site.register(KmMultiplier)
# admin.site.register(EurMultiplier)
