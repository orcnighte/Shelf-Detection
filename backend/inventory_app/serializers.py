"""
Django REST Framework serializers
"""
from rest_framework import serializers
from .models import Product, DailyCount, Image


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=255)
    category = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=255)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category']


class DailyCountSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = DailyCount
        fields = ['id', 'product_id', 'product', 'date', 'count']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'date', 'path', 'confidence_summary', 'uploaded_at']


class DetectionResultSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    count = serializers.IntegerField()
    confidence = serializers.FloatField()


class ImageUploadResponseSerializer(serializers.Serializer):
    image_id = serializers.IntegerField()
    detections = DetectionResultSerializer(many=True)
    total_products = serializers.IntegerField()
    processing_time = serializers.FloatField()


class AnalyticsSummarySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    average_daily_demand = serializers.FloatField()
    growth_rate = serializers.FloatField()
    demand_consistency = serializers.FloatField()
    total_count = serializers.IntegerField()
    days_analyzed = serializers.IntegerField()


class WeeklyAnalyticsResponseSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    products = AnalyticsSummarySerializer(many=True)


class RecommendationItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    category = serializers.CharField(allow_null=True)
    score = serializers.FloatField()
    explanation = serializers.CharField()
    metrics = serializers.DictField()


class RecommendationsResponseSerializer(serializers.Serializer):
    week_start = serializers.DateField()
    week_end = serializers.DateField()
    recommendations = RecommendationItemSerializer(many=True)
    generated_at = serializers.DateTimeField()



