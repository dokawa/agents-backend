# Generated by Django 5.0.1 on 2024-01-10 13:30

from django.db import migrations
from pgvector.django import VectorExtension


class Migration(migrations.Migration):
    dependencies = [
        ("simulations", "0002_auto_20240110_1325"),
    ]

    operations = [VectorExtension()]
