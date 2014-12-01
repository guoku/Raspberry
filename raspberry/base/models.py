# coding=utf8
from djangosphinx.models import SphinxSearch
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


from stream_models import *
from manager.entity import EntityManager
from base.extend.fields.listfield import ListObjectField

from django.conf import settings
from django.utils.log import getLogger

log = getLogger('django')

image_server = getattr(settings, 'IMAGE_SERVER', None)

class BaseModel(models.Model):

    class Meta:
        abstract = True

    def toDict(self):
        fields = []
        for f in  self._meta.fields:
            fields.append(f.column)
        d = {}
        for attr in fields:
            d[attr] = "%s" % getattr(self, attr)
        return d


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
    city = models.CharField(max_length = 32, null = True, default = u'朝阳')
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

    @property
    def avatar_small_url(self):
        return "%s%s" % (image_server, self.avatar_small)


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

    def get_absolute_url(self):
        return "/c/%s" % self.id

    def __unicode__(self):
        return self.title


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


    @property
    def web_url(self):

        if self.content_type == 'entity':
            try:
                entity = Entity.objects.get(pk = self.key)
            except Entity.DoesNotExist, e:
                log.error(e.message)
                return
            return reverse('web_detail', args=[entity.entity_hash])


class Entity(BaseModel):
    entity_hash = models.CharField(max_length=32, unique=True, db_index=True)
    creator_id = models.IntegerField(default=None, null=True, db_index=True)
    category = models.ForeignKey(Category)
    neo_category = models.ForeignKey(Neo_Category)
    brand = models.CharField(max_length=256, null=False, default='')
    title = models.CharField(max_length=256, null=False, default='')
    intro = models.TextField(null=False, default='')
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, db_index=True)
    like_count = models.IntegerField(default=0, db_index=True)
    mark = models.IntegerField(default=0, db_index=True)
    chief_image = models.CharField(max_length=64, null=False)
    detail_images = models.CharField(max_length=1024, null=True)
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)
    novus_time = models.DateTimeField(db_index=True)
    weight = models.IntegerField(default=0, db_index=True)
    rank_score = models.IntegerField(default=0, db_index=True)

    objects = EntityManager()
    
    search = SphinxSearch( 
        index='entities',
        weights={ 
            'title': 20,
            'brand': 10,
            'intro': 5,
        }, 
        mode='SPH_MATCH_ALL',
        rankmode='SPH_RANK_NONE',
    )

    # @property
    # def like_count(self):
    #     return self.entity_like_set.count()

    class Meta:
        ordering = ['-created_time']

    def get_absolute_url(self):
        return "/detail/%s" % self.entity_hash

    def __unicode__(self):
        return self.title


class Entity_Like(models.Model):
    entity = models.ForeignKey(Entity)
    user_id = models.IntegerField(null = False, db_index = True)
    created_time = models.DateTimeField(auto_now_add = True, db_index=True)
    
    class Meta:
        db_table = 'guoku_entity_like'
        ordering = ['-created_time']
        unique_together = ('entity', 'user_id')


class Note(models.Model):
    entity = models.ForeignKey(Entity, related_name="notes")
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

    def __unicode__(self):
        return self.note


class Note_Poke(models.Model):
    note = models.ForeignKey(Note)
    user_id = models.IntegerField(null = False, db_index = True)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    
    class Meta:
        ordering = ['-created_time']
        unique_together = ('note', 'user_id')


class Note_Comment(models.Model):
    note = models.ForeignKey(Note)
    creator = models.ForeignKey(User)
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
    
    search = SphinxSearch( 
        index = 'tags',
        mode = 'SPH_MATCH_ALL',
        rankmode = 'SPH_RANK_NONE',
    )

    def get_absolute_url(self):

        return "/t/%s" % self.tag_hash

    class Meta:
        ordering = ['-created_time']


class Entity_Tag(models.Model):
    entity = models.ForeignKey(Entity)
    user = models.ForeignKey(User) 
    tag = models.ForeignKey(Tag)
    tag_text = models.CharField(max_length = 128, null = False, db_index = True)
    tag_hash = models.CharField(max_length = 32, db_index = True)
    count = models.IntegerField(default = 0)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    last_tagged_time = models.DateTimeField(db_index = True)
    
    class Meta:
        ordering = ['-created_time']
        unique_together = ('entity', 'user', 'tag')

    def get_absolute_url(self):
        return "/t/%s" % self.tag_hash

    def __unicode__(self):
        return self.tag


class Recommend_User_Tag(models.Model):
    user = models.ForeignKey(User) 
    tag = models.CharField(max_length = 128, null = False, db_index = True)
    entity_count = models.IntegerField(default = 0, db_index = True)
    created_time = models.DateTimeField(db_index=True)
    class Meta:
        ordering = ['-created_time']
        unique_together = ('user', 'tag')


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
    taobao_id = models.CharField(max_length = 64, null = True, db_index = True)
    screen_name = models.CharField(max_length = 64, null = True, db_index = True)
    access_token = models.CharField(max_length = 255, null = True, db_index = True)
    refresh_token = models.CharField(max_length = 255, null = True, db_index = True)
    create_time = models.DateTimeField(auto_now_add = True)
    expires_in = models.PositiveIntegerField(default = 0)
    re_expires_in = models.PositiveIntegerField(default = 0)
    updated_time = models.DateTimeField(auto_now = True, null = True)


