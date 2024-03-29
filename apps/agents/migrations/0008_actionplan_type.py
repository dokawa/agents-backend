# Generated by Django 5.0.1 on 2024-01-16 16:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("agents", "0007_alter_agent_chatting_with_alter_agent_plan"),
    ]

    operations = [
        migrations.AddField(
            model_name="actionplan",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("wait", "Wait"),
                    ("move", "Move"),
                    ("do_not_react", "Do not react"),
                    ("chat_with", "Chat with"),
                ],
                max_length=32,
                null=True,
            ),
        ),
    ]
