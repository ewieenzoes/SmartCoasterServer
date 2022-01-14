from django.db import models

# Create your models here.
class Untersetzer(models.Model):
    identifier = models.CharField(max_length=5)
    glass_level = models.IntegerField(default=0)
    timeout = models.BooleanField()
    table = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    def __str__(self):
        return 'Untersetzer Tisch' + self.table
