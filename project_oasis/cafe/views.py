from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializer import CafeSerializer
from .ML import recommend, distance
from .models import Cafe, CafeKeywords
from users.models import UserKeywords, Customer
from users.serializer import UserKeywordsSerializer

import random, json



# Create your views here.

# 사용자의 선호 프로필를 이용해 유사한 키워드를 가진 카페 추천

class RecommendCafeKeywordView(APIView):
	def get(self, request):
	# data = json.loads(request.body.decode('utf-8'))
	# user_cafe_profile = data['user_cafe_profile']
	# user_location = data['user_location']
		email = request.GET.get("email")
		#user_cafe_profile_str = request.GET.get('user_cafe_profile')
		user_location_str = request.GET.get('user_location')

		try:
			#user_cafe_profile = list(map(int, user_cafe_profile_str.split(',')))
			if not email:
				raise ValueError
			user_location = list(map(float, user_location_str.split(',')))
		except:
			return Response({"message: INAVILD_DATA_TYPE"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			customer = Customer.objects.get(email=email)
			user_keyword = UserKeywords.objects.get(user=customer)
		except:
			return Response({'message': 'USER_OR_KEYWORD_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
		
		user_keyword_serializer = UserKeywordsSerializer(user_keyword)
		user_keyword_list = [keyword.value for keyword in user_keyword_serializer][:-3]

		
		#사용자 위치 기준 근처 카페 키워드 데이터
		nearby_cafes_id = distance.get_cafe_list_base_location(user_location, Cafe.objects.all())
		nearby_cafes_value = CafeKeywords.objects.filter(cafe__in = nearby_cafes_id)
		nearby_cafes = Cafe.objects.filter(cafe_id__in = nearby_cafes_id)

		# #랜덤으로 키워드가 없는 카페 중 하나 추천
		nearby_cafes_without_keywords = nearby_cafes.exclude(cafe_id__in = nearby_cafes_value).values('cafe_id')
		# Extract the IDs of these cafes
		nearby_cafes_without_keywords_id = [cafe['cafe_id'] for cafe in nearby_cafes_without_keywords]

		recommend_cafe_list = recommend.recommend_cafe_base_keyworkd(user_keyword_list, nearby_cafes_value)
		recommend_cafe_list.append(random.choice(nearby_cafes_without_keywords_id))

		recommend_cafe = nearby_cafes.filter(cafe_id__in = recommend_cafe_list)
		#recommend_cafe = Cafe.objects.filter(cafe_id__in=recommend_cafe_id_list)
		#직렬화
		serializer = CafeSerializer(recommend_cafe, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	


# 평점과 자체 공통 키워드를 이용해 TOP 3 카페를 추천
class RecommendCafeRatingView(APIView):
	def get(self, request):
		user_location_str = request.GET.get('user_location')

		try:
			user_location = list(map(float, user_location_str.split(',')))
		except:
			return Response({"message: INAVILD_DATA_TYPE"}, status=status.HTTP_400_BAD_REQUEST)

		nearby_cafes_id = distance.get_cafe_list_base_location(user_location, Cafe.objects.all())
		nearby_cafes_value = CafeKeywords.objects.filter(cafe__in=nearby_cafes_id)

		recommend_cafe_list = recommend.recommend_cafe_base_rating(nearby_cafes_value)
		recommend_cafe = Cafe.objects.filter(cafe_id__in = recommend_cafe_list)

		#직렬화
		serializer = CafeSerializer(recommend_cafe, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
		# return JsonResponse(json.dump(json_data), safe=False, status=200)


# def get_reviewed_cafes(request):
class CafeView(APIView):
	def get(self, request):
		search_target = request.GET.get('search_target')

		try:
			result = Cafe.objects.filter( Q(cafe_name__contains=search_target) | Q(address__contains=search_target))
			if not result:
				return Response({'message': "CAFE_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
			serializer = CafeSerializer(result, many=True)
			return Response({"message": "CAFE_FOUND_SUCCESS", "cafe_list": serializer.data}, status=status.HTTP_200_OK)
		except Exception as ex:
			print(ex)
			return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	
	def put(self, request):
		data = json.loads(request.body)
		cafe_name = data['cafe_name']
		cafe_value_list = list(data['cafe_value_list'])
		
		try:
			cafe = Cafe.objects.get(cafe_name=cafe_name)
		except:
			return Response({'message': 'CAFE_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
		
		try:
			cafe_attribute = ['cafe_phone_no', 'cafe_info', 'business_hours']
			
			for idx in range(len(cafe_attribute)):
				setattr(cafe, cafe_attribute[idx], cafe_value_list[idx])
			cafe.save()
			return Response({'message': 'CAFE_INFO_UPDATE_SUCCESS'}, status=status.HTTP_200_OK)
		except Exception as ex:
			print(ex)
			return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            