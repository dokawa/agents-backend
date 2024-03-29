# Generated by Django 5.0.1 on 2024-01-10 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("agents", "0001_initial"),
        ("simulations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="agent",
            name="simulation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="agents",
                to="simulations.simulation",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="agent",
            unique_together={("name", "sprite_name")},
        ),
    ]
