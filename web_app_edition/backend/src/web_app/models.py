from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class NMM_ELO_RatingManager(models.Manager):
    def create_elo(self, user):
        elo = self.create(user=user)
        return elo

class NMM_ELO_Rating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=2000)

    objects = NMM_ELO_RatingManager()
