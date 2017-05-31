from django.contrib import admin
from infographics.models import *

admin.site.register(Building)
admin.site.register(Apartment)
admin.site.register(TargetCapacity)
admin.site.register(ConsumptionMeasurement)
admin.site.register(ProductionMeasurement)
admin.site.register(ExampleGrid)
admin.site.register(CO2Multiplier)
admin.site.register(KmMultiplier)
admin.site.register(GridPriceMultiplier)
admin.site.register(SolarPriceMultiplier)
