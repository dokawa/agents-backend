# Generated by Django 5.0.1 on 2024-01-14 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("agents", "0003_auto_20240110_1326"),
        ("simulations", "0006_simulation_step"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="address",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="interacting_with",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="agents.agent",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="visual_representation",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
