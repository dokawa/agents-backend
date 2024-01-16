from django.contrib import admin

from apps.agents.admin import AgentInline
from apps.simulations.event_models import Event
from apps.simulations.models import Simulation


class SimulationAdmin(admin.ModelAdmin):
    model = Simulation
    list_display = ("id", "name")
    inlines = [AgentInline]
    # raw_id_fields = ["agents"]


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ["id", "agent", "simulation", "type", "position_x", "position_y"]
    list_filter = ["agent__name"]


admin.site.register(Simulation, SimulationAdmin)
admin.site.register(Event, EventAdmin)
