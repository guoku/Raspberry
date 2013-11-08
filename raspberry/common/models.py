# coding=utf8
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

    def __unicode__(self):
        return self.nickname
    
    class Meta:
        app_label = 'base'
    
class Avatar(models.Model):
    user = models.OneToOneField(User)
    avatar_origin = models.CharField(max_length = 1024, db_index = True, null = False, blank = False)
    avatar_small = models.CharField(max_length = 1024, db_index = True, null = False, blank = False)
    avatar_large = models.CharField(max_length = 1024, db_index = True, null = False, blank = False)
    uploaded_time = models.DateTimeField(auto_now_add = True, db_index = True)
    
    class Meta:
        app_label = 'base'
        ordering = ['-uploaded_time']

class Category_Group(models.Model):
    title = models.CharField(max_length = 128, db_index = True)
    status = models.IntegerField(default = 1, db_index = True)
    class Meta:
        ordering = ['id']


class Category(models.Model):
    group = models.ForeignKey(Category_Group)
    title = models.CharField(max_length = 128, db_index = True, unique = True)
    image_store_hash = models.CharField(max_length = 64, db_index = True, null = True, default = None)
    status = models.IntegerField(default = 1, db_index = True)
    class Meta:
        ordering = ['id']
 

class Entity(models.Model):
    entity_hash = models.CharField(max_length = 32, unique = True, db_index = True)
    creator_id = models.IntegerField(default = None, null = True, db_index = True)
    category = models.ForeignKey(Category)
    brand = models.CharField(max_length = 256, null = False, default = '')
    title = models.CharField(max_length = 256, null = False, default = '')
    intro = models.TextField(null = True)
    price = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0, db_index = True)
    chief_image = models.CharField(max_length = 64, null = False)
    detail_images = models.CharField(max_length = 1024, null = True)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)
    weight = models.IntegerField(default = 0, db_index = True)
    is_candidate = models.BooleanField(db_index = True, default = False)
    class Meta:
        ordering = ['-created_time']

 
class Entity_Like(models.Model):
    entity = models.ForeignKey(Entity)
    user_id = models.IntegerField(null = False, db_index = True)
    created_time = models.DateTimeField(auto_now_add = True, db_index=True)
    
    class Meta:
        ordering = ['-created_time']
        unique_together = ('entity', 'user_id')

class Note(models.Model):
    entity = models.ForeignKey(Entity)
    note = models.TextField(null = True)
    score = models.IntegerField(db_index = True, default = 0)
    figures = models.CharField(max_length = 1024, null = True)
    creator_id = models.IntegerField(null = False, db_index = True)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)

    class Meta:
        ordering = ['-created_time']

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
    reply_to_comment_id = models.IntegerField(default = None, null = True, db_index = True)
    reply_to_user_id = models.IntegerField(default = None, null = True, db_index = True)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    class Meta:
        ordering = ['-created_time']

class User_Follow(models.Model):
    follower = models.ForeignKey(User, related_name = "followings")
    followee = models.ForeignKey(User, related_name = "fans")
    followed_time = models.DateTimeField(auto_now_add = True, db_index = True)
    class Meta:
        app_label = 'base'
        ordering = ['-followed_time']
        unique_together = ("follower", "followee")

