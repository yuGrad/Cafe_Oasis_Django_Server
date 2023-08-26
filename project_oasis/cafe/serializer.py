from rest_framework import serializers
from .models import Cafe

class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ['business_name', 'cafe_name', 'cafe_rating', 'visitor_reviews', 'blog_reviews', 'cafe_phone_no', 'cafe_info', 'business_hours', 'address', 'latitude', 'longitude', 'cafe_image']