class One_Time_Token(models.Model):
    user = models.ForeignKey(User, related_name="one_time_token") 
    token = models.CharField(max_length=255, db_index=True)
    token_type = models.CharField(max_length=30, db_index=True)
    is_used = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now=True)


class User_Footprint(models.Model):
    user = models.ForeignKey(User)
    last_read_selection_time = models.DateTimeField(null = True, db_index = True)
    last_read_message_time = models.DateTimeField(null = True, db_index = True)
    last_read_social_feed_time = models.DateTimeField(null = True, db_index = True)
    last_read_friend_feed_time = models.DateTimeField(null = True, db_index = True)


class Seller_Info(models.Model):
    user = models.OneToOneField(User, related_name = "seller_info")
    shop_nick = models.CharField(max_length = 64, db_index = True)
    shop_type = models.CharField(null = True, max_length = 20, db_index = True)
    company_name = models.CharField(null = True, max_length = 100)
    qq_account = models.CharField(null = True, max_length = 50)
    email = models.CharField(null = True, max_length = 50)
    mobile = models.CharField(null = True, max_length = 20)
    main_products = models.CharField(null = True, max_length = 50)
    intro = models.CharField(null = True, max_length = 500)
    verified = models.BooleanField(default = False, db_index = True)


class Guoku_Plus(models.Model):
    entity = models.ForeignKey(Entity)
    item_id = models.CharField(max_length = 32, db_index = True)
    taobao_id = models.CharField(max_length = 32, db_index = True)
    shop_nick = models.CharField(max_length = 50, db_index = True)
    sale_price = models.FloatField()
    total_volume = models.IntegerField()
    sales_volume = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null = True)
    seller_remarks = models.CharField(null = True, max_length = 100)
    editor_remarks = models.CharField(null = True, max_length = 100)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    status = models.CharField(max_length = 32, db_index = True)


class Guoku_Plus_Token(models.Model):
    user = models.ForeignKey(User)
    guoku_plus_activity = models.ForeignKey(Guoku_Plus)
    token = models.CharField(max_length = 50, unique = True, db_index = True)
    used = models.BooleanField()
    created_time = models.DateTimeField()
    used_time = models.DateTimeField(null = True)
    quantity = models.IntegerField(null = True)


class Novus_Stat(models.Model):
    year = models.IntegerField(db_index=True)
    month = models.IntegerField(db_index=True)
    date = models.IntegerField(db_index=True)
    hour = models.IntegerField(db_index=True)
    list_impression = models.IntegerField(db_index=True)
    edit_impression = models.IntegerField(db_index=True)
    novus = models.IntegerField(db_index=True)


# event banner

class Event(models.Model):
    tag = models.CharField(max_length=30, null=False, default='')
    slug = models.CharField(max_length=100, null=False, db_index=True, unique=True)
    status = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['-created_datetime']

    @property
    def has_banner(self):
        count = self.banner.count()
        if count > 0:
            return True
        return False

    @property
    def banners(self):
        count = self.banner.count()
        return count

    @property
    def has_recommendation(self):
        count = self.recommendation.count()
        if count > 0 :
            return True
        return False

    @property
    def recommendations(self):
        count = self.recommendation.count()
        return count

    @property
    def tag_url(self):
        return reverse('web_tag_detail', args=[self.tag])

    @property
    def slug_url(self):
        return reverse('web_event', args=[self.slug])


class Event_Banner(models.Model):
    (item, shop) = (0, 1)
    BANNER_TYPE__CHOICES = [
        (item, _("item")),
        (shop, _("shop")),
    ]

    image = models.CharField(max_length=255, null=False)
    banner_type = models.IntegerField(choices=BANNER_TYPE__CHOICES, default=item)
    user_id = models.CharField(max_length=30, null=True)
    link = models.CharField(max_length=255, null=True)
    created_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        ordering = ['-created_time']

    @property
    def image_url(self):
        return "%s%s" % (image_server, self.image)

    @property
    def position(self):
        try:
            return self.show.pk
        except Show_Event_Banner.DoesNotExist:
            return 0

    @property
    def has_show_banner(self):
        try:
            self.show
            return True
        except Show_Event_Banner.DoesNotExist:
            return False

class Show_Event_Banner(models.Model):
    banner = models.OneToOneField(Event_Banner, related_name='show')
    event = models.ForeignKey(Event, related_name='banner', null=True)
    position = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        ordering = ['id']

# editor recommendation

class Editor_Recommendation(models.Model):
    image = models.CharField(max_length=255, null=False)
    link = models.CharField(max_length=255, null=False)
    created_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        ordering = ['-created_time']

    @property
    def image_url(self):
        return "%s%s" % (image_server, self.image)

    @property
    def position(self):
        try:
            return self.show.pk
        except Show_Editor_Recommendation.DoesNotExist:
            return 0

    @property
    def has_show_banner(self):
        try:
            self.show
            return True
        except Show_Editor_Recommendation.DoesNotExist:
            return False


class Show_Editor_Recommendation(models.Model):
    recommendation = models.OneToOneField(Editor_Recommendation, related_name='show', unique=False)
    event = models.ForeignKey(Event, related_name='recommendation', null=True)
    position = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        ordering = ['id']