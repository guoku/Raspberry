# coding=utf8
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate
from django.conf import settings
from models import Avatar as AvatarModel 
from models import User_Profile as UserProfileModel 
from models import User_Follow as UserFollowModel
from message import UserFollowMessage 
from hashlib import md5
from pymogile import Client
from wand.image import Image
import datetime

class User(object):
    

    class Avatar(object):
        
        def __init__(self, user_id):
            self.user_id = user_id
            try:
                self.avatar_obj = AvatarModel.objects.get(user_id = self.user_id)
            except AvatarModel.DoesNotExist, e:
                self.avatar_obj = None
       
        
        @staticmethod
        def crop_square(data):
            _img = Image(blob = data)
            _delta = _img.width - _img.height
            if _delta > 0:
                _img.crop(_delta / 2 , 0, width = _img.height, height = _img.height)
            elif _delta < 0:
                _img.crop(0, 0, width = _img.width, height = _img.width)
            return _img.make_blob()
        
        @staticmethod
        def resize(data, w, h):
            _img = Image(blob = data)
            _img.resize(w, h)
            return _img.make_blob()
    
        def get_large_link(self):
            if self.avatar_obj != None: 
                return settings.IMAGE_SERVER + self.avatar_obj.avatar_large
            return 'http://imgcdn.guoku.com/avatar/large_79761_fe9187b12ab58170abadbb1530f6f5d2.jpg'
        
        def get_small_link(self):
            if self.avatar_obj != None:
                return settings.IMAGE_SERVER + self.avatar_obj.avatar_small
            return 'http://imgcdn.guoku.com/avatar/large_79761_fe9187b12ab58170abadbb1530f6f5d2.jpg'
        
        @classmethod
        def create(cls, user_id, origin_data):
            _key = md5(origin_data).hexdigest()
            
            _datastore = Client(
                domain = settings.MOGILEFS_DOMAIN, 
                trackers = settings.MOGILEFS_TRACKERS 
            )
            
            _origin_link = 'avatar/origin/' + _key
            _fp = _datastore.new_file(_origin_link)
            _fp.write(origin_data)
            _fp.close()
    
            _square_data = cls.crop_square(origin_data)
            _large_link = 'avatar/large/' + _key
            _large_data = cls.resize(_square_data, 180, 180)
            _fp = _datastore.new_file(_large_link)
            _fp.write(_large_data)
            _fp.close()
            
             
            _small_link = 'avatar/small/' + _key
            _small_data = cls.resize(_square_data, 50, 50)
            _fp = _datastore.new_file(_small_link)
            _fp.write(_small_data)
            _fp.close()
           
            _inst = cls(user_id)
            if _inst.avatar_obj == None:
                _avatar_obj = AvatarModel.objects.create(
                    user_id = user_id,
                    avatar_origin = _origin_link,
                    avatar_small = _small_link,
                    avatar_large = _large_link
                )
                _inst.avatar_obj = _avatar_obj
            else:
                _inst.avatar_obj.avatar_origin = _origin_link
                _inst.avatar_obj.avatar_large = _large_link
                _inst.avatar_obj.avatar_small = _small_link
                _inst.avatar_obj.save()

            return _inst

        
        @staticmethod
        def read_image_data_by_store_key(store_key): 
            _datastore = Client(
                domain = settings.MOGILEFS_DOMAIN, 
                trackers = settings.MOGILEFS_TRACKERS 
            )
            return _datastore.get_file_data(store_key)



    class LoginEmailDoesNotExist(Exception):
        def __init__(self, email):
            self.__message = "login email %s is not exist" %email
        def __str__(self):
            return repr(self.__message)
    
    class LoginPasswordIncorrect(Exception):
        def __init__(self):
            self.__message = "login password is incorrect"
        def __str__(self):
            return repr(self.__message)
    
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
        self.user_id = int(user_id) 
    
    def __ensure_user_obj(self):
        if not hasattr(self, 'user_obj'):
            self.user_obj = AuthUser.objects.get(pk = self.user_id)
    
    def __ensure_user_profile_obj(self):
        if not hasattr(self, 'user_profile_obj'):
            try:
                self.user_profile_obj = UserProfileModel.objects.get(user_id = self.user_id)
            except UserProfileModel.DoesNotExist, e:
                self.user_profile_obj = None

    def get_username(self):
        self.__ensure_user_obj()
        return self.user_obj.username
    
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
        try:
            _user_obj = AuthUser.objects.get(email = email)
        except AuthUser.DoesNotExist, e:
            raise User.LoginEmailDoesNotExist(email)

        _inst = cls(_user_obj.id)
        _inst.user_obj = _user_obj
        
        if not _inst.check_auth(password):
            raise User.LoginPasswordIncorrect()
        return _inst

    @staticmethod
    def email_exist(email):
        if AuthUser.objects.filter(email = email).count() > 0:
            return True
        return False

    @classmethod
    def create(cls, email, password, username = None):
        if User.email_exist(email):
            raise User.EmailExistAlready(email) 

        _username = cls._generate_username()
        _user = AuthUser.objects.create(username = _username, email = email)
        _user.set_password(password)
        _user.save()
         
        _inst = cls(_user.id)
        return _inst
    
    
    def delete(self):
        self.__ensure_user_obj()
        self.user_obj.delete()
        

    @staticmethod
    def nickname_exist(nickname):
        if UserProfileModel.objects.filter(nickname = nickname).count() > 0:
            return True
        return False
    
    def set_profile(self, nickname, location = 'beijing', gender = 'O', bio = '', website = ''):
        self.__ensure_user_profile_obj()
        
        if self.user_profile_obj == None:
            _user_profile_obj = UserProfileModel.objects.create(
                user_id = self.user_id,
                nickname = nickname,
                location = location,
                gender = gender,
                bio = bio,
                website = website
            )
            self.user_profile_obj = _user_profile_obj
        else:
            if nickname != None:
                _nickname = nickname.strip()
                if User.nickname_exist(_nickname):
                    raise User.NicknameExistAlready(_nickname)
                else:
                    self.user_profile_obj.nickname = _nickname
            
            if location != None:
                _location = location.strip()
                self.user_profile_obj.location = _location 

            self.user_profile_obj.save()
           
    
    def __ensure_avatar_obj(self):
        if not hasattr(self, 'avatar_obj'):
            self.avatar_obj = self.Avatar(self.user_id)

        
    def __load_user_context(self):
        self.__ensure_user_obj()
        _context = {}
        _context['user_id'] = self.user_obj.id
        
        _profile = UserProfileModel.objects.get(user_id = self.user_id)
        _context['nickname'] = _profile.nickname
        _context['verified'] = 0 
        _context['verified_type'] = 'guoku' 
        _context['verified_reason'] = 'guoku' 
        _context['gender'] = _profile.gender 
        
        self.__ensure_avatar_obj()
        _context['avatar_large'] = self.avatar_obj.get_large_link() 
        _context['avatar_small'] = self.avatar_obj.get_small_link() 
            
        return _context
    
    def read(self):
        _context = self.__load_user_context()
        return _context

    def follow(self, followee_id):
        try:
            UserFollowModel.objects.create(
                follower_id = self.user_id,
                followee_id = followee_id 
            )
            
            _message = UserFollowMessage(
                user_id = followee_id,
                follower_id = self.user_id,
                created_time = datetime.datetime.now()
            )
            _message.save()
            
            return True
        except:
            pass
        return False
         
    def unfollow(self, followee_id):
        try:
            _obj = UserFollowModel.objects.get(
                follower_id = self.user_id,
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
        
        _is_following = UserFollowModel.objects.filter(
                follower_id = _sub_user_id, 
                followee_id = _obj_user_id, 
        ).count()
        
        _is_followed = UserFollowModel.objects.filter(
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

    def get_following_user_id_list(self, offset = 0, count = 30):
        return map(lambda x : x.followee_id, UserFollowModel.objects.filter(follower_id = self.user_id)[offset : offset + count])
             
    def get_fan_user_id_list(self, offset = 0, count = 30):
        return map(lambda x : x.follower_id, UserFollowModel.objects.filter(followee_id = self.user_id)[offset : offset + count])

    def upload_avatar(self, data):
        self.avatar_obj = self.Avatar.create(self.user_id, data)
       
        
