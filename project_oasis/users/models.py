from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# # Create your models here.


class User(AbstractBaseUser):
    USER_TYPE_CHOICES = [
        ('1', 'Customer'),
        ('2', 'Employee'),
    ]

    email = models.EmailField(
        max_length=255, null=False, unique=True)
    password = models.CharField(max_length=60, default='none')
    name = models.CharField(max_length=255, default='none')
    phone_no = models.CharField(max_length=20, default='none')
    registration_date = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'User'


# class User(models.Model):
#     USER_TYPE_CHOICES = [
#         ('1', 'Customer'),
#         ('2', 'Employee'),
#     ]

#     user_id = models.AutoField(primary_key=True)
#     email = models.EmailField(max_length=255, default='none')
#     password = models.CharField(max_length=60, default='none')
#     name = models.CharField(max_length=255, default='none')
#     phone_no = models.CharField(max_length=20, default='none')
#     registration_date = models.DateTimeField(auto_now_add=True)
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

#     class Meta:
#         db_table = 'User'

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
