from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

# https://velog.io/@kyleee/TIL61-Django-auth    password 관련 참고 사이트
# https://yonghyunlee.gitlab.io/python/user-extend/     로그인 확장
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#django.contrib.auth.models.PermissionsMixin    user 인증 공식문서

# # Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password, name, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The password field musb be set')
        if not name:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.name = name
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, name, **extra_fields):
        user = self.create_user(email, password, name, **extra_fields)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('1', 'Customer'),
        ('2', 'Employee'),
    ]

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(
        max_length=255, null=False, unique=True)
    # bcrypt를 사용해도 접두어가 존재할 수 있으므로 60자보다 길 수 있음
    password = models.CharField(max_length=128, null=False)
    name = models.CharField(max_length=255, null=False)
    phone_no = models.CharField(max_length=20, default='none')
    registration_date = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False) # permissionsmixin interface에서 제공하는 속성이므로 제거

    USERNAME_FIELD = 'email'

    # superuser 생성할 때 추가적으로 입력할 정보 항목
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    class Meta:
        db_table = 'User'


class Customer(User):
    SEX_CHOICES = [
        ('1', 'Male'),
        ('2', 'Female'),
    ]

    nickname = models.CharField(max_length=15)
    age = models.IntegerField()
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)

    def __str__(self):
        return f'{self.user_id}, {self.email}'

    class Meta:
        db_table = 'Customer'


class UserKeywords(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 4)]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    beverage = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    dessert = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    various_menu = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    special_menu = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    large_store = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    background = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    talking = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    concentration = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    trendy_store = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    gift_packaging = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    price = models.BooleanField(default=False)

    class Meta:
        db_table = 'UserKeywords'


class EmailCode(models.Model):
    user_email = models.EmailField(max_length=255, default='none')
    user_code = models.CharField(max_length=6)

    class Meta:
        db_table = 'EmailCode'
