# coding=utf8
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count 
from django.template.loader import render_to_string
from models import Avatar as AvatarModel 
from models import Entity_Like as EntityLikeModel
from models import Entity_Tag as EntityTagModel
from models import Note as NoteModel
from models import Note_Poke as NotePokeModel
from models import User_Censor as UserCensorModel 
from models import Seed_User as SeedUserModel 
from models import Sina_Token as SinaTokenModel 
from models import Seller_Info as SellerInfoModel 
from models import Taobao_Token as TaobaoTokenModel 
from models import One_Time_Token as OneTimeTokenModel 
from models import User_Profile as UserProfileModel 
from models import User_Follow as UserFollowModel
from models import User_Footprint as UserFootprintModel
from utils.apns_notification import APNSWrapper
from tasks import CreateUserFollowMessageTask
from message import NeoMessage 
from models import Selection 
from utils.mail import Mail
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
            return 'http://imgcdn.guoku.com/avatar/large_241170_637c2ee4729634de9fc848f9754c263b.png'
        
        def get_small_link(self):
            if self.avatar_obj != None:
                return settings.IMAGE_SERVER + self.avatar_obj.avatar_small
            return 'http://imgcdn.guoku.com/avatar/small_241170_ce838e0ed9c613bb06ce79842913c83f.png'
        
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
    
    class LoginSinaIdDoesNotExist(Exception):
        def __init__(self, sina_id):
            self.__message = "login sina_id %s is not exist" %sina_id
        def __str__(self):
            return repr(self.__message)
    
    class LoginTaobaoIdDoesNotExist(Exception):
        def __init__(self, taobao_id):
            self.__message = "login taobao_id %s is not exist" %taobao_id
        def __str__(self):
            return repr(self.__message)
    
    class EmailExistAlready(Exception):
        def __init__(self, email):
            self.__message = "email %s is exist" %email
        def __str__(self):
            return repr(self.__message)
    
    class EmailDoesNotExist(Exception):
        def __init__(self, email):
            self.__message = "email %s does not exist" %email
        def __str__(self):
            return repr(self.__message)
    
    class SinaIdExistAlready(Exception):
        def __init__(self, sina_id):
            self.__message = "sina_id %s is exist" %sina_id
        def __str__(self):
            return repr(self.__message)

    class TaobaoIdExistAlready(Exception):
        def __init__(self, taobao_id):
            self.__message = "taobao_id %s is exist" %taobao_id
        def __str__(self):
            return repr(self.__message)

    class NicknameExistAlready(Exception):
        def __init__(self, nickname):
            self.__message = "nickname%s is exist" %nickname
        def __str__(self):
            return repr(self.__message)
    
    class UserBindTaobaoAlready(Exception):
        def __init__(self):
            self.__message = "bind taobao already" 
        def __str__(self):
            return repr(self.__message)
    
    class UserBindShopAlready(Exception):
        def __init__(self):
            self.__message = "bind shop already" 
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
    
    def get_email(self):
        self.__ensure_user_obj()
        return self.user_obj.email
    
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

    @classmethod
    def login_by_sina(cls, sina_id, sina_token = None, screen_name = None, expires_in = None):
        try:
            _sina_token_obj = SinaTokenModel.objects.get(sina_id = sina_id)
        except SinaTokenModel.DoesNotExist, e:
            raise User.LoginSinaIdDoesNotExist(sina_id)
    
        if sina_token:
            _sina_token_obj.access_token = sina_token
        if screen_name:
            _sina_token_obj.screen_name = screen_name
        if expires_in:
            _sina_token_obj.expires_in = expires_in
        _sina_token_obj.save()
        _inst = cls(_sina_token_obj.user_id)
        return _inst
    
    @classmethod
    def login_by_taobao(cls, taobao_id, taobao_token = None, screen_name = None, expires_in = None):
        try:
            _taobao_token_obj = TaobaoTokenModel.objects.get(taobao_id = taobao_id)
        except TaobaoTokenModel.DoesNotExist, e:
            raise User.LoginTaobaoIdDoesNotExist(taobao_id)
    
        if taobao_token:
            _taobao_token_obj.access_token = taobao_token
        if screen_name:
            _taobao_token_obj.screen_name = screen_name
        if expires_in:
            _taobao_token_obj.expires_in = expires_in
        _taobao_token_obj.save()
        _inst = cls(_taobao_token_obj.user_id)
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
    
    @classmethod
    def create_by_sina(cls, sina_id, screen_name, sina_token, email, password, username = None):
        if SinaTokenModel.objects.filter(sina_id = sina_id).count() > 0:
            raise User.SinaIdExistAlready(sina_id)

        _user_inst = cls.create(
            email = email,
            password = password,
            username = username
        )

        SinaTokenModel.objects.create(
            user_id = _user_inst.user_id,
            sina_id = sina_id,
            screen_name = screen_name,
            access_token = sina_token
        )

        return _user_inst
    
    @classmethod
    def create_by_taobao(cls, taobao_id, screen_name, taobao_token, email, password, expires_in = 0, username = None):
        if TaobaoTokenModel.objects.filter(taobao_id = taobao_id).count() > 0:
            raise User.TaobaoIdExistAlready(taobao_id)

        _user_inst = cls.create(
            email = email,
            password = password,
            username = username
        )

        TaobaoTokenModel.objects.create(
            user_id = _user_inst.user_id,
            taobao_id = taobao_id,
            screen_name = screen_name,
            access_token = taobao_token,
            expires_in = expires_in
        )

        return _user_inst
    
   
    def authenticate_without_password(self):
        try:
            _user = AuthUser.objects.get(pk = self.user_id)
            _user.backend = 'django.contrib.auth.backends.ModelBackend'
            return _user
        except:
            return None

    def bind_sina(self, sina_id, screen_name, access_token, expires_in = 0):
        try:
            _token = SinaTokenModel.objects.get(user_id = self.user_id, sina_id = sina_id)
            _token.screen_name = screen_name
            _token.access_token = access_token
            _token.expires_in = expires_in
            _token.save()
        except SinaTokenModel.DoesNotExist:
            if SinaTokenModel.objects.filter(sina_id = sina_id).count() > 0:
                raise User.SinaIdExistAlready(sina_id)
            
            if SinaTokenModel.objects.filter(user_id = self.user_id).count() > 0:
                raise User.UserBindSinaAlready()
            
            SinaTokenModel.objects.create(
                user_id = self.user_id,
                sina_id = sina_id,
                screen_name = screen_name,
                access_token = access_token,
                expires_in = expires_in
            )
        self.__reset_basic_info_to_cache()
    
    def unbind_sina(self):
        try:
            _sina_token_obj = SinaTokenModel.objects.get(user_id = self.user_id)
            _sina_token_obj.delete()
            self.__reset_basic_info_to_cache()
        except SinaTokenModel.DoesNotExist:
            pass
 
    def bind_taobao(self, taobao_id, screen_name, taobao_token, expires_in = 0):
        try:
            _token = TaobaoTokenModel.objects.get(user_id = self.user_id, taobao_id = taobao_id)
            _token.screen_name = screen_name
            _token.access_token = taobao_token
            _token.expires_in = expires_in
            _token.save()
        except TaobaoTokenModel.DoesNotExist:
            if TaobaoTokenModel.objects.filter(taobao_id = taobao_id).count() > 0:
                raise User.TaobaoIdExistAlready(taobao_id)
            
            if TaobaoTokenModel.objects.filter(user_id = self.user_id).count() > 0:
                raise User.UserBindTaobaoAlready()
            
            TaobaoTokenModel.objects.create(
                user_id = self.user_id,
                taobao_id = taobao_id,
                screen_name = screen_name,
                access_token = taobao_token,
                expires_in = expires_in
            )
        self.__reset_basic_info_to_cache()
    
    def unbind_taobao(self):
        try:
            _taobao_token_obj = TaobaoTokenModel.objects.get(user_id = self.user_id)
            _taobao_token_obj.delete()
            self.__reset_basic_info_to_cache()
        except TaobaoTokenModel.DoesNotExist, e:
            print e
        
    def create_seller_info(self, taobao_shop_nick):
        if SellerInfoModel.objects.filter(user_id = self.user_id).count() > 0:
            raise User.UserBindShopAlready() 
        SellerInfoModel.objects.create(user_id = self.user_id, shop_nick = taobao_shop_nick)
        self.__reset_basic_info_to_cache()
    
    def delete(self):
        self.__ensure_user_obj()
        self.user_obj.delete()
    
    @classmethod
    def count(cls): 
        _hdl = AuthUser.objects.all()
        return _hdl.count() 
    
    
    @classmethod
    def find(cls, offset = None, count = None):
        _hdl = AuthUser.objects.all()
        
        if offset != None and count != None:
            _hdl = _hdl[offset : offset + count]
        
        _list = map(lambda x: x.id, _hdl)
        return _list
        

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
           
    
    
    def set_profile(self, nickname, location = u'北京', city = u'朝阳', gender = 'O', bio = '', website = ''):
        self.__ensure_user_profile_obj()

        if nickname != None:
            _nickname = nickname.strip()
            if self.user_profile_obj != None and _nickname != self.user_profile_obj.nickname:
                if User.nickname_exist(_nickname):
                    raise User.NicknameExistAlready(_nickname)
        
        if self.user_profile_obj == None:
            _user_profile_obj = UserProfileModel.objects.create(
                user_id = self.user_id,
                nickname = nickname.strip(),
                location = location,
                city = city,
                gender = gender,
                bio = bio,
                website = website
            )
            self.user_profile_obj = _user_profile_obj
        else:
            if nickname != None:
                self.user_profile_obj.nickname = nickname.strip()
            if location != None:
                self.user_profile_obj.location = location.strip()
            if city != None:
                self.user_profile_obj.city = city.strip()
            if bio != None:
                self.user_profile_obj.bio = bio.strip()
            if website != None:
                self.user_profile_obj.website = website.strip()
            if gender != None:
                self.user_profile_obj.gender = gender.strip()
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
        return _basic_info
        
    def __reset_basic_info_to_cache(self):
        _cache_key = 'user_%s_basic_info'%self.user_id
        self.__ensure_user_obj()
        _basic_info = {}
        _basic_info['user_id'] = self.user_obj.id
        _basic_info['email'] = self.user_obj.email
        _basic_info['username'] = self.user_obj.username 
        
        if UserCensorModel.objects.filter(user = self.user_id).count() > 0:
            _basic_info['is_censor'] = True 
            _basic_info['nickname'] = u'我是一只小白兔'
            _basic_info['bio'] = u'内心温柔，人畜无害' 
            _basic_info['website'] = ''
            _basic_info['gender'] = 'O' 
            _basic_info['avatar_large'] = 'http://imgcdn.guoku.com/avatar/large_191181_a9b257239f709958650cd28f400dd7fe.jpg' 
            _basic_info['avatar_small'] = 'http://imgcdn.guoku.com/avatar/small_191181_e8fe39377fc03cae8d9e3deec45c5443.jpg' 
              
        else:
            _profile = UserProfileModel.objects.get(user_id = self.user_id)
            _basic_info['nickname'] = _profile.nickname
            _basic_info['verified'] = 0 
            _basic_info['verified_type'] = 'guoku' 
            _basic_info['verified_reason'] = 'guoku' 
            _basic_info['gender'] = _profile.gender 
            _basic_info['location'] = _profile.location
            _basic_info['city'] = _profile.city
            _basic_info['bio'] = _profile.bio
            _basic_info['is_censor'] = False
            
            self.__ensure_avatar_obj()
            _basic_info['avatar_large'] = self.avatar_obj.get_large_link() 
            _basic_info['avatar_small'] = self.avatar_obj.get_small_link()

        try:
            _sina_token_obj = SinaTokenModel.objects.get(user_id = self.user_id)
            _basic_info['sina_screen_name'] = _sina_token_obj.screen_name
        except SinaTokenModel.DoesNotExist:
            pass
        
        try:
            _taobao_token_obj = TaobaoTokenModel.objects.get(user_id = self.user_id)
            _basic_info['taobao_nick'] = _taobao_token_obj.screen_name
            _basic_info['taobao_token_expires_in'] = _taobao_token_obj.expires_in
        except TaobaoTokenModel.DoesNotExist:
            pass

        try:
            _seller_info_obj = SellerInfoModel.objects.get(user_id = self.user_id)
            _basic_info['shop_nick'] = _seller_info_obj.shop_nick
            _basic_info['shop_type'] = _seller_info_obj.shop_type
            _basic_info['shop_company_name'] = _seller_info_obj.company_name
            _basic_info['shop_qq_account'] = _seller_info_obj.qq_account
            _basic_info['shop_email'] = _seller_info_obj.email
            _basic_info['shop_mobile'] = _seller_info_obj.shop_type
            _basic_info['shop_main_products'] = _seller_info_obj.main_products
            _basic_info['shop_intro'] = _seller_info_obj.intro
            _basic_info['shop_verified'] = _seller_info_obj.verified
        except SellerInfoModel.DoesNotExist:
            pass
        cache.set(_cache_key, _basic_info, 864000)
        cache.delete("user_context_%s"%self.user_id)
            
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
            _stat_info['following_count'] = UserFollowModel.objects.filter(follower_id=self.user_id).count()
            _stat_info['fan_count'] = UserFollowModel.objects.filter(followee_id=self.user_id).count()
            _stat_info['like_count'] = EntityLikeModel.objects.filter(user_id=self.user_id).count()
            _stat_info['latest_like_entity_id_list'] = map(lambda x: x.entity_id, EntityLikeModel.objects.filter(user_id=self.user_id).order_by('-created_time')[0:20])
            _stat_info['tag_count'] = EntityTagModel.objects.filter(user_id=self.user_id).values('tag').annotate(entity_count=Count('entity')).count()
            _stat_info['entity_note_count'] = NoteModel.objects.filter(creator_id=self.user_id).count()
            _stat_info['entity_note_poke_count'] = NotePokeModel.objects.filter(note__creator_id=self.user_id).count()
        
        else:
            _stat_info = stat_info
        cache.set(_cache_key, _stat_info, 864000)
        return _stat_info
    
    
    def entity_like_count(self, category_id=None, neo_category_id=None):
        _hdl = EntityLikeModel.objects.filter(user_id = self.user_id)
        if category_id != None:
            _hdl = _hdl.filter(entity__category__pid = category_id)
        
        if neo_category_id != None:
            _hdl = _hdl.filter(entity__neo_category_id = neo_category_id)
        
        return _hdl.count() 
        
    def find_like_entity(self, category_id = None, neo_category_id = None, timestamp = None, offset = None, count = 30, sort_by = None, reverse = False, with_timestamp = False):
        
        _hdl = EntityLikeModel.objects.filter(user_id = self.user_id)
        
        if timestamp != None:
            _hdl = _hdl.filter(created_time__lt = timestamp)
        
        if category_id != None:
            _hdl = _hdl.filter(entity__category__pid = category_id)
        
        if neo_category_id != None:
            _hdl = _hdl.filter(entity__neo_category_id = neo_category_id)
        
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
        
        if not with_timestamp:
            return map(lambda x: x.entity_id, _hdl)
        else:
            return map(lambda x: [x.entity_id, x.created_time], _hdl)
            
    
    
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
    
    def update_user_like_stat_info(self):
        _stat_info = self.__load_user_stat_info_from_cache()
        if _stat_info != None:
            _stat_info['like_count'] = EntityLikeModel.objects.filter(user_id=self.user_id).count()
            _stat_info['latest_like_entity_id_list'] = map(lambda x: x.entity_id, EntityLikeModel.objects.filter(user_id=self.user_id).order_by('-created_time')[0:20])
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
    
    def get_nickname(self):
        _context = self.__read_basic_info()
        return _context['nickname']

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

            _followee = User(_followee_id)
            _followee.add_fan(self.user_id)
        
        
            ## CLEAN_OLD_CACHE ## 
            cache.delete("user_fan_id_list_%s"%followee_id)
            cache.delete("user_following_id_list_%s"%self.user_id)
            
            CreateUserFollowMessageTask.delay(
                user_id = _followee_id,
                user_unread_message_count = User(_followee_id).get_unread_message_count(), 
                follower_id = self.user_id,
                follower_nickname = self.get_nickname(),
            )
            
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
             
            ## CLEAN_OLD_CACHE ## 
            cache.delete("user_fan_id_list_%s"%followee_id)
            cache.delete("user_following_id_list_%s"%self.user_id)
            
            return True
        except:
            pass
        return False
    
    def is_following(self, followee_user_id):
        _followee_user_id = int(followee_user_id)
        _list = self.read_following_user_id_list()
        if _followee_user_id in _list:
            return True
        return False
    
    
    @staticmethod
    def get_relation(sub_user_id, obj_user_id):
        _sub_user_id = int(sub_user_id)
        _obj_user_id = int(obj_user_id)
        if _sub_user_id == _obj_user_id:
            return 4
        
        _is_following = User(_sub_user_id).is_following(_obj_user_id) 
        _is_fan = User(_obj_user_id).is_following(_sub_user_id) 
        
        if _is_following and _is_fan:
            return 3

        if _is_following > 0:
            return 1

        if _is_fan > 0:
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
        return _list
    
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
        return _list
    
    
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
        
        _basic_info = self.__load_basic_info_from_cache()
        if _basic_info != None:
            _basic_info = self.__reset_basic_info_to_cache()
        
        cache.delete("avatar_%s"%self.user_id)

       
        
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
    
    @classmethod
    def read_seed_users(cls): 
        _cache_key = 'seed_user_id_list'
        _seed_user_id_list = cache.get(_cache_key)
        if _seed_user_id_list == None:
            _seed_user_id_list = map(lambda x: x.user_id, SeedUserModel.objects.all())
            cache.set(_cache_key, _seed_user_id_list, 86400)
        return _seed_user_id_list


    def __create_one_time_token(self, token_type):
        _token = md5(self.user_obj.email + unicode(str(self.user_obj.id)) + unicode(self.user_obj.username) + unicode(datetime.datetime.now())).hexdigest()
        try:
            _record = OneTimeTokenModel.objects.get(user = self.user_id, token_type = token_type)
            _record.created_time = datetime.datetime.now() 
            _record.token = _token
            _record.is_used = False
            _record.save()
        except OneTimeTokenModel.DoesNotExist:
            _record = OneTimeTokenModel.objects.create(
                user_id = self.user_id, 
                token = _token, 
                token_type = token_type
            )
        return _token

    @staticmethod
    def get_user_id_by_email(email):
        try:
            _user_obj = AuthUser.objects.get(email = email)
            return _user_obj.id
        except Exception: 
            pass
        return None
        

    def retrieve_password(self):
        self.__ensure_user_obj()
        self.__ensure_user_profile_obj()
        _token = self.__create_one_time_token('reset_password')
        _url = 'http://www.guoku.com/reset_password/?token=' + _token
        _message = render_to_string(
            'mail/forget_password.html',
            { 
                'url' : _url, 
                'nickname' : self.user_profile_obj.nickname 
            }
        )
        _mail = Mail(u"重设果库帐号密码", _message)
        _mail.send(
            address = self.user_obj.email
        )
    
         
    def mark_footprint(self, selection = False, message = False, social_feed = False, friend_feed = False):
        _cache_key = 'user_%s_footprint'%self.user_id
        try:
            _record = UserFootprintModel.objects.get(user_id = self.user_id)
        except UserFootprintModel.DoesNotExist:
            _record = UserFootprintModel.objects.create(
                user_id = self.user_id,
                last_read_selection_time = None, 
                last_read_message_time = None,
                last_read_social_feed_time = None, 
                last_read_friend_feed_time = None
            )
        if selection:
            _record.last_read_selection_time = datetime.datetime.now()
        if message:
            _record.last_read_message_time = datetime.datetime.now()
        if social_feed:
            _record.last_read_social_feed_time = datetime.datetime.now()
        if friend_feed:
            _record.last_read_friend_feed_time = datetime.datetime.now()
        _record.save()
        
        _footprint = {} 
        _footprint['selection'] = _record.last_read_selection_time
        _footprint['message'] = _record.last_read_message_time
        cache.set(_cache_key, _footprint, 86400)

        return _footprint
            
    def get_last_read_message_time(self):
        _cache_key = 'user_%s_footprint'%self.user_id
        _footprint = cache.get(_cache_key)
        if _footprint == None:
            _footprint = self.mark_footprint()
        
        if _footprint.has_key('message') and _footprint['message'] != None:
            return _footprint['message']

        return None
    
    def get_unread_message_count(self):
        _last_read_message_time = self.get_last_read_message_time() 
        if _last_read_message_time != None:
            return NeoMessage.objects.filter(user_id = self.user_id, created_time__gt = _last_read_message_time).count()
        return 0
        

    
    def get_unread_selection_count(self):
        _cache_key = 'user_%s_footprint'%self.user_id
        _footprint = cache.get(_cache_key)
        if _footprint == None:
            _footprint = self.mark_footprint()
        
        if _footprint.has_key('selection') and _footprint['selection'] != None:
            return Selection.objects.filter(post_time__gt = _footprint['selection'], post_time__lt = datetime.datetime.now()).count() 
        else:
            pass
        
        return 0
    
