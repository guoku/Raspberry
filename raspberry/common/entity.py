# coding=utf8
from models import Entity as RBEntityModel
from models import Entity_Like as RBEntityLikeModel
from models import Entity_Note as RBEntityNoteModel
from models import Entity_Note_Comment as RBEntityNoteCommentModel
from models import Entity_Note_Figure as RBEntityNoteFigureModel
from models import Entity_Note_Poke as RBEntityNotePokeModel
from django.conf import settings
from django.db.models import Sum
from hashlib import md5
import datetime
import urllib
from mango.client import MangoApiClient
from pymogile import Client



class RBEntity(object):
   
    class Figure(object):
        
        def __init__(self, key):
            self.__key = key 
            self.__origin_store_key = self.__key + "_origin"
            self.__datastore = Client(
                domain = settings.MOGILEFS_DOMAIN, 
                trackers = settings.MOGILEFS_TRACKERS 
            )
        
        def get_hash_key(self):
            return self.__key
   
        
        @classmethod
        def create(cls, origin_data):
            _key = md5(origin_data).hexdigest()
            _inst = cls(_key)
    
            if len(_inst.__datastore.get_paths(_inst.__origin_store_key)) == 0:
                _inst.write(origin_data)
    
            return _inst
    
        def read_origin_link(self):
            return settings.IMAGE_SERVER + 'image/entity/figure/' + self.__key + '_origin'
    
        def write(self, origin_data): 
            _fp = self.__datastore.new_file(self.__origin_store_key)
            _fp.write(origin_data)
            _fp.close()


    class Note(object):
    
        def __init__(self, note_id):
            self.note_id = note_id
    
        def __ensure_note_obj(self):
            if not hasattr(self, 'note_obj'):
                print "loading note object..."
                self.note_obj = RBEntityNoteModel.objects.get(pk = self.note_id)
        
        def __ensure_figure_obj(self):
            if not hasattr(self, 'figure_obj'):
                self.figure_obj = None
                for _figure_obj in RBEntityNoteFigureModel.objects.filter(note_id = self.note_id).order_by('-created_time'):
                    self.figure_obj = _figure_obj
                    break
    
        @classmethod
        def find(cls, timestamp = None, creator_set = None, offset = 0, count = 30):
            _hdl = RBEntityNoteModel.objects
            if timestamp != None:
                _hdl = _hdl.filter(created_time__lt = timestamp)
            if creator_set != None:
                _hdl = _hdl.filter(creator_id__in = creator_set)
            _list = []
            for _note_obj in _hdl.order_by('-created_time')[offset : offset + count]:
                _list.append({
                    'entity_id' : _note_obj.entity_id,
                    'note_id' : _note_obj.id
                })
            return _list
    
        def get_creator_id(self):
            self.__ensure_note_obj()
            return self.note_obj.creator_id
        
        @classmethod
        def create(cls, entity_id, creator_id, score, note_text, image_data = None):
            _note_obj = RBEntityNoteModel.objects.create(
                entity_id = entity_id,
                creator_id = creator_id,
                score = score,
                note_text = note_text
            )

            _inst = cls(_note_obj.id)
            _inst.note_obj = _note_obj
        
            if image_data != None:
                _figure = RBEntity.Figure.create(image_data)
                _figure_obj = RBEntityNoteFigureModel.objects.create(
                    entity_id = entity_id,
                    note_id = _note_obj.id,
                    creator_id = creator_id,
                    store_hash = _figure.get_hash_key()
                )
                _inst.figure_obj = _figure_obj
            return _inst
        
        def update(self, score, note_text, image_data):
            _score = int(score)
            self.__ensure_note_obj()
            self.note_obj.note_text = note_text
            self.note_obj.score = _score
            self.note_obj.save()
            
            if image_data != None:
                self.__ensure_figure_obj()
                _figure = RBEntity.Figure.create(image_data)
                if self.figure_obj == None:
                    _figure_obj = RBEntityNoteFigureModel.objects.create(
                        entity_id = self.note_obj.entity_id,
                        note_id = self.note_id,
                        creator_id = self.note_obj.creator_id,
                        store_hash = _figure.get_hash_key()
                    )
                    self.figure_obj = _figure_obj
                else:
                    self.figure_obj.store_hash = _figure.get_hash_key()
                    self.figure_obj.save()
        
        def __load_note_context(self):
            self.__ensure_note_obj()
            _context = {} 
            _context["note_id"] = self.note_obj.id
            _context["entity_id"] = self.note_obj.entity_id
            _context["creator_id"] = self.note_obj.creator_id
            _context["score"] = self.note_obj.score
            _context["content"] = self.note_obj.note_text
            _context["poker_id_list"] = map(lambda x : x.user_id, RBEntityNotePokeModel.objects.filter(note_id = self.note_id))
            _context["poke_count"] = len(_context["poker_id_list"]) 
            _context["comment_id_list"] = map(lambda x : x.id, RBEntityNoteCommentModel.objects.filter(note_id = self.note_id))
            _context["comment_count"] = len(_context["comment_id_list"]) 
            _context["created_time"] = self.note_obj.created_time
            _context["updated_time"] = self.note_obj.updated_time
            
            self.__ensure_figure_obj()
            if self.figure_obj != None:
                _context['figure'] = RBEntity.Figure(self.figure_obj.store_hash).read_origin_link()
            
            return _context
            
        def read(self):
            _context = self.__load_note_context()
            return _context

        def poke(self, user_id):
            try:
                RBEntityNotePokeModel.objects.create(
                    note_id = self.note_id,
                    user_id = user_id
                )
                return True
            except: 
                pass
            return False

        def depoke(self, user_id):
            try:
                _obj = RBEntityNotePokeModel.objects.get(
                    note_id = self.note_id,
                    user_id = user_id
                )
                _obj.delete()
                return True
            except: 
                pass
            return False

        def poke_already(self, user_id):
            return RBEntityNotePokeModel.objects.filter(user_id = user_id).count() > 0

        def read_comment(self, comment_id):
            _obj = RBEntityNoteCommentModel.objects.get(pk = comment_id)
            _context = {}
            _context["comment_id"] = _obj.id
            _context["content"] = _obj.comment_text 
            _context["creator_id"] = _obj.creator_id
            _context["reply_to"] = _obj.reply_to
            _context["created_time"] = _obj.created_time
            return _context
        
        def add_comment(self, comment_text, creator_id, reply_to = None):
            _obj = RBEntityNoteCommentModel.objects.create(
                note_id = self.note_id,
                comment_text = comment_text, 
                creator_id = creator_id,
                reply_to = reply_to
            )
            return _obj.id

    
    def __init__(self, entity_id):
        self.__entity_id = entity_id
        self.notes = {} 
    
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
        _context["created_time"] = self.__entity_obj.created_time
        _context["updated_time"] = self.__entity_obj.updated_time
        

        _context["total_score"] = 0 
        _context["score_count"] = 0 
        _context["note_id_list"] = []
        for _note_obj in RBEntityNoteModel.objects.filter(entity_id = self.__entity_id):
            _context["note_id_list"].append(_note_obj.id)
            _context["total_score"] += _note_obj.score
            _context["score_count"] += 1

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
        return RBEntityLikeModel.objects.filter(user_id = user_id, entity_id = self.__entity_id).count() > 0 

    @staticmethod
    def like_list_of_user(user_id):
        _user_id = int(user_id)
        return map(lambda x : x.entity_id, RBEntityLikeModel.objects.filter(user_id = _user_id))
        
    def get_user_note(self, user_id):
        try:
            _obj = RBEntityNoteModel.objects.get(creator_id = user_id, entity_id = self.__entity_id)
            return _obj.id
        except RBEntityNoteModel.DoesNotExist, e:
            pass
        return None 

    def add_note(self, creator_id, score, note_text, image_data):
        _creator_id = int(creator_id)
        _note = self.Note.create(
            entity_id = self.__entity_id,
            creator_id = _creator_id,
            score = score,
            note_text = note_text,
            image_data = image_data
        )
        self.notes[_note.note_id] = _note
        return _note.note_id

    
    def update_note(self, note_id, score, note_text, image_data = None):
        _note_id = int(note_id)
        _note = self.Note(_note_id)
        _note.update(
            score = score,
            note_text = note_text,
            image_data = image_data
        )
        self.notes[_note.note_id] = _note
        
    
    def read_note(self, note_id):
        _note_id = int(note_id)
        if not self.notes.has_key(_note_id):
            self.notes[_note_id] = self.Note(_note_id) 
        _context = self.notes[_note_id].read()
        return _context
     
    def poke_note(self, note_id, user_id):
        return self.Note(note_id).poke(user_id)
    
    def depoke_note(self, note_id, user_id):
        return self.Note(note_id).depoke(user_id)
    
    def poke_note_already(self, note_id, user_id):
        return self.Note(note_id).poke_already(user_id)
    
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
