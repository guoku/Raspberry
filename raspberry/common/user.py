# coding=utf8
from django.contrib.auth.models import User
from models import User_Profile
import datetime

class RBUser(object):
    
    def __init__(self, user_id):
        self.__user_id = user_id 
    
    def get_user_id(self):
        return self.__user_id
    
    @classmethod
    def create(cls, username, email, password):
        _user = User.objects.create(username = username, email = email)
        _user.set_password(password)
        _user.save()
         
        _inst = cls(_user.id)
        return _inst

    
    def set_profile(self, nickname, location, gender, bio, website):
        _user_profile = User_Profile.objects.create(
            nickname = nickname,
            location = location,
            gender = gender,
            bio = bio,
            website = website
        )
        self.__profile = _user_profile

