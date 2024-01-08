from django.db import models


class Cafe(models.Model):
    cafe_id = models.PositiveIntegerField(primary_key=True)
    cafe_name = models.CharField(max_length=255)
    cafe_type = models.CharField(max_length=64)
    cafe_rating = models.DecimalField(max_digits=3, decimal_places=2)
    visitor_reviews = models.IntegerField()
    blog_reviews = models.IntegerField()
    cafe_phone_no = models.CharField(max_length=20, blank=True)
    cafe_info = models.TextField(blank=True)
    business_hours = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    cafe_image = models.URLField(max_length=1024, blank=True)

    class Meta:
        db_table = 'Cafe'


class CafeKeyword(models.Model):
    LABEL_CHOICES = [(i, str(i)) for i in range(8)]

    cafe = models.OneToOneField(
        Cafe, on_delete=models.CASCADE, primary_key=True)
    
    beverage = models.FloatField()
    dessert = models.FloatField()
    special_various_menu = models.FloatField()
    
    background = models.FloatField()
    design = models.FloatField()

    cozy = models.FloatField()
    lively = models.FloatField()
    
    price = models.FloatField()
    gift_packaging = models.BooleanField()
    large_parking = models.FloatField()

    clean = models.FloatField()
    service = models.FloatField()

    label = models.PositiveSmallIntegerField(choices=LABEL_CHOICES)

    class Meta:
        db_table = 'CafeKeyword'
