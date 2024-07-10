from django.db import models

# Create your models here.
# optimizer/models.py
from django.db import models

class GFG(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    address = models.CharField(max_length=500)

class File(models.Model):
    file = models.FileField(upload_to="excel")
