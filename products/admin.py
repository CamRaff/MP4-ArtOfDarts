from django.contrib import admin
from .models import Product, Category, Barrel, Flight, Stem


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class BarrelAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'barrel_shape',
        'price',
        'image',
    )

    ordering = ('barrel_shape',)


class FlightAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'flight_shape',
        'price',
        'image',
    )

    ordering = ('flight_shape',)


class StemAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'stem_length',
        'price',
        'image',
    )

    ordering = ('stem_length',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Barrel, BarrelAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Stem, StemAdmin)
