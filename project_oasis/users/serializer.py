from rest_framework import serializers
from .models import Customer, UserKeywords


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('email', 'password', 'name', 'user_type', 'phone_no',
                  'nickname', 'age', 'sex')

    def create(self, validated_data):
        return Customer.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            # create_user 메소드는 extra_fields를 **kwargs로 받으므로,
            # 나머지 필드는 extra_fields로 전달할 수 있습니다.
            **{k: v for k, v in validated_data.items() if k not in ['email', 'password', 'name']}
        )


class UserKeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKeywords
        fields = (
            'beverage',
            'dessert',
            'various_menu',
            'special_menu',
            'large_store',
            'background',
            'talking',
            'concentration',
            'trendy_store',
            'gift_packaging',
            'parking',
            'price'
        )

# class Cafe_info_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = CafeInfo
#         fields = ('cafe_id','cafe_name', 'cafe_rating', 'visitor_reviews', 'blog_reviews',\
#                   'address',  'latitude', 'longitude','cafe_buisiness_hour', 'cafe_phone', 'cafe_link',\
#                     'cafe_desc')
