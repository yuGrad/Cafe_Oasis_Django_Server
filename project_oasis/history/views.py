from django.http import JsonResponse
import json

from .models import CafeRating, VisitHistory
from users.models import Customer
from cafe.models import Cafe

# Create your views here.
#카페 평점 이력을 저장
def create_cafe_rating_history(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email']
    business_name = data['business_name']
    cafe_rating = data['cafe_rating']

    user = Customer.objects.filter(email = email)
    cafe = Cafe.objects.filter(business_name = business_name)
    if user.exists() and cafe.exists():
        user = user[0]
        cafe = cafe[0]
    else:
        return JsonResponse({'message' : "CAFE_OR_USER_NOT_FOUND"},status =404)
    
    try:
        CafeRating.objects.create(
            user = user,
            cafe = cafe,
            rating = cafe_rating
        )
        return JsonResponse({'message': "CAFE_RATING_CREATED_SUCCESS"}, status=200)
    except:
        return JsonResponse({'message': 'CAFE_RATING_CREATION_FAILED'}, status=400)
    

#카페 방문 이력을 저장
def create_cafe_visit_history(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email']
    business_name = data['business_name']
    total_spend = data['total_spend']
    visit_date = data['visit_date']

    user = Customer.objects.filter(email = email)
    cafe = Cafe.objects.filter(business_name = business_name)
    if user.exists() and cafe.exists():
        user = user[0]
        cafe = cafe[0]
    else:
        return JsonResponse({'message' : "CAFE_OR_USER_NOT_FOUND"},status =404)
    
    try:
        VisitHistory.objects.create(
            user = user,
            cafe = cafe,
            total_spend = total_spend,
            visit_date = visit_date
        )
        return JsonResponse({'message': "CAFE_VISIT_HISTORY_CREATED_SUCCESS"}, status=200)
    except:
        return JsonResponse({'message': 'CAFE_vISIT_HISTORY_CREATED_FAILED'}, status=400)


        
