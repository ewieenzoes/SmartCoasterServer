from django.db import models


# Create your models here.
class Untersetzer(models.Model):
    identifier = models.CharField(max_length=5)
    glass_level = models.IntegerField(default=0)
    timeout = models.BooleanField()
    table = models.ForeignKey('Table', on_delete=models.CASCADE, related_name='table', blank=True, null=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return 'Untersetzer ' + self.identifier


class Beverage(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    edition = models.CharField(max_length=200)
    coaster = models.ForeignKey('Untersetzer', on_delete=models.CASCADE, related_name='beverage')

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    coaster = models.ForeignKey('Untersetzer', on_delete=models.CASCADE, related_name='food')

    def __str__(self):
        return self.name

## --> Move Beverages in DB (WIP)
class BeverageTemplate(models.Model):
    name = models.CharField(max_length=200) #Muss eindeutig sein!!
    price = models.FloatField(default=0)
    edition = models.CharField(max_length=200)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " " + self.edition

class FoodTemplate(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Table(models.Model):
    identifier = models.CharField(max_length=200)
    coasters = models.ManyToManyField('Untersetzer', related_name='coasterForTable')

    def __str__(self):
        return 'Tisch' + self.identifier

class lastBeverages(models.Model):
    beverages = models.ForeignKey('Beverage', on_delete=models.CASCADE, related_name='new_beverage')

#To-Do: Create View
class tempCoasterGroup(models.Model):
    identifier = models.CharField(max_length=200)
    coasters = models.ManyToManyField('Untersetzer')

    def __str__(self):
        return self.identifier

class serviceCall(models.Model):
    coaster = models.ForeignKey('Untersetzer', on_delete=models.CASCADE, related_name='serviceCall')

class paymentRequest(models.Model):
    coaster = models.ForeignKey('Untersetzer', on_delete=models.CASCADE, related_name='serviceCall')
    type = models.CharField(max_length=200)