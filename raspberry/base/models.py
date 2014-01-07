# coding=utf8
from djangosphinx.models import SphinxSearch
from django.contrib.auth.models import User
from django.db import models

class User_Profile(models.Model):
    Man = u'M'
    Woman = u'F'
    Other = u'O'
    GENDER_CHOICES = (
        (Man, u'男'),
        (Woman,  u'女'),
        (Other,  u'其他')
    )
    
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length = 64, db_index = True, unique = True)
    location = models.CharField(max_length = 32, null = True, default = u'北京')
    gender = models.CharField(max_length = 2, choices = GENDER_CHOICES, default = Other)
    bio = models.CharField(max_length = 1024, null = True, blank = True)
    website = models.CharField(max_length = 1024, null = True, blank = True)
    email_verified = models.BooleanField(default = False)

    search = SphinxSearch( 
        index = 'users',
        mode = 'SPH_MATCH_ALL',
        rankmode = 'SPH_RANK_NONE',
    )
    
    def __unicode__(self):
        return self.nickname
    
    class Meta:
        app_label = 'base'
    
class Avatar(models.Model):
    user = models.OneToOneField(User)
    avatar_origin = models.CharField(max_length = 1024, db_index = True, null = False, blank = False)
    avatar_small = models.CharField(max_length = 1024, db_index = True, null = False, blank = False)
    avatar_large = models.CharField(max_length = 1024, db_index = True, null = False, blank = False)
    uploaded_time = models.DateField(auto_now_add = True, db_index = True)
    
    class Meta:
        app_label = 'base'
        ordering = ['-uploaded_time']

class Seed_User(models.Model):
    user_id = models.IntegerField(null = False, db_index = True, unique = True)
    weight = models.IntegerField(default = 0, db_index = True)

class User_Censor(models.Model):
    user = models.OneToOneField(User) 
    censor = models.ForeignKey(User, related_name = "censor") 
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    class Meta:
        db_table = 'guoku_user_censor'
        ordering = ['-created_time']


class Neo_Category_Group(models.Model):
    title = models.CharField(max_length = 128, db_index = True)
    status = models.IntegerField(default = 1, db_index = True)
    class Meta:
        ordering = ['id']


class Neo_Category(models.Model):
    group = models.ForeignKey(Neo_Category_Group)
    title = models.CharField(max_length = 128, db_index = True, unique = True)
    image_store_hash = models.CharField(max_length = 64, db_index = True, null = True, default = None)
    status = models.IntegerField(default = 1, db_index = True)
    class Meta:
        ordering = ['id']

class Category(models.Model):
    pid = models.IntegerField(default = 0)
    title = models.CharField(max_length = 256)
    english_title = models.CharField(max_length = 256)
    level = models.IntegerField(default = 0)
    status = models.IntegerField(default = 1, db_index = True)

class Taobao_Item_Category_Mapping(models.Model):
    taobao_category_id = models.IntegerField(db_index = True, unique = True)
    parent_id = models.IntegerField(default = 0)
    title = models.CharField(max_length = 256)
    guoku_category = models.ForeignKey(Category)
 
class Taobao_Item_Neo_Category_Mapping(models.Model):
    taobao_category_id = models.IntegerField(db_index = True, unique = True)
    neo_category_id = models.IntegerField(db_index = True)

class Banner(models.Model):
    content_type = models.CharField(max_length = 64, null = False)
    key = models.CharField(max_length = 1024, null = False)
    image = models.CharField(max_length = 64, null = False)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)
    weight = models.IntegerField(default = 0, db_index = True)
    class Meta:
        ordering = ['-created_time']


