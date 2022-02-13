from django.contrib import admin

# Register your models here.
from .models import Untersetzer, Beverage, Table

admin.site.register(Untersetzer)
admin.site.register(Beverage)
admin.site.register(Table)
