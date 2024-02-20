import time

from django.db import models


# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.IntegerField(default=int(time.time()))
    duration_in_seconds = models.IntegerField(default=3600)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)


class Flag(models.Model):
    name = models.CharField(max_length=255)
    points = models.IntegerField(default=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)


class Graph(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    time = models.IntegerField(default=time.time())

    def __str__(self):
        return f"{self.user} - {self.score}"


class Challenge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    files = models.FileField(upload_to='challenges/')
    amount_of_flags = models.IntegerField(default=1)

    def __str__(self):
        return self.name
