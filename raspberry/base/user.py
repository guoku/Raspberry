# coding=utf8
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.cache import cache
from models import Avatar as AvatarModel 
from models import Entity_Like as EntityLikeModel
from models import Note as NoteModel
from models import Note_Poke as NotePokeModel
from models import Sina_Token as SinaTokenModel 
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


    class PasswordLessIllegal(Exception):
        def __init__(self):
            self.__message = "password illegal"
        def __str__(self):
            return repr(self.__message)

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
    
    def reset_account(self, username = None, password = None, email = None): 
        self.__ensure_user_obj()
        
        if email != None:
            if self.email_exist(email) and self.user_obj.email != email:
                raise self.EmailExistAlready(email) 
            self.user_obj.email = email
        
        if username != None:
            self.user_obj.username = username
        
        if password != None:
            if len(password) < 6:
                raise self.PasswordLessIllegal() 
        
            self.user_obj.set_password(password)

        self.user_obj.save()
        
        _basic_info = self.__load_basic_info_from_cache()
        if _basic_info != None:
            _basic_info = self.__reset_basic_info_to_cache()
           
    
    
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
        
        _basic_info = self.__load_basic_info_from_cache()
        if _basic_info != None:
            _basic_info = self.__reset_basic_info_to_cache()
           
    
    def __ensure_avatar_obj(self):
        if not hasattr(self, 'avatar_obj'):
            self.avatar_obj = self.Avatar(self.user_id)

    def __load_basic_info_from_cache(self):
        _cache_key = 'user_%s_basic_info'%self.user_id
        _basic_info = cache.get(_cache_key)
        #if self.user_id == 79761:
        #    print _basic_info
        return _basic_info
        
    def __reset_basic_info_to_cache(self):
        _cache_key = 'user_%s_basic_info'%self.user_id
        self.__ensure_user_obj()
        _basic_info = {}
        _basic_info['user_id'] = self.user_obj.id
        _basic_info['email'] = self.user_obj.email
        
        _profile = UserProfileModel.objects.get(user_id = self.user_id)
        _basic_info['nickname'] = _profile.nickname
        _basic_info['verified'] = 0 
        _basic_info['verified_type'] = 'guoku' 
        _basic_info['verified_reason'] = 'guoku' 
        _basic_info['gender'] = _profile.gender 
        
        self.__ensure_avatar_obj()
        _basic_info['avatar_large'] = self.avatar_obj.get_large_link() 
        _basic_info['avatar_small'] = self.avatar_obj.get_small_link() 
        
        cache.set(_cache_key, _basic_info, 864000)
            
        return _basic_info
    
    def __read_basic_info(self):
        _basic_info = self.__load_basic_info_from_cache()
        if _basic_info == None:
            _basic_info = self.__reset_basic_info_to_cache()
        return _basic_info 
    
    def __load_user_stat_info_from_cache(self):
        _cache_key = 'user_%s_stat_info'%self.user_id
        _stat_info = cache.get(_cache_key)
        return _stat_info
    
    def __reset_user_stat_info_to_cache(self, stat_info = None):
        _cache_key = 'user_%s_stat_info'%self.user_id
        if stat_info == None:
            _stat_info = {}
            _stat_info['following_count'] = UserFollowModel.objects.filter(follower_id = self.user_id).count()
            _stat_info['fan_count'] = UserFollowModel.objects.filter(followee_id = self.user_id).count()
            _stat_info['like_count'] = EntityLikeModel.objects.filter(user_id = self.user_id).count()
            _stat_info['entity_note_count'] = NoteModel.objects.filter(creator_id = self.user_id).count()
            _stat_info['entity_note_poke_count'] = NotePokeModel.objects.filter(note__creator_id = self.user_id).count()
        
        else:
            _stat_info = stat_info
        cache.set(_cache_key, _stat_info, 864000)
        return _stat_info
    
    
    def entity_like_count(self, category_id):
        return EntityLikeModel.objects.filter(user_id = self.user_id, entity__neo_category_id = category_id).count()
        
    def find_like_entity(self, category_id, offset = None, count = 30, sort_by = None, reverse = False):
        _hdl = EntityLikeModel.objects.filter(user_id = self.user_id, entity__neo_category_id = category_id)
        if sort_by == 'price':
            if reverse:
                _hdl = _hdl.order_by('-entity__price')
            else:
                _hdl = _hdl.order_by('entity__price')
        elif sort_by == 'like':
            if reverse:
                _hdl = _hdl.order_by('entity__like_count')
            else:
                _hdl = _hdl.order_by('-entity__like_count')
        else:
            _hdl = _hdl.order_by('-created_time')
       
        if offset != None and count != None:
            _hdl = _hdl[offset : offset + count]

        _entity_id_list = map(lambda x: x.entity_id, _hdl)
        return _entity_id_list
    
    
    def __update_user_following_count(self, delta):
        _stat_info = self.__load_user_stat_info_from_cache()
        if _stat_info != None:
            _stat_info['following_count'] += delta
            if _stat_info['following_count'] < 0:
                _stat_info['following_count'] = 0
            self.__reset_user_stat_info_to_cache(_stat_info)
    
    def __update_user_fan_count(self, delta):
        _stat_info = self.__load_user_stat_info_from_cache()
        if _stat_info != None:
            _stat_info['fan_count'] += delta
            if _stat_info['fan_count'] < 0:
                _stat_info['fan_count'] = 0
            self.__reset_user_stat_info_to_cache(_stat_info)
    
    def update_user_like_count(self, delta):
        _stat_info = self.__load_user_stat_info_from_cache()
        if _stat_info != None:
            _stat_info['like_count'] += delta
            if _stat_info['like_count'] < 0:
                _stat_info['like_count'] = 0
            self.__reset_user_stat_info_to_cache(_stat_info)
    
    def update_user_entity_note_count(self, delta):
        _stat_info = self.__load_user_stat_info_from_cache()
        if _stat_info != None:
            _stat_info['entity_note_count'] += delta
            if _stat_info['entity_note_count'] < 0:
                _stat_info['entity_note_count'] = 0
            self.__reset_user_stat_info_to_cache(_stat_info)
            
    def update_user_entity_note_poke_count(self, delta):
        _stat_info = self.__load_user_stat_info_from_cache()
        if _stat_info != None:
            _stat_info['entity_note_poke_count'] += delta
            if _stat_info['entity_note_poke_count'] < 0:
                _stat_info['entity_note_poke_count'] = 0
            self.__reset_user_stat_info_to_cache(_stat_info)
            

        
    
    def __read_user_stat_info(self):
        _stat_info = self.__load_user_stat_info_from_cache()
        if _stat_info == None:
            _stat_info = self.__reset_user_stat_info_to_cache()
        return _stat_info
    
    def read(self):
        _context = self.__read_basic_info()
        _context.update(self.__read_user_stat_info())
        return _context

    def follow(self, followee_id):
        try:
            _followee_id = int(followee_id)
            UserFollowModel.objects.create(
                follower_id = self.user_id,
                followee_id = _followee_id 
            )
            self.__update_user_following_count(delta = 1)

            _list = self.__load_following_user_id_list_from_cache()
            if _list != None:
                if not _followee_id in _list:
                    _list.append(_followee_id)
                    self.__reset_following_user_id_list_to_cache(user_id_list = _list)

            User(_followee_id).add_fan(self.user_id)
            
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
            _followee_id = int(followee_id)
            _obj = UserFollowModel.objects.get(
                follower_id = self.user_id,
                followee_id = followee_id 
            )
            _obj.delete()
            self.__update_user_following_count(delta = -1)
            
            _list = self.__load_following_user_id_list_from_cache()
            if _list != None:
                if _followee_id in _list:
                    _list.remove(_followee_id)
                    self.__reset_following_user_id_list_to_cache(user_id_list = _list)
            
            User(_followee_id).remove_fan(self.user_id)
            
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

    def __load_following_user_id_list_from_cache(self):
        _cache_key = 'user_%s_following_list'%self.user_id
        _list = cache.get(_cache_key)
        return _list
    
    def __reset_following_user_id_list_to_cache(self, user_id_list = None):
        _cache_key = 'user_%s_following_list'%self.user_id
        if user_id_list == None:
            _list = map(lambda x : x.followee_id, UserFollowModel.objects.filter(follower_id = self.user_id))
        else:
            _list = user_id_list
        cache.set(_cache_key, _list, 864000)

    
    def read_following_user_id_list(self):
        _list = self.__load_following_user_id_list_from_cache() 
        if _list == None:
            _list = self.__reset_following_user_id_list_to_cache()
        return _list
             
    def __load_fan_user_id_list_from_cache(self):
        _cache_key = 'user_%s_fan_list'%self.user_id
        _list = cache.get(_cache_key)
        return _list
    
    def __reset_fan_user_id_list_to_cache(self, user_id_list = None):
        _cache_key = 'user_%s_fan_list'%self.user_id
        if user_id_list == None:
            _list = map(lambda x : x.follower_id, UserFollowModel.objects.filter(followee_id = self.user_id))
        else:
            _list = user_id_list
        cache.set(_cache_key, _list, 864000)
    
    def read_fan_user_id_list(self):
        _list = self.__load_fan_user_id_list_from_cache() 
        if _list == None:
            _list = self.__reset_fan_user_id_list_to_cache() 
        return _list

    def add_fan(self, user_id):
        _user_id = int(user_id)
        _list = self.__load_fan_user_id_list_from_cache()
        if _list != None:
            if not _user_id in _list:
                _list.append(_user_id)
                self.__reset_fan_user_id_list_to_cache(user_id_list = _list)
                self.__update_user_fan_count(delta = 1)
         
    def remove_fan(self, user_id):
        _user_id = int(user_id)
        _list = self.__load_fan_user_id_list_from_cache()
        if _list != None:
            if _user_id in _list:
                _list.remove(_user_id)
                self.__reset_fan_user_id_list_to_cache(user_id_list = _list)
                self.__update_user_fan_count(delta = -1)
    
    def upload_avatar(self, data):
        self.avatar_obj = self.Avatar.create(self.user_id, data)
       
        
    @staticmethod
    def check_sina_id(sina_id_list):
        _rslt = [] 
        for _sina_token_obj in SinaTokenModel.objects.filter(sina_id__in = sina_id_list):
            if _sina_token_obj.user_id != None:
                _rslt.append({
                    'sina_id' : _sina_token_obj.sina_id,
                    'user_id' : _sina_token_obj.user_id
                })
        return _rslt

    @classmethod
    def search(cls, query_string, offset = 0, count = 30):
        _query_set = UserProfileModel.search.query(query_string).order_by('-fans_count')
        _user_id_list = []
        for _result in _query_set[offset : offset + count]:
            _user_id_list.append(int(_result._sphinx['attrs']['user_id']))
        return _user_id_list
    

