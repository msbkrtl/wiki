from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=22)  # max_length = required by default
    description = models.TextField(blank=False, null=True, default="OLOLOLOL")
    price = models.DecimalField(decimal_places=2, max_digits=100000)
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=True)
    lo = models.CharField(max_length=22)  # max_length = required by default
