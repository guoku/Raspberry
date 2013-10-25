# coding=utf8
from models import Entity as RBEntityModel
from models import Entity_Like as RBEntityLikeModel
from models import Entity_Note as RBEntityNoteModel
from django.conf import settings
from django.db.models import Sum
from mango.client import MangoApiClient
from note import RBNote
from hashlib import md5
import datetime
import urllib
import time



class RBEntity(object):

    def __init__(self, entity_id):
        self.entity_id = entity_id
    
    @classmethod
    def cal_entity_hash(cls, entity_hash_string):
        while True:
            _hash = md5(entity_hash_string + unicode(datetime.datetime.now())).hexdigest()[0:8]
            try:
                Entity.objects.get(entity_hash = _hash)
            except:
                break
        return _hash 
    
    def get_entity_id(self):
        return self.entity_id
    
    @staticmethod
    def check_taobao_item_exist(taobao_id):
        _mango_client = MangoApiClient()
        return _mango_client.check_taobao_item_exist(taobao_id)
    
    @classmethod
    def create_by_taobao_item(cls, creator_id, category_id, chief_image_url, 
                              taobao_item_info, brand = "", title = "", intro = "", detail_image_urls = []):
       
        _mango_client = MangoApiClient()
        _entity_id = _mango_client.create_entity_by_taobao_item(
            taobao_item_info = taobao_item_info,
            chief_image_url = chief_image_url,
            brand = brand,
            title = title,
            intro = intro,
            detail_image_urls = detail_image_urls
        )
       
        _entity_hash = cls.cal_entity_hash(taobao_item_info['taobao_id'])
        _entity_obj = RBEntityModel.objects.create( 
            entity_id = _entity_id,
            entity_hash = _entity_hash,
            category_id = category_id,
            creator_id = creator_id
        )
         
        _inst = cls(_entity_obj.entity_id)
        _inst.__entity_obj = _entity_obj
        return _inst

    
    def add_taobao_item(self, taobao_item_info, image_urls = []):
        _mango_client = MangoApiClient()
        _item_id = _mango_client.add_taobao_item_for_entity(self.entity_id, taobao_item_info, image_urls)
    
    
    def __ensure_entity_obj(self):
        if not hasattr(self, '__entity_obj'):
            self.__entity_obj = RBEntityModel.objects.get(entity_id = self.entity_id)

    def __load_entity_context(self, meta_context):
        self.__ensure_entity_obj()
        _context = meta_context 
        _context["entity_hash"] = self.__entity_obj.entity_hash
        _context["category_id"] = self.__entity_obj.category_id
        _context["created_time"] = self.__entity_obj.created_time
        _context["updated_time"] = self.__entity_obj.updated_time
        

        _context["total_score"] = 0 
        _context["score_count"] = 0 
        _context["note_id_list"] = []
        for _entity_note_obj in RBEntityNoteModel.objects.filter(entity_id = self.entity_id):
            _context["note_id_list"].append(_entity_note_obj.note_id)
            _context["total_score"] += _entity_note_obj.score
            _context["score_count"] += 1

        return _context
        

    def read(self, json = False):
        _mango_client = MangoApiClient()
        _meta_context = _mango_client.read_entity(self.entity_id)
        _context = self.__load_entity_context(_meta_context)
        if json:
            _context['created_time'] = time.mktime(_context["created_time"].timetuple())
            _context['updated_time'] = time.mktime(_context["updated_time"].timetuple())
        return _context    
    
    
    def update(self, category_id = None, brand = None, title = None, intro = None, price = None):
        if brand != None or title != None or intro != None:
            _mango_client = MangoApiClient()
            _base_info = _mango_client.read_entity(self.entity_id)
            
            if brand != None or title != None or intro != None or price != None:
                _mango_client.update_entity(
                    entity_id = self.entity_id, 
                    brand = brand, 
                    title = title, 
                    intro = intro,
                    price = price
                )
        
        if category_id != None:
            self.__ensure_entity_obj()
            self.__entity_obj.category_id = int(category_id)
            self.__entity_obj.save()
            
   
    @classmethod
    def read_entities(cls, entity_id_list):
        _mango_client = MangoApiClient()
        _context_list = []
        for _entity_id in entity_id_list:
            _context = cls(_entity_id).read()
            _context['base_info'] = _mango_client.read_entity(_entity_id)
            _context_list.append(_context)
        return _context_list
             
       
    @classmethod
    def find(cls, category_id = None, timestamp = None, offset = 0, count = 30):
        _hdl = RBEntityModel.objects
        if category_id != None:
            _hdl = _hdl.filter(category_id = category_id)
        if timestamp != None:
            _hdl = _hdl.filter(created_time__lt = timestamp)
        _hdl = _hdl.order_by('-created_time')[offset : offset + count]
        _entity_id_list = map(lambda x: x.entity_id, _hdl)
        return _entity_id_list
        
    @classmethod
    def count(cls, category_id = None):
        _hdl = RBEntityModel.objects.filter(category_id = category_id)
        return _hdl.count()
    
    def bind_item(self, item_id):
        _mango_client = MangoApiClient()
        _mango_client.bind_entity_item(self.entity_id, item_id)
    
    def unbind_item(self, item_id):
        _mango_client = MangoApiClient()
        _mango_client.unbind_entity_item(self.entity_id, item_id)

    def like(self, user_id):
        try:
            RBEntityLikeModel.objects.create(
                entity_id = self.entity_id,
                user_id = user_id
            )
            return True
        except:
            pass
        return False
         
    def unlike(self, user_id):
        try:
            _obj = RBEntityLikeModel.objects.get(
                entity_id = self.entity_id,
                user_id = user_id
            )
            _obj.delete()
            return True
        except:
            pass
        return False
         
    def like_already(self, user_id):
        return RBEntityLikeModel.objects.filter(user_id = user_id, entity_id = self.entity_id).count() > 0 

    @staticmethod
    def like_list_of_user(user_id):
        _user_id = int(user_id)
        return map(lambda x : x.entity_id, RBEntityLikeModel.objects.filter(user_id = _user_id))
        
    def add_note(self, creator_id, score, note_text, image_data):
        _creator_id = int(creator_id)
        _score = int(score)
        _note = RBNote.create(
            creator_id = _creator_id,
            note_text = note_text,
            image_data = image_data
        )
        _entity_note_obj = RBEntityNoteModel.objects.create(
            entity_id = self.entity_id,
            note_id = _note.note_id,
            score = _score,
            creator_id = _creator_id
        )
        return _note

    
    def update_note(self, note_id, score, note_text, image_data = None):
        _note_id = int(note_id)
        _score = int(score)
        _note = RBNote(_note_id)
        _note.update(
            note_text = note_text,
            image_data = image_data
        )
        _entity_note_obj = RBEntityNoteModel.objects.get(
            entity_id = self.entity_id,
            note_id = _note_id
        )
        _entity_note_obj.score = _score
        _entity_note_obj.save()
        return _note
        
    
    def add_note_comment(self, note_id, comment_text, creator_id, reply_to = None):
        _note = self.Note(note_id)
        _comment_id = _note.add_comment(
            comment_text = comment_text,
            creator_id = creator_id,
            reply_to = reply_to
        )
        return _note.read_comment(_comment_id)
    
    def read_note_comment(self, note_id, comment_id):
        _note = self.Note(note_id)
        return _note.read_comment(comment_id)
    
    def get_entity_note_of_user(self, user_id):
        _user_id = int(user_id)
        try:
            _obj = RBEntityNoteModel.objects.get(entity_id = self.entity_id, creator_id = _user_id)
            return _obj.note_id
        except RBEntityNoteModel.DoesNotExist, e:
            pass
        return None
    
    @staticmethod
    def get_user_note_count(user_id):
        _user_id = int(user_id)
        return RBEntityNoteModel.objects.filter(creator_id = _user_id).count()
    
    @staticmethod
    def get_user_like_count(user_id):
        _user_id = int(user_id)
        return RBEntityLikeModel.objects.filter(user_id = _user_id).count()
    
    @staticmethod
    def get_user_last_note(user_id):
        _user_id = int(user_id)
        try:
            _note = RBEntityNoteModel.objects.filter(creator_id = _user_id).order_by('-created_time')[0]
            return {
                'note_id' : _note.id,
                'entity_id' : _note.entity_id
            }
        except:
            pass
        return None
    
    @staticmethod
    def get_user_last_like(user_id):
        _user_id = int(user_id)
        try:
            _obj = RBEntityLikeModel.objects.filter(user_id = _user_id).order_by('-created_time')[0]
            return _obj.entity_id
        except:
            pass
        return None
    
    @staticmethod
    def search(query):
        _mango_client = MangoApiClient()
        return _mango_client.search_entity(query)
    
    @staticmethod
    def read_entity_note_figure_data_by_store_key(store_key): 
        _datastore = Client(
            domain = settings.MOGILEFS_DOMAIN, 
            trackers = settings.MOGILEFS_TRACKERS 
        )
        return _datastore.get_file_data(store_key)
