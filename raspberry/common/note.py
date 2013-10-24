# coding=utf8
from models import Note as RBNoteModel
from models import Note_Comment as RBNoteCommentModel
from models import Note_Figure as RBNoteFigureModel
from models import Note_Poke as RBNotePokeModel
from django.conf import settings
from hashlib import md5
from mango.client import MangoApiClient
from pymogile import Client
import datetime



class RBNote(object):
    
    class Figure(object):
        
        def __init__(self, key):
            self.__key = key 
            self.__origin_store_key = 'note/origin/' + self.__key
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
            return settings.IMAGE_SERVER + self.__origin_store_key
    
        def write(self, origin_data): 
            _fp = self.__datastore.new_file(self.__origin_store_key)
            _fp.write(origin_data)
            _fp.close()


    def __init__(self, note_id):
        self.note_id = note_id

    def __ensure_note_obj(self):
        if not hasattr(self, 'note_obj'):
            self.note_obj = RBNoteModel.objects.get(pk = self.note_id)
    
    def __ensure_figure_obj(self):
        if not hasattr(self, 'figure_obj'):
            self.figure_obj = None
            for _figure_obj in RBNoteFigureModel.objects.filter(note_id = self.note_id).order_by('-created_time'):
                self.figure_obj = _figure_obj
                break

#    @classmethod
#    def find(cls, timestamp = None, creator_set = None, offset = 0, count = 30):
#        _hdl = RBEntityNoteModel.objects
#        if timestamp != None:
#            _hdl = _hdl.filter(created_time__lt = timestamp)
#        if creator_set != None:
#            _hdl = _hdl.filter(creator_id__in = creator_set)
#        _list = []
#        for _note_obj in _hdl.order_by('-created_time')[offset : offset + count]:
#            _list.append({
#                'entity_id' : _note_obj.entity_id,
#                'note_id' : _note_obj.id
#            })
#        return _list

    def get_creator_id(self):
        self.__ensure_note_obj()
        return self.note_obj.creator_id
    
    @classmethod
    def create(cls, creator_id, note_text, image_data = None):
        _note_obj = RBNoteModel.objects.create(
            creator_id = creator_id,
            note_text = note_text
        )

        _inst = cls(_note_obj.id)
        _inst.note_obj = _note_obj
    
        if image_data != None:
            _figure = self.Figure.create(image_data)
            _figure_obj = RBNoteFigureModel.objects.create(
                note_id = _note_obj.id,
                creator_id = creator_id,
                store_hash = _figure.get_hash_key()
            )
            _inst.figure_obj = _figure_obj
        return _inst
    
    def update(self, note_text, image_data):
        self.__ensure_note_obj()
        self.note_obj.note_text = note_text
        self.note_obj.save()
        
        if image_data != None:
            self.__ensure_figure_obj()
            _figure = self.Figure.create(image_data)
            if self.figure_obj == None:
                _figure_obj = RBNoteFigureModel.objects.create(
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
        _context["creator_id"] = self.note_obj.creator_id
        _context["content"] = self.note_obj.note_text
        _context["poker_id_list"] = map(lambda x : x.user_id, RBNotePokeModel.objects.filter(note_id = self.note_id))
        _context["poke_count"] = len(_context["poker_id_list"]) 
        _context["comment_id_list"] = map(lambda x : x.id, RBNoteCommentModel.objects.filter(note_id = self.note_id))
        _context["comment_count"] = len(_context["comment_id_list"]) 
        _context["created_time"] = self.note_obj.created_time
        _context["updated_time"] = self.note_obj.updated_time
        
        self.__ensure_figure_obj()
        if self.figure_obj != None:
            _context['figure'] = self.Figure(self.figure_obj.store_hash).read_origin_link()
        
        return _context
        
    def read(self):
        _context = self.__load_note_context()
        return _context

    def poke(self, user_id):
        try:
            RBNotePokeModel.objects.create(
                note_id = self.note_id,
                user_id = user_id
            )
            return True
        except: 
            pass
        return False

    def depoke(self, user_id):
        try:
            _obj = RBNotePokeModel.objects.get(
                note_id = self.note_id,
                user_id = user_id
            )
            _obj.delete()
            return True
        except: 
            pass
        return False

    def poke_already(self, user_id):
        if RBNotePokeModel.objects.filter(note_id = self.note_id, user_id = user_id).count() > 0:
            return True
        return False

    def read_comment(self, comment_id):
        _obj = RBNoteCommentModel.objects.get(pk = comment_id)
        _context = {}
        _context["comment_id"] = _obj.id
        _context["content"] = _obj.comment_text 
        _context["creator_id"] = _obj.creator_id
        _context["reply_to"] = _obj.reply_to
        _context["created_time"] = _obj.created_time
        return _context
    
    def add_comment(self, comment_text, creator_id, reply_to = None):
        _obj = RBNoteCommentModel.objects.create(
            note_id = self.note_id,
            comment_text = comment_text, 
            creator_id = creator_id,
            reply_to = reply_to
        )
        return _obj.id


