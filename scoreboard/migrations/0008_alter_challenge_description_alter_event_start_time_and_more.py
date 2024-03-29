# Generated by Django 5.0.2 on 2024-02-20 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0007_alter_event_start_time_alter_graph_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='description',
            field=models.TextField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.IntegerField(default=1708419792),
        ),
        migrations.AlterField(
            model_name='graph',
            name='time',
            field=models.IntegerField(default=1708419792.838254),
        ),
    ]
