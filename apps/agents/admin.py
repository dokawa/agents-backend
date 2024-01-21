from django.contrib import admin

from apps.agents.models import ActionPlan, Agent


class AgentAdmin(admin.ModelAdmin):
    model = Agent
    list_display = ["id", "name", "sprite_name"]


class AgentInline(admin.TabularInline):
    model = Agent


class ActionPlanAdmin(admin.ModelAdmin):
    model = ActionPlan
    list_display = ("id", "agent", "description", "start_time", "time")
    list_filter = ("type",)
    inlines = [
        AgentInline,
    ]

    def time(self, obj):
        # Calculate hours, minutes, and seconds
        if not obj.start_time:
            return

        time_delta = obj.start_time - obj.start_time.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"


admin.site.register(Agent, AgentAdmin)
admin.site.register(ActionPlan, ActionPlanAdmin)
