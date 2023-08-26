from django.urls import path
from .views import LoginView, SignUpView, FindEmailView, FindPwView, EmailSendView
from .views import EmailVerifyView, EditProfileView, CreateUserKeywords, UpdateUserKeywords
from .views import isKeywordExist

urlpatterns = [
    path('login', LoginView.as_view()),
    path('signup', SignUpView.as_view()),
    path('findemail', FindEmailView.as_view()),
    path('findpw', FindPwView.as_view()),
    path('mailsend', EmailSendView.as_view()),
    path('mailverify',EmailVerifyView.as_view()),
    path('profileEdit', EditProfileView.as_view()),
    path('profile/keyword/create', CreateUserKeywords.as_view()),
    path('profile/keyword/update', UpdateUserKeywords.as_view()),
    path('profile/keyword/isexist', isKeywordExist.as_view()),
    # path('cafeinfo', CafeInfoView.as_view()),
]