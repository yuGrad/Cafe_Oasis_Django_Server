# \***\*Oasis: A Content-Based Café Recommendation System\*\***

---

영남대학교 컴퓨터공학과 4학년 전공과목 종합설계과제 프로젝트

개발기간: 2023.03 ~ 2023.11

---

![image](https://github.com/yuGrad/Cafe_Oasis_Django_Server/assets/102767676/69ac6783-0d2b-4a1f-9896-4be2ab28aac0)

### 개발 멤버

---

|        | 우정현                             | 김두현                        | 유아성                     | 이다해                             |
| ------ | ---------------------------------- | ----------------------------- | -------------------------- | ---------------------------------- |
| github | https://github.com/CommitTheKermit | https://github.com/iamdudumon | https://github.com/YuASung | https://github.com/iamnotyourocean |
| 소속   | 영남대학교 컴퓨터공학과            | 영남대학교 컴퓨터공학과       | 영남대학교 컴퓨터공학과    | 영남대학교 컴퓨터공학과            |
| 역할   | 조장, backend + frontend           | backend                       | frontend                   | frontend                           |

- 프로젝트 소개
  ## 프로젝트 소개
  ***
  ‘카페 오아시스’ 는 사용자의 카페 취향 키워드를 활용한 콘텐츠 기반 카페 추천 시스템이다.
  오아시스라는 단어는 여행자들이 뜨거운 사막에서 신선한 물과 그늘을 찾듯이, 카페를 찾는 이들에게 좋은 음료와 새로운 경험을 선사한다는 의미를 담고 있다.
  이 시스템의 목표는 사용자들이 카페를 찾는 데에 있어 다양하고 고갈되지 않은 새로운 경험을 제공하는 것이다.
  ‘카페 오아시스’를 통해 사용자는 취향에 맞는 카페를 추천받고 추천 결과에 따른 사용자의 만족도를 수집해 시스템에 반영해 더 풍부한 경험을 사용자에게 제공하는 것을 목표로 한다.
  ### 개발 목표
  - 사용자들이 자신의 취향과 필요에 맞는 카페를 쉽게 찾을 수 있도록 데이터 기반의 사용자 맞춤
    형 추천 서비스를 제공하여 사용자들이 더욱 만족스러운 카페 경험을 할 수 있도록 한다.
  - 사용자와 상호작용을 하기 위한 애플리케이션, 앱에 필요한 정보를 제공하고 저장하는 서버 및 데이터베이스로 나뉜 소프트웨어를 개발한다.
  - 카페와 사용자 간의 상호작용을 촉진하여, 카페 문화의 활성화와 소통을 증진한다.
  ### 주요 기능
  1. 사용자 회원가입, 로그인
  2. 사용자 정보 수정, 이메일/비밀번호 찾기
  3. 실시간 사용자 현재 위치 연동
  4. 카페 추천
     1. based on Keywords
     2. based on Ratings
  5. 추천받은 카페 평점 저장
  6. 카페 영수증 인식: 자동으로 카페 방문 이력 저장
  7. 사용자 선호 카페 키워드 프로필 생성/수정
- 서버 실행 방법
  ## 백엔드 \***\*설치 및 실행 방법\*\***
  ***
  ### \* 해당 설치 및 실행 방법은 로컬 호스트에서 테스트하는 것을 전제로 하고 있습니다. 어플리케이션이 필요로 하는 서버는 AWS에서 실행 중입니다.
  ### \***\*Dependencies\*\***
  - Python 3.10.6
  - Django==4.2.1
  - djangorestframework==3.14.0
  ### Installation
  1. Clone the repository
  2. Move the project file
  3. Install the dependencies
  4. migarte database
  5. Run the server
  ```bash
  $ git clone https://github.com/CommitTheKermit/django_aws
  $ cd oasis_venv
  pip install -r requirements.txt
  $ cd project_oasis
  $ python3 manage.py makemigrations
  $ python3 manage.py migrate
  $ python3 manage.py runserver 0.0.0.0:8000
  ```
  → http://localhost:8000/ 으로 접속

---

- Stacks
  ## Stacks
  ***
  ### Environment
  - VISUAL STUDIO CODE
  - GIT
  - GITHUB
  - AWS EC2
  - AWS ROUTE53
  ### Development
  - Python3
    - Django
    - nginx
    - guicorn
  - MariaDB
  - Java
  - Android Studio
  ### Communication
  - Notion
  - Discode
- 아키텍쳐
  ## 디렉토리 구조
  ```markdown
  project_oasis/
  ├── project_oasis
  │ ├── cafe
  │ │ ├── admin.py
  │ │ ├── apps.py
  │ │ ├── **init**.py
  │ │ ├── migrations
  │ │ ├── ML
  │ │ ├── models.py
  │ │ ├── **pycache**
  │ │ ├── serializer.py
  │ │ ├── tests.py
  │ │ ├── urls.py
  │ │ └── views.py
  │ ├── history
  │ │ ├── admin.py
  │ │ ├── apps.py
  │ │ ├── **init**.py
  │ │ ├── migrations
  │ │ ├── models.py
  │ │ ├── **pycache**
  │ │ ├── tests.py
  │ │ ├── urls.py
  │ │ └── views.py
  │ ├── manage.py
  │ ├── project_oasis
  │ │ ├── asgi.py
  │ │ ├── **init**.py
  │ │ ├── **pycache**
  │ │ ├── settings.py
  │ │ ├── urls.py
  │ │ └── wsgi.py
  │ └── users
  │ ├── admin.py
  │ ├── apps.py
  │ ├── email_verification.py
  │ ├── **init**.py
  │ ├── migrations
  │ ├── models.py
  │ ├── **pycache**
  │ ├── serializer.py
  │ ├── tests.py
  │ ├── urls.py
  │ └── views.py
  ├── README.md
  ├── requirements.txt
  └── temp
  └── migration
  ├── cafe
  ├── history
  └── users
  ```
- Recommend System

  ## Recommend System

  ***

  ### 카페 데이터 수집

  1. 대구 지역으로 제한해서 카페 데이터 수집
  2. 카페 데이터는 네이버 지도에서 해당 카페를 검색한 결과를 크롤링해서 수집
  3. 카페 데이터 크롤링 수집 정보 범위 -> (사업자명, 카페명, 카페이름, 별점, 방문자리뷰수, 블로그리뷰수, 주소, 영업시간, 전화번호, 설명, 키워드)
  4. 크롤링을 통해 수집한 카페 데이터를 csv 파일로 변환

  ### 카페 데이터 전처리

  1. 각 컬럼의 대한 결측치를 0 이나 다른 값으로 처리
  2. 주소 컬럼이 결측치인 카페 행은 제거
  3. 주소와 전화번호가 중복인 카페 행이 존재 -> 주소와 전화번호가 다른 카페는 다른 카페로 분류
  4. 구글 GeoCoder를 사용해 카페의 주소를 통해 위도, 경도 수집 -> 카페 데이터 프레임에 새로운 컬럼으로 추가
  5. 카페 키워드 중 카페의 특징을 반영하는데 불필요한 키워드는 삭제 -> 키워드가 없는 카페 행끼리 별도로 저장
  6. 남은 키워드들 중에 특징을 반영할 수 있는 유사한 키워드끼리 카테고리고 묶음.

  ```python
  categories = {
      # 음료, 음식
      'beverage': ['차가 맛있어요', '음료가 맛있어요', '커피가 맛있어요'],
      'dessert': ['디저트가 맛있어요', '빵이 맛있어요', '음식이 맛있어요'],
      'various_menu': ['메뉴 구성이 알차요', '종류가 다양해요'],
      'special_menu': ['특별한 메뉴가 있어요', '특색 있는 제품이 많아요'],

      # 시설
      'large_store': ['매장이 넓어요', '룸이 잘 되어있어요', '공간이 넓어요'],
      'background': ['야외 공간이 멋져요', '뷰가 좋아요'],
      'parking': ['주차하기 편해요'],

      # 분위기
      'talking': ['분위기가 편안해요', '대화하기 좋아요', '아늑해요'],
      'concentration' : ['집중하기 좋아요', '차분한 분위기에요',  '오래 머무르기 좋아요'],
      'trendy_store': ['트렌디해요', '사진이 잘 나와요', '음악이 좋아요', '인테리어가 멋져요', '컨셉이 독특해요'],

      # 기타
      'gift_packaging': ['선물하기 좋아요', '포장이 깔끔해요'],
      'low_price': ['가격이 합리적이에요', '가성비가 좋아요', '양이 많아요'],
      'high_price': ['특별한 날 가기 좋아요', '비싼 만큼 가치있어요'],

      'common_keywords': ['좌석이 편해요', '친절해요', '화장실이 깨끗해요', '시설이 깔끔해요', '매장이 청결해요'] # '차가 맛있어요', '음료가 맛있어요', '커피가 맛있어요',
  }
  ```

  1. 공통 키워드는 카페의 특징이나 취향의 척도가 아닌 대부분의 사용자가 카페를 방문할 때 갖는 기본적인 기대치이므로 별도의 카테고리로 분류.
  2. 카페 데이터 프레임의 각 행에서 카테고리 별 점수를 환산 -> 카페의 각 키워드가 속한 카테고리에 가중치를 계속 합하는 방식 사용.
  3. 카페 각 키워드의 원 가중치를 그대로 사용하면 방문자리뷰가 많은 카페가 압도적으로 높은 가중치를 가짐 -> 각 카페의 특징을 반영하지 못 함
  4. 각 카테고리의 가중치 값의 합으로 각 카테고리를 나눔 -> 카테고리 별 비율을 계산, 공통 키워드 값은 성능의 지표로 사용하기 위해 비율이 아닌 방문자수로 나눔 -> "방문자 1명은 평균적으로 공통 키워드에 대해 이 정도의 점수를 부여했다" 의 의미로 사용
  5. 카페 데이터 프레임의 'beverage', 'dessert', 'various_menu', 'special_menu', 'large_store', 'background', 'talking', 'concentration', 'trendy_store' 컬럼은 1~4범위의 Min-Max 정규화 적용
  6. 'low_price', 'high_price', 'parking', 'gift_packaging', 'common_keywords' 컬럼은 z-score 정규화 -> 해당 각 카테고리의 평균 값을 이용해 0 or 1의 값을 가지기 위해서

  ### 카페 추천 알고리즘

  1. 클러스터링
     - 카페 데이터 프레임의 각 카테고리의 가중치로 유사한 값을 가진 카페들끼리 군집 -> k-means++ 모델 사용
     - elbow method를 사용해 적절한 n_clusters 파라미터 값을 찾음 -> 8개의 군집으로 분류
     - 8개의 군집으로 분류한 결과를 카페 데이터 프레임에 'label' 컬럼으로 추가
     - 여러번의 클러스터링을 통해 카페 수가 적은 클러스터의 일부 카페를 이상치로 분류해 제거
  2. 라벨 예측(분류)
     - 랜덤 포레스트 모델에 라벨 값을 분류한 카페 데이터를 학습시켜 라벨을 분류하는 모델 생성.
     - 사용자는 app에서 선호 카페 키워드 프로필을 생성
     - 선호 카페 키워드 프로필 값으로 카페 라벨을 분류, 예측
  3. 코사인 유사도 계산
     - 사용자의 현재 위치 기반으로 3km 안에 카페 + 분류된 라벨 값을 가친 카페만을 데이터베이스에서 불러옴.
     - 해당 카페들과 사용자의 선호 카페 키워드 값과 코사인 유사도 계산
     - 유사도가 가장 큰 2개의 카페의 id를 추천 리스트에 저장
  4. 카페 추천
     - 코사인 유사도가 가장 큰 2개의 카페와 키워드 값이 없는 카페 중 하나를 랜덤으로 추천 -> 카페 추천의 다양성을 위해
     - 추가적으로 사용자 근처 카페 중 별점과 공통 키워드의 합이 가장 큰 3개까지의 카페를 추천
     <aside>
     💡 업데이트 방향

  - 현재는 Contents-based Recommender System을 기반으로 추천 시스템을 구현
  - 추후 사용자의 카페 방문 기록과 평점 데이터가 수집되면 카페 키워드와 사용자 데이터를 결합한 Hybrid Recommender System 방식의 추천 시스템으로 업데이트 예정
  </aside>
