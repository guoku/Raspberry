# coding=utf8
from django.conf import settings
from base.models import Guoku_Plus as GuokuPlusModel
from base.models import Guoku_Plus as GuokuPlusTokenModel
from base.models import Seller_Info as SellerInfoModel
from base.stream_models import TaobaoShop as TaobaoShopModel
from base.stream_models import TaobaoShopInfo
from base.stream_models import TaobaoShopExtendedInfo
from base.stream_models import CrawlerInfo
from base.stream_models import TaobaoShopVerificationInfo
from base.stream_models import GuokuPlusApplication
from base.stream_models import GuokuPlusApplicationComment
from base.stream_models import ShopScore
from base.entity import Entity
from base.item import Item
import datetime
import urllib
import pymongo
   
STATUS_WAITING = 'waiting'
STATUS_ACCEPTED = 'accepted'
STATUS_REJECTED = 'rejected'

class TaobaoShop(object):
    
    def __init__(self, nick):
        self.nick = nick 
   
    @staticmethod
    def nick_exist(nick):
        return TaobaoShopModel.objects.filter(shop_info__nick = nick).count() > 0

    @staticmethod
    def find(nick, offset, num, sort_by, contained_gifts):
        if nick:
            _hdl = TaobaoShopModel.objects(shop_info__nick = nick)
        else:
            _hdl = TaobaoShopModel.objects
        if contained_gifts:
            _hdl = _hdl.filter(extended_info__gifts__in=contained_gifts)
        count = _hdl.count()
        if sort_by:
            _hdl = _hdl.order_by(sort_by)
        results = _hdl.skip(offset).limit(num)
        return results, count
        
    @classmethod
    def create(cls, nick, shop_id, title, shop_type, seller_id, pic_path):
        _now = datetime.datetime.now()
        shop = TaobaoShopModel(
            shop_info = TaobaoShopInfo(
                sid = int(shop_id),
                nick = nick, 
                title = title,
                shop_type = shop_type,
                seller_id = int(seller_id),
                pic_path = pic_path,
                shop_score = ShopScore(credit = "", praise_rate = 0),
                main_products = "",
                location = ""
            ),
            extended_info = TaobaoShopExtendedInfo(
                orientational = False,
                commission_rate = -1
            ),
            crawler_info = CrawlerInfo(priority = 10, cycle = 720),
            created_time = _now,
            last_updated_time = _now
        )
        shop.save()
        _inst = cls(nick)
        return _inst 


    def read(self, full_info = False):
        _hdl = TaobaoShopModel.objects.filter(shop_info__nick = self.nick)
        if _hdl.count() == 0:
            return None
        _doc = _hdl.first()
        _context = {}
        _context['shop_nick'] = self.nick
        _context['shop_id'] = _doc.shop_info.sid
        _context['title'] = _doc.shop_info.title
        _context['shop_type'] = _doc.shop_info.shop_type 
        _context['seller_id'] = _doc.shop_info.seller_id 

        _context['extended_info'] = _doc.extended_info._data
        _context['crawler_info'] = _doc.crawler_info._data
        if _doc.shop_info.shop_score:
            _context['shop_score'] = _doc.shop_info.shop_score._data
        
        return _context

    def update(self, priority = None, cycle = None, shop_type = None,
               orientational = None, commission = None, commission_rate = None,
               original = None, gifts = None, main_products = None, single_tail = None):
        shop = TaobaoShopModel.objects.filter(shop_info__nick = self.nick).first()
        if shop:
            if priority:
                shop.crawler_info.priority = priority
            if cycle:
                shop.crawler_info.cycle = cycle
            if shop_type:
                shop.shop_info.shop_type = shop_type
            if orientational:
                shop.extended_info.orientational = orientational
            if commission:
                shop.extended_info.commission = commission
            if commission_rate:
                shop.extended_info.commission_rate = commission_rate
            if gifts:
                shop.extended_info.gifts = gifts
            if main_products:
                shop.extended_info.main_products = main_products
            if single_tail:
                shop.extended_info.single_tail = single_tail
            shop.save()

    def create_verification_info(self, user_id, shop_type, comany_name, qq_account, email, mobile, main_products, intro):
        info = TaobaoShopVerificationInfo(
            user_id = user_id,
            shop_nick = self.nick,
            shop_type = shop_type,
            company_name = company_name,
            email = email,
            qq_account = qq_account,
            mobile = mobile,
            main_products = main_products,
            intro = intro,
            status = STATUS_WAITING,
            created_time = datetime.datetime.now()
            )
        info.save()

    def create_guoku_plus_application(self, taobao_item_id, entity_id, quantity, sale_price, remarks):
        item = GuokuPlusApplication(
            shop_nick = self.nick,
            taobao_item_id = taobao_item_id,
            entity_id = entity_id,
            quantity = quantity,
            sale_price = sale_price,
            status = STATUS_WAITING,
            remarks = remarks,
            editor_comments = [],
            seller_comments = [],
            has_new_editor_comment = False,
            has_new_seller_comment = False,
            created_time = datetime.datetime.now(),
            updated_time = datetime.datetime.now()
        )
        item.save()
   
    def read_guoku_plus_application_list(self, offset = 0, count = 100):
        return GuokuPlusApp.find(shop_nick = self.nick, offset = offset, count = count) 

    def item_exist(self, taobao_item_id):
        item = Item.get_item_by_taobao_id(taobao_item_id)
        if not item:
            return False
        item_context = item.read()
        if item_context['shop_nick'] == self.nick:
            return True
        return False

    @classmethod
    def read_shop_verification_list(cls, offset, count):
        _hdl = TaobaoShopVerificationInfo.objects
        _count = _hdl.count()
        _results = _hdl.order_by("-created_time").skip(offset).limit(count)
        results = []
        for item in _results:
            results.append(item._data)
        return results, _count

    @classmethod
    def approve_shop_verification(cls, shop_nick):
        _record = TaobaoShopVerificationInfo.objects.filter(shop_nick = shop_nick).first()
        if _record:
            SellerInfoModel.objects.create(
                    
            )
        return


