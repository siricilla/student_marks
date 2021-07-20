from django.db import models


class Marks(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    marks = models.PositiveIntegerField(null=True, blank=True)
