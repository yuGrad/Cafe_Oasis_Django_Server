
# from haversine import haversine, Unit
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.ensemble import RandomForestClassifier

# from django.apps import apps
# import pandas as pd
# import json
# import pickle

# cafe_df = pd.read_csv("/home/ubuntu/django_aws/oasis_venv/project_oasis/cafe/cafe_df.csv", encoding="utf-8")
# cafe_value = pd.read_csv("/home/ubuntu/django_aws/oasis_venv/project_oasis/cafe/cafe_value.csv", encoding="utf-8")
# cafe_without_value = pd.read_csv("/home/ubuntu/django_aws/oasis_venv/project_oasis/cafe/cafe_without_keywords.csv", encoding="utf-8")
# #cafe_value_x = cafe_value.drop(columns=['cafe_id'])
# with open('/home/ubuntu/django_aws/oasis_venv/project_oasis/cafe/model.pkl', 'rb') as f:
#             rfc_model = pickle.load(f)

# # 두 위치 간 거리를 구하는 함수
# def calculate_distance(user_location, cafe_location):
#     distance = haversine(user_location, cafe_location, unit=Unit.KILOMETERS)
#     return distance

# #현재 사용자 위치 기준 3km 이내 카페의 id list 반환 함수
# def get_cafe_list_base_location(user_location, max_distance=3.0):
#     nearby_cafes = []
#     for idx, row in cafe_df.iterrows():
#         cafe_location = (row['위도'], row['경도'])
#         distance = calculate_distance(user_location, cafe_location)
#         if distance <= max_distance:
#             nearby_cafes.append(row['cafe_id'])

#     return nearby_cafes

# def create_user_cafe_profile_df(user_cafe_profile):
#     cafe_value_columns_list = ['beverage', 'dessert', 'various_menu', 'special_menu', 'large_store', 'background', 'talking', 'concentration', 'trendy_store']
#     return pd.DataFrame([user_cafe_profile], columns=cafe_value_columns_list )

# def classify_with_random_forest(user_cafe_profile):
#     # 랜덤 포레스트 모델로 카페 데이터 학습 -> grid search 로 찾은 최적의 파라미터 사용
#     return  rfc_model.predict(create_user_cafe_profile_df(user_cafe_profile))

# def calculate_cosine_similarity(neary_cafes_value, user_cafe_profile):
#     return cosine_similarity(neary_cafes_value, create_user_cafe_profile_df(user_cafe_profile))


# def recommend_cafe_base_keyworkd(user_cafe_profile, user_location, range=3):
#     #근처 카페 id list로 데이터 프레임 불러오기
#     neary_cafes_list = get_cafe_list_base_location(user_location, range)
#     neary_cafes_value_df = cafe_value[cafe_value['cafe_id'].isin(neary_cafes_list)]
    
#     #랜덤 포레스트로 분류 과정에 불필요한 열 값들은 제거
#     neary_cafes_value_df = neary_cafes_value_df.drop(columns=['cafe_id', 'low_price', 'high_price', 'parking', 'gift_packaging', 'common_keywords'])

#     #랜덤 포레스트 모델로 라벨 값 분류해서 라벨에 해당하는 근처 카페 추출
#     classified_label = classify_with_random_forest(user_cafe_profile)
#     neary_cafes_value_df = neary_cafes_value_df[neary_cafes_value_df['label'] == classified_label[0]]

#     print(len(neary_cafes_list))

#     #코사인 유사도 계산 과정에 불필요한 열 값들은 제거
#     # neary_cafes_value_df = neary_cafes_value_df.drop(columns=['label'])

#     # #사용자 선호 카페 프로필 값으로 코사인 유사도 계산
#     # similarities = calculate_cosine_similarity(neary_cafes_value_df, user_cafe_profile)
#     # neary_cafes_value_df['similarity'] = similarities

# 	# #코사인 유사도가 가장 높은 2개의 카페를 리스트에 저장
#     # top_two_cafe_df = neary_cafes_value_df['similarity'].nlargest(2).index.to_list()
#     # recommend_cafe_list = cafe_value.loc[top_two_cafe_df, 'cafe_id'].to_list()

