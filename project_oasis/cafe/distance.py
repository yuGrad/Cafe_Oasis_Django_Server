from haversine import haversine, Unit

# 두 위치 간 거리를 구하는 함수
def calculate_distance(user_location, cafe_location):
    distance = haversine(user_location, cafe_location, unit=Unit.KILOMETERS)
    return distance

#현재 사용자 위치 기준 3km 이내 카페의 id list 반환 함수
def get_cafe_list_base_location(user_location, cafe_objects_all, max_distance=3.0):
    nearby_cafes = []
    for cafe in cafe_objects_all:
        cafe_location = (cafe.latitude, cafe.longitude)
        distance = calculate_distance(user_location, cafe_location)
        if distance <= max_distance:  # if the cafe is within 3 kilometers of the user's location
            nearby_cafes.append(cafe.cafe_id)

    return nearby_cafes
