from django.contrib import admin

from apps.agents.models import Agent


class AgentAdmin(admin.ModelAdmin):
    model = Agent
    list_display = ["id", "name", "sprite_name"]


class AgentInline(admin.TabularInline):
    model = Agent


admin.site.register(Agent, AgentAdmin)