# 	# #키워드와 별점이 존재하지 않는 카페 리스트에서 랜덤으로 카페 하나를 추출해 리스트에 저장
#     # neary_cafes_value_df = cafe_without_value.sample(1)
#     # recommend_cafe_list.append(neary_cafes_value_df['cafe_id'].values[0])

#     # recommend_cafe = cafe_df.iloc[recommend_cafe_list]
	
#     # return recommend_cafe

# recommend_cafe_df = recommend_cafe_base_keyworkd([0, 3, 1, 3, 1, 3, 1, 1, 3], [35.8680733, 128.5995891])
# print(recommend_cafe_df)
# #

#json_data = recommend_cafe_df.to_json(orient='records')
# # json.loads(json_data)


import csv
from django.db import transaction
from cafe.models import Cafe, CafeKeywords

#카페 csv 파일을 Cafe 테이블에 삽입
def import_cafe_data(csv_filepathname):
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    next(dataReader, None)  # skip the headers
    with transaction.atomic():
        for row in dataReader:
            cafe = Cafe()
            cafe.cafe_id = int(row[0]) + 1
            cafe.business_name = row[1]
            cafe.cafe_name = row[2]
            cafe.cafe_rating = row[3]
            cafe.visitor_reviews = row[4]
            cafe.blog_reviews = row[5]
            cafe.address = row[6]
            cafe.business_hours = row[7]
            cafe.cafe_phone_no = row[8]
            #cafe.cafe_info = row[9]
            cafe.latitude = float(row[11])
            cafe.longitude = float(row[12])
            cafe.save()

#카페 값 csv 파이을 CafeKeywords 테이블에 삽입
def import_cafe_value(csv_filepathname):
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    next(dataReader, None)  # skip the headers
    with transaction.atomic():
        for row in dataReader:
            cafe_keywords = CafeKeywords()
            cafe_keywords.cafe = Cafe.objects.get(cafe_id = int(row[0]) + 1)
            cafe_keywords.beverage = row[1]
            cafe_keywords.dessert = row[2]
            cafe_keywords.various_menu = row[3]
            cafe_keywords.special_menu = row[4]
            cafe_keywords.large_store = row[5]
            cafe_keywords.background = row[6]
            cafe_keywords.talking = row[7]
            cafe_keywords.concentration = row[8]
            cafe_keywords.trendy_store = row[9]
            cafe_keywords.label = row[10]
            gift_packaging = row[14]
            if float(gift_packaging) > 0:
                cafe_keywords.gift_packaging = True
            else:
                cafe_keywords.gift_packaging = False
            parking = row[13]
            if float(parking) > 0:
                cafe_keywords.parking = True
            else:
                cafe_keywords.parking = False
            low_price, high_price = row[11], row[12]
            if float(low_price) < -0.75 or float(high_price) > 0.75:
                cafe_keywords.price = True
            else:
                cafe_keywords.price = False
            cafe_keywords.common_keywords = row[15]
            cafe_keywords.save()

#카페 이미지 경로를 Cafe 테이블에 업데이트
def import_cafe_img(csv_filepathname):
    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    next(dataReader, None)  # skip the headers
    with transaction.atomic():
        for row in dataReader:
            cafe = Cafe.objects.get(cafe_id=int(row[0]))
            cafe.cafe_image = row[1]
            cafe.save()
    

import_cafe_value("/home/du/duhyun/django/cafe_oasis/Cafe_Oasis_Django_Server/project_oasis/cafe/ML/cafe_value.csv")
import_cafe_data("/home/du/duhyun/django/cafe_oasis/Cafe_Oasis_Django_Server/project_oasis/cafe/ML/cafe_df.csv")
import_cafe_img("/home/du/duhyun/django/cafe_oasis/Cafe_Oasis_Django_Server/project_oasis/cafe/ML/merged_df.csv")