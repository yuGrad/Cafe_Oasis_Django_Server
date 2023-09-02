from django.db import models
from users.models import User
from cafe.models import Cafe

# Create your models here.


class VisitHistory(models.Model):
    visit_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING)
    cafe = models.ForeignKey(
        Cafe, on_delete=models.DO_NOTHING)
    total_spend = models.DecimalField(max_digits=10, decimal_places=0)
    visit_date = models.DateTimeField()

    class Meta:
        db_table = 'VisitHistory'


class CafeRating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rating_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING)
    cafe = models.ForeignKey(
        Cafe, on_delete=models.DO_NOTHING)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    rating_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CafeRating'
