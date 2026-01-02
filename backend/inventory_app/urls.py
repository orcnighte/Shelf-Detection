"""
URL configuration for inventory_app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Images
    path('images/upload', views.upload_image, name='upload_image'),
    path('images', views.get_images, name='get_images'),
    
    # Products
    path('products', views.products, name='products'),
    path('products/<int:product_id>', views.delete_product, name='delete_product'),
    path('products/<int:product_id>/counts', views.product_counts, name='product_counts'),
    
    # Analytics
    path('analytics/weekly', views.weekly_analytics, name='weekly_analytics'),
    path('analytics/daily', views.daily_summary, name='daily_summary'),
    
    # Recommendations
    path('recommendations/weekly', views.weekly_recommendations, name='weekly_recommendations'),
]



