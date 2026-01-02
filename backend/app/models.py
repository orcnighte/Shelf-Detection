from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    category = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class DailyCount(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="daily_counts"
    )
    date = models.DateField(db_index=True)
    count = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "date"],
                name="uq_dailycount_product_date"
            )
        ]

    def __str__(self):
        return f"{self.product_id} {self.date}: {self.count}"


class Image(models.Model):
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    path = models.TextField()  # مسیر فایل (لوکال یا S3)
    confidence_summary = models.TextField(null=True, blank=True)  # JSON string
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.path}"


