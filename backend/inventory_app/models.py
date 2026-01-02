"""
Django models for inventory management
"""
from django.db import models
from django.utils import timezone


class Product(models.Model):
    """Product catalog"""
    name = models.CharField(max_length=255, db_index=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['name']

    def __str__(self):
        return self.name


class DailyCount(models.Model):
    """Daily product count records"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='daily_counts')
    date = models.DateField(db_index=True)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_counts'
        unique_together = ['product', 'date']
        ordering = ['-date', 'product']

    def __str__(self):
        return f"{self.product.name} - {self.date}: {self.count}"


class Image(models.Model):
    """Stored image metadata"""
    date = models.DateTimeField(default=timezone.now, db_index=True)
    path = models.CharField(max_length=500)
    confidence_summary = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'images'
        ordering = ['-date']

    def __str__(self):
        return f"Image {self.id} - {self.date}"



