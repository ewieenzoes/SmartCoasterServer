from django.contrib import admin

# Register your models here.
from .models import Untersetzer, Beverage, Table, BeverageTemplate, FoodTemplate, tempCoasterGroup, QuickAccessTemplate, \
    Food, QuickAccessTemplateFood

admin.site.register(Untersetzer)
admin.site.register(Beverage)
admin.site.register(Table)
admin.site.register(BeverageTemplate)
admin.site.register(FoodTemplate)
admin.site.register(Food)
admin.site.register(tempCoasterGroup)
admin.site.register(QuickAccessTemplate)
admin.site.register(QuickAccessTemplateFood)
