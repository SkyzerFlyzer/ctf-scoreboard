# Generated by Django 5.0.2 on 2024-02-14 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='duration_in_seconds',
            field=models.IntegerField(default=3600),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.IntegerField(default=1707920260),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.IntegerField(default=1707916660),
        ),
        migrations.AlterField(
            model_name='graph',
            name='time',
            field=models.IntegerField(default=1707916660.925372),
        ),
    ]
