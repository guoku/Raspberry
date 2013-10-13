# coding=utf8
from models import Entity as RBEntityModel
from models import Entity_Like as RBEntityLikeModel
from models import Entity_Note as RBEntityNoteModel
from models import Entity_Note_Poke as RBEntityNotePokeModel
from hashlib import md5
import datetime
import urllib
from utils.lib import cal_guoku_hash 
from mango.client import MangoApiClient



class RBEntity(object):
    
    class Note(object):
    
        def __init__(self, note_id):
            self.__note_id = note_id
    
        def __ensure_note_obj(self):
            if not hasattr(self, '__note_obj'):
                self.__note_obj = RBEntityNoteModel.objects.get(pk = self.__note_id)
    
        @classmethod
        def create(cls, entity_id, creator_id, note_text):
            _note_obj = RBEntityNoteModel.objects.create(
                entity_id = entity_id,
                creator_id = creator_id,
                note_text = note_text
            )
            _inst = cls(_note_obj.id)
            _inst.__note_obj = _note_obj
            return _inst
        
        def __load_note_context(self):
            self.__ensure_note_obj()
            _context = {} 
            _context["note_id"] = self.__note_obj.id
            _context["creator_id"] = self.__note_obj.creator_id
            _context["note_text"] = self.__note_obj.note_text
            _context["poker_id_list"] = map(lambda x : x.user_id, RBEntityNotePokeModel.objects.filter(note_id = self.__note_id))
            _context["created_time"] = self.__note_obj.created_time
            _context["updated_time"] = self.__note_obj.updated_time
            return _context
            
        def read(self):
            _context = self.__load_note_context()
            return _context

        def poke(self, user_id):
            try:
                RBEntityNotePokeModel.objects.create(
                    note_id = self.__note_id,
                    user_id = user_id
                )
                return True
            except: 
                pass
            return False

        def depoke(self, user_id):
            try:
                _obj = RBEntityNotePokeModel.objects.get(
                    note_id = self.__note_id,
                    user_id = user_id
                )
                _obj.delete()
                return True
            except: 
                pass
            return False

        def poke_already(self, user_id):
            return RBEntityNotePokeModel.objects.filter(user_id = user_id).count() > 0


    
    def __init__(self, entity_id):
        self.__entity_id = entity_id
    
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
        return self.__entity_id
    
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
        _item_id = _mango_client.add_taobao_item_for_entity(self.__entity_id, taobao_item_info, image_urls)
    
    
    def __ensure_entity_obj(self):
        if not hasattr(self, '__entity_obj'):
            self.__entity_obj = RBEntityModel.objects.get(entity_id = self.__entity_id)

    def __load_entity_context(self, meta_context):
        self.__ensure_entity_obj()
        _context = meta_context 
        _context["entity_hash"] = self.__entity_obj.entity_hash
        _context["category_id"] = self.__entity_obj.category_id
        _context["note_id_list"] = map(lambda x : x.id, RBEntityNoteModel.objects.filter(entity_id = self.__entity_id))
        _context["created_time"] = self.__entity_obj.created_time
        _context["updated_time"] = self.__entity_obj.updated_time
        return _context
        

    def read(self):
        _mango_client = MangoApiClient()
        _meta_context = _mango_client.read_entity(self.__entity_id)
        _context = self.__load_entity_context(_meta_context)
        return _context    
    
    
    def update(self, category_id = None, brand = None, title = None, intro = None, price = None):
        if brand != None or title != None or intro != None:
            _mango_client = MangoApiClient()
            _base_info = _mango_client.read_entity(self.__entity_id)
            
            if brand != None or title != None or intro != None or price != None:
                _mango_client.update_entity(
                    entity_id = self.__entity_id, 
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
    def find(cls, category_id = None, offset = 0, count = 30):
        _hdl = RBEntityModel.objects
        if category_id != None:
            _hdl = _hdl.filter(category_id = category_id)
        _hdl = _hdl.order_by('-created_time')[offset : offset + count]
        _entity_id_list = map(lambda x: x.entity_id, _hdl)
        return _entity_id_list
        
    @classmethod
    def count(cls, category_id = None):
        _hdl = RBEntityModel.objects.filter(category_id = category_id)
        return _hdl.count()
    
    def bind_item(self, item_id):
        _mango_client = MangoApiClient()
        _mango_client.bind_entity_item(self.__entity_id, item_id)
    
    def unbind_item(self, item_id):
        _mango_client = MangoApiClient()
        _mango_client.unbind_entity_item(self.__entity_id, item_id)

    def like(self, user_id):
        try:
            RBEntityLikeModel.objects.create(
                entity_id = self.__entity_id,
                user_id = user_id
            )
            return True
        except:
            pass
        return False
         
    def unlike(self, user_id):
        try:
            _obj = RBEntityLikeModel.objects.get(
                entity_id = self.__entity_id,
                user_id = user_id
            )
            _obj.delete()
            return True
        except:
            pass
        return False
         
    def like_already(self, user_id):
        return RBEntityLikeModel.objects.filter(user_id = user_id).count() > 0 

    @staticmethod
    def like_list_of_user(user_id):
        _user_id = int(user_id)
        return map(lambda x : x.entity_id, RBEntityLikeModel.objects.filter(user_id = _user_id))
        
    def add_note(self, creator_id, note_text):
        _note = self.Note.create(
            entity_id = self.__entity_id,
            creator_id = creator_id,
            note_text = note_text
        )
        return _note.read()
    
    def read_note(self, note_id):
        return self.Note(note_id).read()
     
    def poke_note(self, note_id, user_id):
        return self.Note(note_id).poke(user_id)
    
    def depoke_note(self, note_id, user_id):
        return self.Note(note_id).depoke(user_id)
    
    def poke_note_already(self, note_id, user_id):
        return self.Note(note_id).poke_already(user_id)
    
    @staticmethod
    def note_list_of_user(user_id):
        _user_id = int(user_id)
        _list = []
        for _note_obj in RBEntityNoteModel.objects.filter(creator_id = _user_id):
            _list.append({
                'entity_id' : _note_obj.entity_id,
                'note_id' : _note_obj.id
            })
        return _list
        
