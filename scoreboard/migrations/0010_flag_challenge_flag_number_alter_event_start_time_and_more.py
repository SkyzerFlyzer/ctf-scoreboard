# Generated by Django 5.0.2 on 2024-02-20 13:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0009_alter_challenge_description_alter_event_start_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='challenge',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='scoreboard.challenge'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flag',
            name='number',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.IntegerField(default=1708436411),
        ),
        migrations.AlterField(
            model_name='graph',
            name='time',
            field=models.IntegerField(default=1708436411.347778),
        ),
        migrations.CreateModel(
            name='FlagSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255)),
                ('time', models.IntegerField(default=1708436411.348224)),
                ('flag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoreboard.flag')),
            ],
        ),
    ]
