from django.contrib import admin

from apps.simulations.models import Simulation


class SimulationAdmin(admin.ModelAdmin):
    model = Simulation
    list_display = ("id", "name")


admin.site.register(Simulation, SimulationAdmin)
