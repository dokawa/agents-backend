from django.contrib import admin

from apps.agents.models import ActionPlan, Agent


class AgentAdmin(admin.ModelAdmin):
    model = Agent
    list_display = ["id", "name", "sprite_name"]


class AgentInline(admin.TabularInline):
    model = Agent


class ActionPlanAdmin(admin.ModelAdmin):
    model = ActionPlan


admin.site.register(Agent, AgentAdmin)
admin.site.register(ActionPlan, ActionPlanAdmin)
