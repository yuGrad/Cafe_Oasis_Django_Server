from django.db import models

# Create your models here.


class Cafe(models.Model):
    cafe_id = models.PositiveIntegerField(primary_key=True)
    business_name = models.CharField(max_length=255)
    cafe_name = models.CharField(max_length=255)
    cafe_rating = models.DecimalField(max_digits=3, decimal_places=2)
    visitor_reviews = models.IntegerField()
    blog_reviews = models.IntegerField()
    cafe_phone_no = models.CharField(max_length=20, blank=True)
    cafe_info = models.TextField(blank=True)
    business_hours = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    cafe_image = models.URLField(max_length=200, blank=True)

    class Meta:
        db_table = 'Cafe'


class CafeKeywords(models.Model):
    LABEL_CHOICES = [(i, str(i)) for i in range(8)]

    cafe = models.OneToOneField(
        Cafe, on_delete=models.CASCADE, primary_key=True)
    beverage = models.FloatField()
    dessert = models.FloatField()
    various_menu = models.FloatField()
    special_menu = models.FloatField()
    large_store = models.FloatField()
    background = models.FloatField()
    talking = models.FloatField()
    concentration = models.FloatField()
    trendy_store = models.FloatField()
    label = models.PositiveSmallIntegerField(choices=LABEL_CHOICES)

    gift_packaging = models.BooleanField()
    parking = models.BooleanField()
    price = models.BooleanField(default=False)
    common_keywords = models.FloatField()

    class Meta:
        db_table = 'CafeKeywords'
