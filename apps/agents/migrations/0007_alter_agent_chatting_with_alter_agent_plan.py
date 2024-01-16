# Generated by Django 5.0.1 on 2024-01-16 15:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("agents", "0006_agent_chatting_with_agent_plan"),
    ]

    operations = [
        migrations.AlterField(
            model_name="agent",
            name="chatting_with",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="agents.agent",
            ),
        ),
        migrations.AlterField(
            model_name="agent",
            name="plan",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="agent",
                to="agents.actionplan",
            ),
        ),
    ]