class Entity(models.Model):
    entity_hash = models.CharField(max_length = 32, unique = True, db_index = True)
    creator_id = models.IntegerField(default = None, null = True, db_index = True)
    category = models.ForeignKey(Category)
    neo_category = models.ForeignKey(Neo_Category)
    brand = models.CharField(max_length = 256, null = False, default = '')
    title = models.CharField(max_length = 256, null = False, default = '')
    intro = models.TextField(null = False, default = '')
    price = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0, db_index = True)
    like_count = models.IntegerField(default = 0, db_index = True)
    mark = models.IntegerField(default = 0, db_index = True)
    chief_image = models.CharField(max_length = 64, null = False)
    detail_images = models.CharField(max_length = 1024, null = True)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)
    weight = models.IntegerField(default = 0, db_index = True)
    
    search = SphinxSearch( 
        index = 'entities',
        weights = { 
            'title' : 20,
            'brand' : 10,
            'intro' : 5,
        }, 
        mode = 'SPH_MATCH_ALL',
        rankmode = 'SPH_RANK_NONE',
    )

    class Meta:
        ordering = ['-created_time']

 
class Entity_Like(models.Model):
    entity = models.ForeignKey(Entity)
    user_id = models.IntegerField(null = False, db_index = True)
    created_time = models.DateTimeField(auto_now_add = True, db_index=True)
    
    class Meta:
        db_table = 'guoku_entity_like'
        ordering = ['-created_time']
        unique_together = ('entity', 'user_id')

class Note(models.Model):
    entity = models.ForeignKey(Entity)
    note = models.TextField(null = True)
    score = models.IntegerField(db_index = True, default = 0)
    figure = models.CharField(max_length = 256, null = False, default = '')
    creator_id = models.IntegerField(null = False, db_index = True)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)
    post_time = models.DateTimeField(null = True, db_index = True)
    selector = models.ForeignKey(User, null = True, db_index = True, related_name = "selected_note") 
    selected_time = models.DateTimeField(null = True)
    poke_count = models.IntegerField(default = 0, db_index = True)
    weight = models.IntegerField(default = 0, db_index = True)
    
    search = SphinxSearch( 
        index = 'notes',
        mode = 'SPH_MATCH_ALL',
        rankmode = 'SPH_RANK_NONE',
    )

    class Meta:
        ordering = ['-created_time']
        unique_together = ('entity', 'creator_id')

class Note_Poke(models.Model):
    note = models.ForeignKey(Note)
    user_id = models.IntegerField(null = False, db_index = True)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    
    class Meta:
        ordering = ['-created_time']
        unique_together = ('note', 'user_id')

class Note_Comment(models.Model):
    note = models.ForeignKey(Note)
    creator_id = models.IntegerField(null = False, db_index = True)
    comment = models.TextField(null = False)
    replied_comment_id = models.IntegerField(default = None, null = True, db_index = True)
    replied_user_id = models.IntegerField(default = None, null = True, db_index = True)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)
    class Meta:
        ordering = ['-created_time']

class Tag(models.Model):
    tag = models.CharField(max_length = 128, null = False, unique = True, db_index = True)
    tag_hash = models.CharField(max_length = 32, unique = True, db_index = True)
    status = models.IntegerField(default = 0, db_index = True)
    creator = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add = True, db_index=True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)

    class Meta:
        ordering = ['-created_time']

class Entity_Tag(models.Model):
    entity = models.ForeignKey(Entity)
    user = models.ForeignKey(User) 
    tag = models.ForeignKey(Tag)
    count = models.IntegerField(default = 0)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    last_tagged_time = models.DateTimeField(db_index = True)
    
    class Meta:
        ordering = ['-created_time']
        unique_together = ('entity', 'user', 'tag')

    def __unicode__(self):
        return self.tag

class User_Follow(models.Model):
    follower = models.ForeignKey(User, related_name = "followings")
    followee = models.ForeignKey(User, related_name = "fans")
    followed_time = models.DateTimeField(auto_now_add = True, db_index = True)
    class Meta:
        app_label = 'base'
        ordering = ['-followed_time']
        unique_together = ("follower", "followee")

