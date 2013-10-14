# coding=utf8
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate
from models import User_Profile as RBUserProfileModel 
from models import User_Follow as RBUserFollowModel
import datetime

class RBUser(object):
    
    class EmailExistAlready(Exception):
        def __init__(self, email):
            self.__message = "email %s is exist" %email
        def __str__(self):
            return repr(self.__message)

    class NicknameExistAlready(Exception):
        def __init__(self, nickname):
            self.__message = "nickname%s is exist" %nickname
        def __str__(self):
            return repr(self.__message)
    
    def __init__(self, user_id):
        self.__user_id = int(user_id) 
    
    def __ensure_user_obj(self):
        if not hasattr(self, '__user_obj'):
            self.__user_obj = AuthUser.objects.get(pk = self.__user_id)

    def get_user_id(self):
        return self.__user_id
    
    def get_username(self):
        self.__ensure_user_obj()
        return self.__user_obj.username
    
    @classmethod
    def _generate_seed(cls):
        _seed = AuthUser.objects.all().values_list('id', flat = True).latest('id')
        return _seed 

    @classmethod
    def _generate_username(cls):
        _seed = cls._generate_seed()
        _username = "mb_%s" % str(_seed) 
        return _username

    def check_auth(self, password):
        self.__ensure_user_obj()
        if authenticate(username = self.get_username(), password = password):
            return True
        return False
    
    @classmethod
    def login(cls, email, password):
        _user_obj = AuthUser.objects.get(email = email)
        _inst = cls(_user_obj.id)
        _inst.__user_obj = _user_obj
        
        if _inst.check_auth(password): 
            return _inst
        return None

    @staticmethod
    def email_exist(email):
        if AuthUser.objects.filter(email = email).count() > 0:
            return True
        return False

    @classmethod
    def create(cls, email, password, username = None):
        if RBUser.email_exist(email):
            raise RBUser.EmailExistAlready(email) 

        _username = cls._generate_username()
        _user = AuthUser.objects.create(username = _username, email = email)
        _user.set_password(password)
        _user.save()
         
        _inst = cls(_user.id)
        return _inst
    
    def delete(self):
        self.__ensure_user_obj()
        self.__user_obj.delete()
        

    @staticmethod
    def nickname_exist(nickname):
        if RBUserProfileModel.objects.filter(nickname = nickname).count() > 0:
            return True
        return False
    
    def set_profile(self, nickname, location = 'beijing', gender = 'O', bio = '', website = ''):
        if RBUser.nickname_exist(nickname):
            raise RBUser.NicknameExistAlready(nickname) 
        
        _user_profile = RBUserProfileModel.objects.create(
            user_id = self.__user_id,
            nickname = nickname,
            location = location,
            gender = gender,
            bio = bio,
            website = website
        )
        self.__profile = _user_profile
        
    def __load_user_context(self):
        self.__ensure_user_obj()
        _context = {}
        _context['user_id'] = self.__user_obj.id
        
        try:
            _profile = RBUserProfileModel.objects.get(user_id = self.__user_id)
            _context['nickname'] = _profile.nickname
            _context['avatar'] = 'http://imgcdn.guoku.com/avatar/large_79761_fe9187b12ab58170abadbb1530f6f5d2.jpg'
            _context['verified'] = 0 
            _context['verified_type'] = 'guoku' 
            _context['verified_reason'] = 'guoku' 
            _context['gender'] = _profile.gender 
            _context['friend_count'] = 0 
            _context['follower_count'] = 0 
            _context['money_i_need'] = 0 
            _context['like_count'] = 0 
            _context['note_count'] = 0 
            _context['same_follow'] = []
        except RBUserProfileModel.DoesNotExist, e:
            _context['nickname'] = 'unknown' 
            _context['avatar'] = 'http://imgcdn.guoku.com/avatar/large_79761_fe9187b12ab58170abadbb1530f6f5d2.jpg'
            _context['verified'] = 0 
            _context['verified_type'] = 'guoku' 
            _context['verified_reason'] = 'guoku' 
            _context['gender'] = 'O' 
            _context['friend_count'] = 0 
            _context['follower_count'] = 0 
            _context['money_i_need'] = 0 
            _context['like_count'] = 0 
            _context['note_count'] = 0 
            _context['same_follow'] = []
            
            
        return _context
    
    def read(self):
        _context = self.__load_user_context()
        return _context

    def follow(self, followee_id):
        try:
            RBUserFollowModel.objects.create(
                follower_id = self.__user_id,
                followee_id = followee_id 
            )
            return True
        except:
            pass
        return False
         
    def unfollow(self, followee_id):
        try:
            _obj = RBUserFollowModel.objects.get(
                follower_id = self.__user_id,
                followee_id = followee_id 
            )
            _obj.delete()
            return True
        except:
            pass
        return False
    
    @staticmethod
    def get_relation(sub_user_id, obj_user_id):
        _sub_user_id = int(sub_user_id)
        _obj_user_id = int(obj_user_id)
        if _sub_user_id == _obj_user_id: 
            return 4
        
        _is_following = RBUserFollowModel.objects.filter(
                follower_id = _sub_user_id, 
                followee_id = _obj_user_id, 
        ).count()
        
        _is_followed = RBUserFollowModel.objects.filter(
                follower_id = _obj_user_id,
                followee_id = _sub_user_id, 
        ).count()
        
        if _is_following > 0 and _is_followed > 0:
            return 3

        if _is_following > 0:
            return 1

        if _is_followed > 0:
            return 2

        return 0

    def get_following_user_id_list(self):
        return map(lambda x : x.followee_id, RBUserFollowModel.objects.filter(follower_id = self.__user_id))
             
    def get_fan_user_id_list(self):
        return map(lambda x : x.follower_id, RBUserFollowModel.objects.filter(followee_id = self.__user_id))

            
         

