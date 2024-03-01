from django.db import models
from django.contrib.auth.models import User

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=[
        ('работа', 'Работа'),
        ('личное', 'Личное'),
        ('саморазвитие', 'Саморазвитие'),
        ('здоровье', 'Здоровье'),
    ], default='personal')

    class Meta:
        db_table = "tblevents"