class Sina_Token(models.Model):
    user = models.OneToOneField(User)
    sina_id = models.CharField(max_length = 64, null = True, db_index = True)
    screen_name = models.CharField(max_length = 64, null = True, db_index = True)
    access_token = models.CharField(max_length = 255, null = True, db_index = True)
    create_time = models.DateTimeField(auto_now_add = True)
    expires_in = models.PositiveIntegerField(default = 0)
    updated_time = models.DateTimeField(auto_now = True, null = True) 

class Taobao_Token(models.Model):
    user = models.OneToOneField(User)
    taobao_user_nick = models.CharField(max_length = 64, null = True, db_index = True)
    taobao_id = models.CharField(max_length = 64, null = True, db_index = True)
    screen_name = models.CharField(max_length = 64, null = True, db_index = True)
    access_token = models.CharField(max_length = 255, null = True, db_index = True)
    refresh_token = models.CharField(max_length = 255, null = True, db_index = True)
    create_time = models.DateTimeField(auto_now_add = True)
    expires_in = models.PositiveIntegerField(default = 0)
    re_expires_in = models.PositiveIntegerField(default = 0)
    updated_time = models.DateTimeField(auto_now = True, null = True)


class One_Time_Token(models.Model):
    user = models.ForeignKey(User, related_name = "one_time_token") 
    token = models.CharField(max_length = 255, db_index = True)
    token_type = models.CharField(max_length = 30, db_index = True)
    is_used = models.BooleanField(default = False)

class User_Footprint(models.Model):
    user = models.ForeignKey(User)
    last_read_selection_time = models.DateTimeField(null = True, db_index = True)
    last_read_message_time = models.DateTimeField(null = True, db_index = True)
    last_read_social_feed_time = models.DateTimeField(null = True, db_index = True)
    last_read_friend_feed_time = models.DateTimeField(null = True, db_index = True)


from mongoengine import * 
class Image(Document):
    source = StringField(required = True)
    origin_url  = URLField(required = False)
    store_hash = StringField(required = False)
    created_time = DateTimeField(required = True)
    updated_time = DateTimeField(required = True)
    meta = {
        'indexes' : [ 
            'source',
            'origin_url',
            'store_hash',
        ],
        'allow_inheritance' : True
    }

class Item(Document):
    entity_id = IntField(required = True) 
    source = StringField(required = True)
    images = ListField(required = False)
    created_time = DateTimeField(required = True)
    updated_time = DateTimeField(required = True)
    meta = {
        'indexes' : [ 
            'entity_id' 
        ],
        'allow_inheritance' : True
    }

class TaobaoItem(Item):
    taobao_id = StringField(required = True, unique = True)
    cid = IntField(required = True) 
    title = StringField(required = True)
    shop_nick = StringField(required = True)
    price = DecimalField(required = True)
    soldout = BooleanField(required = True) 

    meta = {
        'indexes' : [ 
            'taobao_id',
            'cid',
            'shop_nick',
            'price',
            'soldout'
        ],
    }
    
class Selection(Document):
    selector_id = IntField(required = True) 
    selected_time = DateTimeField(required = True)
    post_time = DateTimeField(required = True)
    meta = {
        "indexes" : [ 
            "selector_id", 
            "post_time" 
        ],
        "allow_inheritance" : True
    }

class NoteSelection(Selection):
    entity_id = IntField(required = True) 
    note_id = IntField(required = True) 
    root_category_id = IntField(required = True) 
    neo_category_group_id = IntField(required = True) 
    neo_category_id = IntField(required = True) 
    category_id = IntField(required = True) 
    meta = {
        "indexes" : [ 
            "entity_id", 
            "note_id",
            "root_category_id",
            "neo_category_group_id",
            "neo_category_id",
            "category_id" 
        ]
    }

class Seller_Info(models.Model):
    user = models.OneToOneField(User, related_name = "seller_info")
    shop_nick = models.CharField(max_length = 64, db_index = True)
    verified = models.BooleanField(default = False)
