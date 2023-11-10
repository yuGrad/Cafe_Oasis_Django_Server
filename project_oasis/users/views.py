from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Customer, EmailCode, UserKeywords
from .serializer import CustomerSerializer, UserKeywordsSerializer
from .email_verification import email_validate

import random
import json
import bcrypt

# 로그인
# https://axce.tistory.com/116


class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)

        try:
            email = data['email']
            password = data['password']
            customer = Customer.objects.get(email=email)
            if customer and customer.check_password(password):
                # User 객체와 연결된 Customer 객체를 직접 참조
                serialzer_customer = CustomerSerializer(customer)

                # 사용자 키워드 불러오기
                user_keywords = UserKeywords.objects.filter(user=customer)
                if user_keywords:
                    user_keywords = user_keywords[0]
                    serialzer_user_keywords = UserKeywordsSerializer(
                        user_keywords).data
                else:
                    serialzer_user_keywords = None

                return Response({'message': "LOGIN_SUCCESS",
                                'customer': serialzer_customer.data,
                                 'user_keywords': serialzer_user_keywords},
                                status=status.HTTP_200_OK)

            return Response({"message": "INVALID_USER"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            print(ex)
            return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 회원가입


class SignUpView(APIView):
    # 조회 get id값으로 !get_all 보내면 전체 조회, 특정 아이디 보내면 해당 아이디 정보 반환
    def get(self, request):
        reqString = request.GET.get('email', None)

        try:
            account = Customer.objects.get(email=reqString)
            # "account": CustomerSerializer( Customer.objects.f(email=reqString))
            return Response({"message": "EMAIL_EXISTS"}, status=status.HTTP_200_OK)
        except:
            return Response({'message': "USER_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

    # post방식으로 요청할 경우 회원가입한다.
    def post(self, request):
        data = json.loads(request.body)
        print(data)

        # 비밀번호를 bcrypt 해싱 기법으로 해시 후 데이터 베이스에 저장
        # hashed_password = bcrypt.hashpw(
        #     data['password'].encode('utf-8'), bcrypt.gensalt())
        # decoded_hashed_pw = hashed_password.decode('utf-8')

        if Customer.objects.filter(Q(email=data['email']) | Q(phone_no=data['phone_no'])).exists():
            return Response({'message': "EMAIL_OR_PHONE_EXISTS"}, status=status.HTTP_409_CONFLICT)

        try:
            serializer = CustomerSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({'message': 'SIGNUP_SUCCESS', "email": user.email}, status=status.HTTP_200_OK)
            else:
                return Response({'message': "SIGNUP_FAILED"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print(ex)
            return Response({'message': "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 이메일 찾기
class FindEmailView(APIView):
    # 조회 get id값으로 !get_all 보내면 전체 조회 특정 아이디 보내면 해당 아이디 정보 반환
    def post(self, request):
        data = json.loads(request.body)

        if Customer.objects.filter(phone_no=data['phone_no']).exists():
            user_data = Customer.objects.get(phone_no=data['phone_no'])
            return Response({'message': "EMAIL_FOUND_SUCCESS",
                             'email': user_data.email}, status=status.HTTP_200_OK)

        else:
            return Response({'message': "USER_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

# 비번 찾기


class FindPwView(APIView):
    # 이메일 전화번호 전달받아 해당 이메일, 전화번호를 가진 유저의 비밀번호 변경
    def post(self, request):
        data = json.loads(request.body)

        if Customer.objects.filter(email=data['email']).exists():
            user_data = Customer.objects.get(email=data['email'])

        if user_data.phone_no == data['phone_no']:
            # Update fields from request
            hashed_password = bcrypt.hashpw(
                data['password'].encode('utf-8'), bcrypt.gensalt())
            pw = hashed_password.decode('utf-8')
            setattr(user_data, 'password', pw)
            print(user_data.password)
            # Save the updated instance
            user_data.save()
            return Response({'message': "PASSWORD_CHANGE_SUCCESS"}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "USER_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)


class EmailSendView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        code = random.sample(range(10), 6)
        code = ''.join(map(str, code))

        existFlag = EmailCode.objects.filter(user_email=data['email']).exists()
        if not existFlag:
            EmailCode(
                user_email=data['email'],
                user_code=code
            ).save()

            try:
                email_validate(data['email'], code)
                return Response({'message': "EMAIL_SENT_SUCCESS"}, status=status.HTTP_200_OK)
            except:
                return Response({'message': "EMAIL_SENDING_FAILED"}, status=status.HTTP_400_BAD_REQUEST)

        elif existFlag:
            email_code = EmailCode.objects.get(user_email=data["email"])
            email_code.delete()

            EmailCode(
                user_email=data['email'],
                user_code=code
            ).save()
            try:
                email_validate(data['email'], code)
                return Response({'message': "EMAIL_RESENT_SUCCESS"}, status=status.HTTP_200_OK)
            except:
                return Response({'message': "EMAIL_SENDING_FAILED"}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerifyView(APIView):
    def post(self, request):
        data = json.loads(request.body)

        if EmailCode.objects.filter(user_email=data["email"]).exists():
            email_code = EmailCode.objects.get(user_email=data["email"])
            try:
                if email_code.user_code == data["user_code"]:
                    email_code.delete()
                    return Response({'message': "EMAIL_VERIFICATION_SUCCESS"}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': "INCORRECT_EMAIL_VERIFICATION"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'message': "EMAIL_VERIFICATION_FAILED"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    # def post(self, request):
    #     data = json.loads(request.body)

    #     try:
    #         existFlag = Customer.objects.filter(email = data['email']).exists()
    #         if existFlag:
    #             customer = Customer.objects.get(email = data["email"])
    #             customer.delete()
    #             try:
    #                 Customer(
    #                     email    = data['email'],
    #                     password    = data['password'],
    #                     name = data['name'],
    #                     phone_no = data['phone_no'],
    #                     user_type = data['user_type'],
    #                     sex = data['sex'],
    #                     age = data['age'],
    #                     nickname = data['nickname']
    #                 ).save()
    #                 return JsonResponse({'message':"register success"}, status=200)
    #             except:
    #                 return JsonResponse({'message' : "REGISTER ERROR"},status =400)
    #         else:
    #             return JsonResponse({'message' : "email not exist"},status =400)
    #     except:
    #         return JsonResponse({'message' : "INVALID_KEYS"},status =400)
    def patch(self, request):
        data = json.loads(request.body)

        # Check if customer exists
        customer = Customer.objects.get(email=data['email'])
        if not customer:
            return Response({'message': 'USER_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Update fields from request
            customer_attribute = ['nickname', 'phone_no', 'age', 'sex']
            for field in customer_attribute:
                setattr(customer, field, data[field])
            print(customer.nickname)
            # Save the updated instance
            customer.save()

            return Response({'message': 'PROFILE_UPDATE_SUCCESS'}, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class CreateUserKeywords(APIView):

        # try:
        #     user_id = Customer.objects.get(email = data['email'])
        #     if not UserKeywords.objects.get(user_id = user_id).exists():
        #             try:
        #                 UserKeywords.objects.create(
        #                     user_id=user_id,
        #                     beverage=data.get('beverage'),
        #                     dessert=data.get('dessert'),
        #                     various_menu=data.get('various_menu'),
        #                     special_menu=data.get('special_menu'),
        #                     large_store=data.get('large_store'),
        #                     background=data.get('background'),
        #                     talking=data.get('talking'),
        #                     concentration=data.get('concentration'),
        #                     trendy_store=data.get('trendy_store'),
        #                     gift_packaging=data.get('gift_packaging'),
        #                     parking=data.get('parking'),
        #                     price=data.get('price')
        #                 )

        #                 return JsonResponse({'message': "User Keywords Created Successfully"}, status=200)
        #             except:
        #                 return JsonResponse({'message' : "Create User Keywords ERROR"},status =400)
        #     else:
        #         return JsonResponse({'message' : "User keywords already exist"},status =400)

        # except:
        #     return JsonResponse({'message' : "INVALID_KEYS"},status =400)


class UserKeyword(APIView):
    def get(self, request):
        # Check if customer exists
        email = request.GET.get('email')
        try:
            customer = Customer.objects.get(email=email)
            user_keywords = UserKeywords.objects.get(user=customer)

            return Response({'message': 'USER_KEYWORDS_EXISTS', 'keyword': UserKeywordsSerializer(user_keywords).data}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'USER_OR_KEYWORD_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = json.loads(request.body)
        user_keyword_value = list(data['user_keyword_value'])

        try:
            customer = Customer.objects.get(email=data['email'])
        except:
            return Response({'message': 'USER_NOT_FOUND'}, status=404)

        if UserKeywords.objects.filter(user=customer):
            return Response({'message': "USER_KEYWORDS_EXISTS'"}, status=status.HTTP_409_CONFLICT)

        try:
            UserKeywords.objects.create(
                user=customer,
                beverage=user_keyword_value[0],
                dessert=user_keyword_value[1],
                various_menu=user_keyword_value[2],
                special_menu=user_keyword_value[3],
                large_store=user_keyword_value[4],
                background=user_keyword_value[5],
                talking=user_keyword_value[6],
                concentration=user_keyword_value[7],
                trendy_store=user_keyword_value[8],
                gift_packaging=user_keyword_value[9],
                parking=user_keyword_value[10],
                price=user_keyword_value[11]
            )
            return Response({'message': "USER_KEYWORDS_CREATED_SUCCESS"}, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        data = json.loads(request.body)
        user_keyword_value = list(data['user_keyword_value'])

        # Check if customer exists
        try:
            customer = Customer.objects.get(email=data["email"])
            user_keywords = UserKeywords.objects.get(user=customer)
        except:
            return Response({'message': 'USER_OR_KEYWORD_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

        # Update fields from request
        try:
            user_keyword_attribute = ['beverage', 'dessert', 'various_menu', 'special_menu', 'large_store',
                                      'background', 'talking', 'concentration', 'trendy_store', 'gift_packaging', 'parking', 'price']
            for idx in range(len(user_keyword_attribute)):
                setattr(user_keywords,
                        user_keyword_attribute[idx], user_keyword_value[idx])

            # Save the updated instance
            user_keywords.save()
            return Response({'message': 'USER_KEYWORDS_UPDATE_SUCCESS'}, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # try:
        #     existFlag = Customer.objects.filter(email = data['email']).exists()
        #     if existFlag:
        #         user_keywords = UserKeywords.objects.get(user_id = data['user_id'])

        #         try:
        #             # Update fields from request
        #             user_keywords.beverage = data['beverage']
        #             user_keywords.dessert = data['dessert']
        #             user_keywords.various_menu = data['various_menu']
        #             user_keywords.special_menu = data['special_menu']
        #             user_keywords.large_store = data['large_store']
        #             user_keywords.background = data['background']
        #             user_keywords.talking = data['talking']
        #             user_keywords.concentration = data['concentration']
        #             user_keywords.trendy_store = data['trendy_store']
        #             user_keywords.gift_packaging = data['gift_packaging']
        #             user_keywords.parking = data['parking']
        #             user_keywords.price = data['price']

        #             # Save the updated instance
        #             user_keywords.save()
        #             return JsonResponse({'message': 'UserKeywords updated successfully'}, status=200)
        #         except:
        #             return JsonResponse({'message' : "UserKeywords updated ERROR"},status =400)
        # except:
        #     return JsonResponse({'message' : "INVALID_KEYS"},status =400)


# class IsKeywordExist(APIView):


# class CafeInfoView(View):
#     def post(self, request):
#         print(request)
#         data = json.loads(request.body)

#         try:
#            if CafeInfo.objects.filter(cafe_id = data['cafe_id']).exists():
#                 cafe_info = CafeInfo.objects.get(cafe_id = data['cafe_id'])
#                 try:
#                     serialzer = Cafe_info_serializer(cafe_info)
#                     return JsonResponse(serialzer.data, status=200)

#                 except:
#                     return JsonResponse({'message' : "RETURN ERROR"},status =400)
#            else:
#             return JsonResponse({'message' : "NONE EXIST ERROR"},status =400)
#         except:
#             return JsonResponse({'message' : "INVALID_KEYS"},status =400)
