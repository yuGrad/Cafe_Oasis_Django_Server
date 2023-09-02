import os
import django
import sys

sys.path.append('/home/du/duhyun/django/cafe_oasis/Cafe_Oasis_Django_Server/project_oasis')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_oasis.settings')
django.setup()

from cafe.models import Cafe, CafeKeywords
from django.db import transaction
import csv

# 카페 csv 파일을 Cafe 테이블에 삽입

def import_cafe_data(csv_filepathname):
    dataReader = csv.reader(open(csv_filepathname),
                            delimiter=',', quotechar='"')
    next(dataReader, None)  # skip the headers
    with transaction.atomic():
        for row in dataReader:
            cafe = Cafe()
            cafe.cafe_id = int(row[0]) + 1
            cafe.business_name = row[1]
            cafe.cafe_name = row[2]
            cafe.cafe_rating = row[3]
            cafe.visitor_reviews = int(row[4])
            cafe.blog_reviews = int(row[5])
            cafe.address = row[6]
            cafe.business_hours = row[7]
            cafe.cafe_phone_no = row[8]
            # cafe.cafe_info = row[9]
            cafe.latitude = float(row[11])
            cafe.longitude = float(row[12])
            cafe.save()

# 카페 값 csv 파이을 CafeKeywords 테이블에 삽입


def import_cafe_value(csv_filepathname):
    dataReader = csv.reader(open(csv_filepathname),
                            delimiter=',', quotechar='"')
    next(dataReader, None)  # skip the headers
    with transaction.atomic():
        for row in dataReader:
            cafe_keywords = CafeKeywords()
            cafe_keywords.cafe = Cafe.objects.get(cafe_id=int(row[0]) + 1)
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

# 카페 이미지 경로를 Cafe 테이블에 업데이트


def import_cafe_img(csv_filepathname):
    dataReader = csv.reader(open(csv_filepathname),
                            delimiter=',', quotechar='"')
    next(dataReader, None)  # skip the headers
    with transaction.atomic():
        for row in dataReader:
            cafe = Cafe.objects.get(cafe_id=int(row[0]))
            cafe.cafe_image = row[1]
            cafe.save()

import_cafe_data(
    "/home/du/duhyun/django/cafe_oasis/Cafe_Oasis_Django_Server/project_oasis/cafe/ML/cafe_info.csv")
import_cafe_value(
    "/home/du/duhyun/django/cafe_oasis/Cafe_Oasis_Django_Server/project_oasis/cafe/ML/cafe_value.csv")
import_cafe_img(
    "/home/du/duhyun/django/cafe_oasis/Cafe_Oasis_Django_Server/project_oasis/cafe/ML/cafe_image_path.csv")
