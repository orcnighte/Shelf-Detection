from django.contrib import admin
from .models import Product, DailyCount, Image


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'created_at']
    search_fields = ['name', 'category']
    list_filter = ['category', 'created_at']


@admin.register(DailyCount)
class DailyCountAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'date', 'count', 'created_at']
    list_filter = ['date', 'product']
    search_fields = ['product__name']
    date_hierarchy = 'date'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'path', 'uploaded_at']
    list_filter = ['date', 'uploaded_at']
    date_hierarchy = 'date'



