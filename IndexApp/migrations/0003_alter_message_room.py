# Generated by Django 4.1 on 2022-09-15 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("IndexApp", "0002_alter_message_room_alter_message_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="IndexApp.room",
            ),
        ),
    ]