class GuokuPlusApp(object):
    def __init__(self, app_id):
        self.app_id = app_id

    @classmethod
    def find(cls, shop_nick = None, status = None, offset = 0, count = 100):
        _hdl = GuokuPlusApplication.objects
        if shop_nick:
            _hdl = _hdl.filter(shop_nick = shop_nick)
        if status:
            _hdl = _hdl.filter(status = status)
        _hdl = _hdl.order_by("-updated_time")
        _count = _hdl.count()
        _results = _hdl.skip(offset).limit(count)
        results = []
        for app in _results:
            results.append(GuokuPlusApp.normalize_guoku_plus_application_data(app))
        return results, _count

    def read(self):
        app = GuokuPlusApplication.objects.filter(id = self.app_id).first()
        if app:
            return GuokuPlusApp.normalize_guoku_plus_application_data(app)
        else:
            return None

    @staticmethod
    def normalize_guoku_plus_application_data(application):
        result = {}
        result.update(application._data)
        entity = Entity(application.entity_id)
        result['entity_context'] = entity.read()
        item = Item.get_item_by_taobao_id(result['taobao_item_id'])
        if item:
            result['item_context'] = item.read()
        result['editor_comments'] = []
        result['seller_comments'] = []
        for comment in application.editor_comments:
            result['editor_comments'].append(comment._data)
        for comment in application.seller_comments:
            result['seller_comments'].append(comment._data)
        return result

    def approve(self, start_time):
        app = GuokuPlusApplication.objects.filter(id = self.app_id).first()
        if app:
            app_context = self.read()
            GuokuPlusActivity.create(
                entity_id = app_context['entity_context']['entity_id'],
                item_id = app_context['item_context']['item_id'],
                taobao_id = app_context['taobao_item_id'],
                sale_price = app_context['sale_price'],
                total_volume = app_context['quantity'],
                start_time = start_time
            )
            app.status = STATUS_ACCEPTED
            app.save()
        
    def add_editor_comment(self, comment):
        app = GuokuPlusApplication.objects.filter(id = self.app_id).first()
        if app:
            _comment = GuokuPlusApplicationComment(content = comment, created_time = datetime.datetime.now())
            app.update(push__editor_comments = _comment)
            app.has_new_editor_comment = True
            app.save()

    def add_seller_comment(self, comment):
        app = GuokuPlusApplication.objects.filter(id = self.app_id).first()
        if app:
            _comment = GuokuPlusApplicationComment(content = comment, created_time = datetime.datetime.now())
            app.update(push__editor_comments = _comment)
            app.has_new_seller_comment = True
            app.save()

    def mark_editor_comment_as_read(self):
        app = GuokuPlusApplication.objects.filter(id = self.app_id).first()
        if app:
            app.has_new_editor_comment = False
            app.save()
    
    def mark_seller_comment_as_read(self):
        app = GuokuPlusApplication.objects.filter(id = self.app_id).first()
        if app:
            app.has_new_seller_comment = False
            app.save()

GUOKU_PLUS_NORMAL = "normal"
GUOKU_PLUS_STOPPED = "stopped"
GUOKU_PLUS_FINISHED = "finished"
class GuokuPlusActivity(object):
    def __init__(self, activity_id):
        self.activity_id = activity_id

    @classmethod
    def create(cls, entity_id, item_id, taobao_id, sale_price, total_volume, start_time):
        GuokuPlusModel.objects.create(
            entity_id = entity_id,
            item_id = item_id,
            taobao_id = taobao_id,
            sale_price = sale_price,
            total_volume = total_volume,
            sales_volume = 0,
            start_time = start_time,
            status = GUOKU_PLUS_NORMAL,
            created_time = datetime.datetime.now())   
        pass

    def create_token(self, user_id):
        GuokuPlusTokenModel.objects.create(
            user_id = user_id,
            guoku_plus_activity_id = self.activity_id,
            token = "xxxx",
            used = False,
            created_time = datetime.datetime.now()
        )
    
    def use_token(self, token):
        try:
            token_obj = GuokuPlusTokenModel.objects.get(token = token) 
        except:
            return False
        if token_obj.used:
            return False
        try:
            activity = GuokuPlusModel.objects.get(id = token.guoku_plus_activity_id)
        except:
            return False
        if activity.status != GUOKU_PLUS_NORMAL:
            return False
        activity.sales_volume = activity.sales_volume + 1
        if activity.sales_volume >= activity.total_volume:
            activity.status = GUOKU_PLUS_FINISHED
        activity.save()
        token_obj.used = True
        token_obj.used_time = datetime.datetime.now()
        token_obj.save()
        return True
        
    def update(self):
        pass

    @classmethod
    def get_activity_by_token(cls, token):
        try:
            token_obj = GuokuPlusTokenModel.objects.get(token = token) 
        except:
            return None
        return cls(token_obj.guoku_plus_activity_id)
        
    def read(self):
        pass

