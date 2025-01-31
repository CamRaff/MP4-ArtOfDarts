from django.contrib import admin
from .models import Product, Category, Barrel, Flight, Stem

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Barrel)
admin.site.register(Flight)
admin.site.register(Stem)
