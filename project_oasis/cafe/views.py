from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import random

from .serializer import CafeSerializer
from .ML import recommend, distance
from .models import Cafe, CafeKeywords

# Create your views here.

# 사용자의 선호 프로필를 이용해 유사한 키워드를 가진 카페 추천
@api_view(['GET'])
def recommend_cafes_base_keyword(request):
	# data = json.loads(request.body.decode('utf-8'))
	# user_cafe_profile = data['user_cafe_profile']
	# user_location = data['user_location']
	user_cafe_profile_str = request.GET.get('user_cafe_profile')
	user_location_str = request.GET.get('user_location')

	try:
		user_cafe_profile = list(map(int, user_cafe_profile_str.split(',')))
		user_location = list(map(float, user_location_str.split(',')))
	except:
		return Response({"message: Invalid data type"}, status=status.HTTP_400_BAD_REQUEST)
	
	#사용자 위치 기준 근처 카페 키워드 데이터
	nearby_cafes_id = distance.get_cafe_list_base_location(user_location, Cafe.objects.all())
	nearby_cafes_value = CafeKeywords.objects.filter(cafe__in = nearby_cafes_id)
	nearby_cafes = Cafe.objects.filter(cafe_id__in = nearby_cafes_id)

	# #랜덤으로 키워드가 없는 카페 중 하나 추천
	nearby_cafes_without_keywords = nearby_cafes.exclude(cafe_id__in = nearby_cafes_value).values('cafe_id')
	# Extract the IDs of these cafes
	nearby_cafes_without_keywords_id = [cafe['cafe_id'] for cafe in nearby_cafes_without_keywords]

	recommend_cafe_list = recommend.recommend_cafe_base_keyworkd(user_cafe_profile, nearby_cafes_value)
	recommend_cafe_list.append(random.choice(nearby_cafes_without_keywords_id))

	recommend_cafe = nearby_cafes.filter(cafe_id__in = recommend_cafe_list)
	#recommend_cafe = Cafe.objects.filter(cafe_id__in=recommend_cafe_id_list)
	#직렬화
	serializer = CafeSerializer(recommend_cafe, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)
	


# 평점과 자체 공통 키워드를 이용해 TOP 3 카페를 추천
@api_view(['GET'])
def recommend_cafes_base_rating(request):
	user_location_str = request.GET.get('user_location')

	try:
		user_location = list(map(float, user_location_str.split(',')))
	except:
		return Response({"message: Invalid data type"}, status=status.HTTP_400_BAD_REQUEST)

	nearby_cafes_id = distance.get_cafe_list_base_location(user_location, Cafe.objects.all())
	nearby_cafes_value = CafeKeywords.objects.filter(cafe__in=nearby_cafes_id)

	recommend_cafe_list = recommend.recommend_cafe_base_rating(nearby_cafes_value)
	recommend_cafe = Cafe.objects.filter(cafe_id__in = recommend_cafe_list)

	#직렬화
	serializer = CafeSerializer(recommend_cafe, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)
	# return JsonResponse(json.dump(json_data), safe=False, status=200)


# def get_reviewed_cafes(request):
