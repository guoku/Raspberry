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
from base.stream_models import ShopScore
from base.entity import Entity
from base.item import Item
from base.user import User
from utils.lib import get_random_string
import datetime
import urllib
import pymongo
   
STATUS_WAITING = 'waiting'
STATUS_APPROVED = 'approved'
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
        
        try:
            _seller_info_obj = SellerInfoModel.objects.get(shop_nick = self.nick)
            _context['user_id'] = _seller_info_obj.user_id
            _context['shop_type'] = _seller_info_obj.shop_type
            _context['shop_company_name'] = _seller_info_obj.company_name
            _context['shop_qq_account'] = _seller_info_obj.qq_account
            _context['shop_email'] = _seller_info_obj.email
            _context['shop_mobile'] = _seller_info_obj.shop_type
            _context['shop_main_products'] = _seller_info_obj.main_products
            _context['shop_intro'] = _seller_info_obj.intro
            _context['shop_verified'] = _seller_info_obj.verified
        except:
            pass
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

    def update_seller_info(self,
                           shop_type = None,
                           company_name = None,
                           qq_account = None,
                           email = None,
                           mobile = None,
                           main_products = None,
                           intro = None,
                           verified = None):
        _seller = SellerInfoModel.objects.get(shop_nick = self.nick)
        if shop_type:
            _seller.shop_type = shop_type
        if company_name:
            _seller.company_name = company_name
        if qq_account:
            _seller.qq_account = qq_account
        if email:
            _seller.email = email
        if mobile:
            _seller.mobile = mobile
        if main_products:
            _seller.main_products
        if intro:
            _seller.intro = intro
        if verified:
            _seller.verified = verified
        _seller.save()

    def update_verification_info(self, shop_type, company_name, qq_account, email, mobile, main_products, intro):
        info = TaobaoShopVerificationInfo.objects.filter(shop_nick = self.nick).first()
        if not info:
            return False
        info.status = STATUS_WAITING
        info.updated_time = datetime.datetime.now()
        info.save()
        self.update_seller_info(
            shop_type = shop_type,
            company_name = company_name,
            qq_account = qq_account,
            email = email,
            mobile = mobile,
            main_products = main_products,
            intro = intro
        )
        return True

    def create_verification_info(self,  shop_type, company_name, qq_account, email, mobile, main_products, intro):
        if TaobaoShopVerificationInfo.objects.filter(shop_nick = self.nick).count() > 0:
            return False
        time_now = datetime.datetime.now()
        info = TaobaoShopVerificationInfo(
            shop_nick = self.nick,
            status = STATUS_WAITING,
            created_time = time_now,
            updated_time = time_now
        )
        info.save()
        self.update_seller_info(
            shop_type = shop_type,
            company_name = company_name,
            qq_account = qq_account,
            email = email,
            mobile = mobile,
            main_products = main_products,
            intro = intro
        )
        return True
    def read_guoku_plus_list(self, offset = 0, count = 100):
        return GuokuPlusActivity.find(shop_nick = self.nick, offset = offset, count = count) 

    def item_exist(self, taobao_item_id):
        item = Item.get_item_by_taobao_id(taobao_item_id)
        if not item:
            return False
        item_context = item.read()
        if item_context['shop_nick'] == self.nick:
            return True
        return False

    def read_shop_verification(self):
        verification = TaobaoShopVerificationInfo.objects.filter(shop_nick = self.nick).first()
        if verification:
            return verification._data
        else:
            return None

    @classmethod
    def read_shop_verification_list(cls, offset, count):
        _hdl = TaobaoShopVerificationInfo.objects
        _count = _hdl.count()
        _results = _hdl.order_by("-created_time").skip(offset).limit(count)
        results = []
        for item in _results:
            results.append({"verification" : item._data, "shop_context" : TaobaoShop(item.shop_nick).read()})
        return results, _count

    def handle_shop_verification(self, action):
        _record = TaobaoShopVerificationInfo.objects.filter(shop_nick = self.nick).first()
        if not _record:
            return
        if action == "approve":
            self.update_seller_info(verified = True)
            _record.status = STATUS_APPROVED
            _record.save()
        elif action == "reject":
            self.update_seller_info(verified = False)
            _record.status = STATUS_REJECTED
            _record.save()

################################################

ACTIVITY_WAITING = "waiting"
ACTIVITY_APPROVED = "approved"
ACTIVITY_REJECTED = "rejected"
ACTIVITY_ONGOING = "ongoing"
ACIIVITY_FINISHED = "finished"
ACIIVITY_ABORTED = "aborted"

