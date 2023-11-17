import os
import django
import sys
import csv

sys.path.append(
    '/home/du/.duhyun/cafe_oasis/Cafe_Oasis_Django_Server/project_oasis')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_oasis.settings')
django.setup()


# 카페 csv 파일을 Cafe 테이블에 삽입


def import_cafe_data(csv_filepathname):
    from cafe.models import Cafe
    dataReader = csv.reader(open(csv_filepathname),
                            delimiter=',', quotechar='"')
    next(dataReader, None)  # skip the headers
    for idx, row in enumerate(dataReader):
        cafe = Cafe()
        cafe.cafe_id = idx + 1
        # cafe.business_name = row[1]
        cafe.cafe_name = row[0]
        cafe.cafe_rating = row[2]
        cafe.visitor_reviews = int(row[3])
        cafe.blog_reviews = int(row[4])
        cafe.address = row[5]
        cafe.business_hours = row[6]
        cafe.cafe_phone_no = row[7]
        cafe.cafe_info = row[8]
        cafe.cafe_image = str(row[12])
        try:
            cafe.latitude = float(row[13])
            cafe.longitude = float(row[14])
        except Exception as ex:
            print(idx, ex)
            cafe.latitude = 0.0
            cafe.longitude = 0.0
        cafe.save()

# 카페 값 csv 파이을 CafeKeywords 테이블에 삽입


def import_cafe_value(csv_filepathname):
    from cafe.models import Cafe, CafeKeyword
    dataReader = csv.reader(open(csv_filepathname),
                            delimiter=',', quotechar='"')
    next(dataReader, None)  # skip the headers
    for idx, row in enumerate(dataReader):
        try:
            cafe_keywords = CafeKeyword()
            cafe_keywords.cafe = Cafe.objects.get(cafe_id=int(row[0]) + 1)

            cafe_keywords.dessert = row[1]
            cafe_keywords.various_menu = row[2]
            cafe_keywords.special_menu = row[3]
            cafe_keywords.large_store = row[4]
            cafe_keywords.background = row[5]

            cafe_keywords.talking = row[6]
            cafe_keywords.trendy_store = row[7]
            cafe_keywords.concentration = row[8]

            low_price, high_price = row[9], row[10]
            if float(low_price) < -0.75 or float(high_price) > 0.75:
                cafe_keywords.price = True
            else:
                cafe_keywords.price = False

            gift_packaging = row[11]
            if float(gift_packaging) > 0:
                cafe_keywords.gift_packaging = True
            else:
                cafe_keywords.gift_packaging = False
            parking = row[12]
            if float(parking) > 0:
                cafe_keywords.parking = True
            else:
                cafe_keywords.parking = False

            cafe_keywords.beverage = row[13]
            cafe_keywords.clean_store = row[14]
            cafe_keywords.service = row[15]
            cafe_keywords.label = row[16]
            cafe_keywords.save()
        except Exception as ex:
            print(idx, ex)
            continue


# 카페 이미지 경로를 Cafe 테이블에 업데이트


import_cafe_data(
    "cafe/ML/cafe_df.csv")
import_cafe_value(
    "cafe/ML/cafe_value_df.csv")
