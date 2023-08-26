from django.apps import AppConfig
import pickle


class RecommendCafeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cafe'

    def ready(self):
        super().ready()

        #학습된 랜덤 포레스트 모델을 불러옴
        with open('/home/du/duhyun/django/cafe_oasis/Cafe_Oasis_Django_Server/project_oasis/cafe/ML/model.pkl', 'rb') as f:
            self.rfc_model = pickle.load(f)