class GuokuPlusActivity(object):
    def __ensure_activity_obj(self):
        if not hasattr(self, 'activity_obj'):
            self.activity_obj = GuokuPlusModel.objects.get(pk = self.activity_id)
    
    def __init__(self, activity_id):
        self.activity_id = activity_id
        self.__ensure_activity_obj()

    def __get_context(self):
        context = {}
        entity = Entity(self.activity_obj.entity_id)
        item = Item(self.activity_obj.item_id)
        context['activity_id'] = self.activity_obj.id
        context['entity_context'] = entity.read()
        context['item_context'] = item.read()
        context['shop_nick'] = self.activity_obj.shop_nick
        context['taobao_id'] = self.activity_obj.taobao_id
        context['sale_price'] = self.activity_obj.sale_price
        context['total_volume'] = self.activity_obj.total_volume
        context['sales_volume'] = self.activity_obj.sales_volume
        context['start_time'] = self.activity_obj.start_time
        context['seller_remarks'] = self.activity_obj.seller_remarks
        context['editor_remarks'] = self.activity_obj.editor_remarks
        context['created_time'] = self.activity_obj.created_time
        context['updated_time'] = self.activity_obj.updated_time
        context['status'] = self.activity_obj.status
        return context

    @classmethod
    def create(cls, taobao_id, sale_price, total_volume, seller_remarks, shop_nick):
        item_inst = Item.get_item_by_taobao_id(taobao_id)
        item_context = item_inst.read()
        time_now = datetime.datetime.now()
        start_time = time_now + datetime.timedelta(100000) #set start time as 100000 days later
        GuokuPlusModel.objects.create(
            entity_id = item_context['entity_id'],
            item_id = item_context['item_id'],
            taobao_id = taobao_id,
            sale_price = sale_price,
            total_volume = total_volume,
            sales_volume = 0,
            seller_remarks = seller_remarks,
            shop_nick = shop_nick,
            status = ACTIVITY_WAITING,
            start_time = start_time,
            created_time = time_now,
            updated_time = time_now)   

    @classmethod
    def find(cls, shop_nick = None, status = None, offset = 0, count = 100):
        _hdl = GuokuPlusModel.objects.all()
        if shop_nick:
            _hdl = _hdl.filter(shop_nick = shop_nick)
        if status:
            _hdl = _hdl.filter(status = status)
        total = _hdl.count()
        _hdl = _hdl[offset : offset + count]
        results = []
        for item in _hdl:
            print item
            results.append(GuokuPlusActivity(item.id).read())
        print results
        return results, total

    def handle(self, action, editor_remarks = None, start_time = None):
        if action == "approve":
            self.activity_obj.status = ACTIVITY_APPROVED
        elif action == "reject":
            self.activity_obj.status = ACTIVITY_REJECTED
        if start_time != None:
            self.activity_obj.start_time = start_time
        if editor_remarks != None:
            self.activity_obj.editor_remarks = editor_remarks
        self.activity_obj.save()

    def reject(self, editor_remarks = None):
        self.activity_obj.status = ACTIVITY_REJECTED
        self.activity_obj.editor_remarks = editor_remarks
        self.activity_obj.save()
    
    def update(self, sale_price = None, total_volume = None):
        if sale_price:
            self.activity_obj.sale_price = sale_price
        if total_volume:
            self.activity_obj.total_volume = total_volume
        self.activity_obj.save()

    def read(self):
        return self.__get_context()

    def create_token(self, user_id):
        try_times = 10
        while try_times > 0:
            try:
                GuokuPlusTokenModel.objects.create(
                    user_id = user_id,
                    guoku_plus_activity_id = self.activity_id,
                    token = get_random_string(7),
                    used = False,
                    created_time = datetime.datetime.now()
                )
                return True
            except:
                try_times -= 1
        return False
    
    def use_token(self, token):
        try:
            token_obj = GuokuPlusTokenModel.objects.get(token = token) 
        except:
            return False
        if token_obj.used:
            return False
        if self.activity_obj.activity_status != ACTIVITY_ONGOING:
            return False
        self.activity_obj.sales_volume = self.activity_obj.sales_volume + 1
        if self.activity_obj.sales_volume >= self.activity_obj.total_volume:
            self.activity_obj.activity_status = ACTIVITY_FINISHED
        self.activity_obj.save()
        token_obj.used = True
        token_obj.used_time = datetime.datetime.now()
        token_obj.save()
        return True
        
    @classmethod
    def get_activity_by_token(cls, token):
        try:
            token_obj = GuokuPlusTokenModel.objects.get(token = token) 
        except:
            return None
        return cls(token_obj.guoku_plus_activity_id)
        
