from django.contrib import admin

from apps.agents.admin import AgentInline
from apps.simulations.event_models import Event
from apps.simulations.models import Simulation


class SimulationAdmin(admin.ModelAdmin):
    model = Simulation
    list_display = ("id", "name", "current_time")
    inlines = [AgentInline]
    # raw_id_fields = ["agents"]


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = [
        "id",
        "type",
        "agent",
        "interact_with",
        "simulation",
        "sim_time",
        "position_x",
        "position_y",
    ]
    list_filter = ["agent__name", "type"]

    def sim_time(self, obj):
        return obj.sim_time_created.strftime("%Y-%m-%d %H:%M:%S")


admin.site.register(Simulation, SimulationAdmin)
admin.site.register(Event, EventAdmin)
