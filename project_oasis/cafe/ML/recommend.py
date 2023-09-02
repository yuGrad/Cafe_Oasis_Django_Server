from sklearn.metrics.pairwise import cosine_similarity
from django.apps import apps
import pandas as pd
from django_pandas.io import read_frame

app_config = apps.get_app_config('cafe')
rfc_model = app_config.rfc_model


def create_user_cafe_profile_df(user_cafe_profile):
    cafe_value_columns_list = ['beverage', 'dessert', 'various_menu', 'special_menu', 'large_store', 'background', 'talking', 'concentration', 'trendy_store']
    return pd.DataFrame([user_cafe_profile], columns=cafe_value_columns_list )

def classify_with_random_forest(neary_cafes_value, user_cafe_profile):
    # 랜덤 포레스트 모델로 카페 데이터 학습 -> grid search 로 찾은 최적의 파라미터 사용
    return  rfc_model.predict(create_user_cafe_profile_df(user_cafe_profile))

def calculate_cosine_similarity(neary_cafes_value, user_cafe_profile):
    return cosine_similarity(neary_cafes_value, create_user_cafe_profile_df(user_cafe_profile))

#사용자의 선호 카페 프로필과 현재 위치 기반으로 카페 추천
def recommend_cafe_base_keyworkd(user_cafe_profile, nearby_cafes_value):
    #쿼리 셋을 데이터 프레임으로 변환
    nearby_cafes_value_df = read_frame(nearby_cafes_value)
    
    #랜덤 포레스트로 분류 과정에 불필요한 열 값들은 제거
    cafe_id_df = nearby_cafes_value_df['cafe']
    nearby_cafes_value_df = nearby_cafes_value_df.drop(columns=['cafe', 'price', 'parking', 'gift_packaging', 'common_keywords'])

    #랜덤 포레스트 모델로 라벨 값 분류해서 라벨에 해당하는 근처 카페 추출
    classified_label = classify_with_random_forest(nearby_cafes_value_df, user_cafe_profile)
    nearby_cafes_value_df['cafe_id'] = [ cafe_id for cafe_id in cafe_id_df]
    nearby_cafes_value_df = nearby_cafes_value_df[nearby_cafes_value_df['label'] == str(classified_label[0])]

    #코사인 유사도 계산 과정에 불필요한 열 값들은 제거
    cafe_ids = nearby_cafes_value_df['cafe_id']
    nearby_cafes_value_df = nearby_cafes_value_df.drop(columns=['cafe_id', 'label'])
    
    #사용자 선호 카페 프로필 값으로 코사인 유사도 계산
    similarities = calculate_cosine_similarity(nearby_cafes_value_df, user_cafe_profile)
    nearby_cafes_value_df['similarity'] = similarities

    nearby_cafes_value_df['cafe_id'] = cafe_ids    

	#코사인 유사도가 가장 높은 2개의 카페를 리스트에 저장
    top_similarities = nearby_cafes_value_df['similarity'].nlargest(2)
    recommend_cafe_list = nearby_cafes_value_df.loc[top_similarities.index, 'cafe_id'].tolist()


    return recommend_cafe_list

#별점과 Oaiss 자체의 기준으로 점수를 채점해 추천
def recommend_cafe_base_rating(nearby_cafes_value):
    #쿼리 셋을 데이터 프레임으로 변환
    nearby_cafes_value_df = read_frame(nearby_cafes_value)

     #근처 카페 id list로 데이터 프레임 불러오기 + 별점도 불러오기
    cafe_rating_df = pd.DataFrame([cafe_keywords.cafe.cafe_rating for cafe_keywords in nearby_cafes_value], columns=['cafe_rating'])
    nearby_cafes_value_df = pd.concat([nearby_cafes_value_df, cafe_rating_df], axis=1)

    cafe_id_df = nearby_cafes_value_df['cafe']

    #필요한 값만 사용 + 계산을 위한 타입 변환
    nearby_cafes_value_df = nearby_cafes_value_df[['common_keywords', 'cafe_rating']]
    nearby_cafes_value_df['cafe_rating'] = nearby_cafes_value_df['cafe_rating'].astype(float)
    
    # 공통 키워드 값과 별점 값의 총합이 가장 높은 top 3 추천
    top_three_cafe_df = nearby_cafes_value_df.sum(axis=1).nlargest(3)
    nearby_cafes_value_df['cafe_id'] = [ cafe_id for cafe_id in cafe_id_df]
    
    recommend_cafe_list = nearby_cafes_value_df.loc[top_three_cafe_df.index, 'cafe_id'].to_list()
    
    return recommend_cafe_list