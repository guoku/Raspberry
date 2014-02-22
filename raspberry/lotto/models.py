# coding=utf8
from django.db import models
from django.contrib.auth.models import User


class Accumulate(models.Model):
    key = models.IntegerField(db_index=True, null=False)
    count = models.IntegerField(null=False)

class Player(models.Model):
    user_id = models.IntegerField(db_index=True, null=True, default=None)
    sina_id = models.CharField(max_length=64, null=True, db_index=True)
    token = models.CharField(max_length=32, unique=True, db_index=True)
    screen_name = models.CharField(max_length=64, null=True, db_index=True)
    access_token = models.CharField(max_length=255, null=True, db_index=True)
    expires_in = models.PositiveIntegerField(default=0)
    share_count = models.IntegerField(db_index=True, null=True, default=0)
    roll_count = models.IntegerField(db_index=True, null=True, default=0)
    last_share_time = models.DateTimeField(null=True, default=None)
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)


class Reward(models.Model):
    player = models.ForeignKey(Player)
    level = models.IntegerField(db_index=True, null=False)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
