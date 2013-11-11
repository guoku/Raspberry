# coding=utf8
from models import Note as NoteModel
from models import Note_Comment as NoteCommentModel
from models import Note_Poke as NotePokeModel
from message import NotePokeMessage, NoteCommentReplyMessage, NoteCommentMessage
from django.conf import settings
from hashlib import md5
from pymogile import Client
import datetime
import time



class Note(object):
    
    class Figure(object):
        
        def __init__(self, key):
            self.key = key 
            self.origin_store_key = 'note/origin/' + self.key
            self.__datastore = Client(
                domain = settings.MOGILEFS_DOMAIN, 
                trackers = settings.MOGILEFS_TRACKERS 
            )
        
        @classmethod
        def create(cls, origin_data):
            _key = md5(origin_data).hexdigest()
            _inst = cls(_key)
    
            if len(_inst.__datastore.get_paths(_inst.origin_store_key)) == 0:
                _inst.write(origin_data)
    
            return _inst
    
        def read_origin_link(self):
            return settings.IMAGE_SERVER + self.origin_store_key
    
        def write(self, origin_data): 
            _fp = self.__datastore.new_file(self.origin_store_key)
            _fp.write(origin_data)
            _fp.close()


    def __init__(self, note_id):
        self.note_id = note_id
        self.comments = {} 

    def __ensure_note_obj(self):
        if not hasattr(self, 'note_obj'):
            self.note_obj = NoteModel.objects.get(pk = self.note_id)
    
    @classmethod
    def count(cls, timestamp = None, entity_id = None, creator_set = None, offset = 0, count = 30):
        _hdl = NoteModel.objects
        if entity_id != None:
            _hdl = _hdl.filter(entity_id = entity_id)
        if timestamp != None:
            _hdl = _hdl.filter(created_time__lt = timestamp)
        if creator_set != None:
            _hdl = _hdl.filter(creator_id__in = creator_set)
        return _hdl.count() 
    
    @classmethod
    def find(cls, timestamp = None, entity_id = None, category_id = None, creator_set = None, offset = 0, count = 30):
        _hdl = NoteModel.objects
        if entity_id != None:
            _hdl = _hdl.filter(entity_id = entity_id)
        if category_id != None:
            _hdl = _hdl.filter(entity__neo_category_id = category_id)
        if timestamp != None:
            _hdl = _hdl.filter(created_time__lt = timestamp)
        if creator_set != None:
            _hdl = _hdl.filter(creator_id__in = creator_set)
        _list = []
        for _note_obj in _hdl.order_by('-created_time')[offset : offset + count]:
            _list.append(_note_obj.id)
        return _list
    
    
    def get_creator_id(self):
        self.__ensure_note_obj()
        return self.note_obj.creator_id
    
    @classmethod
    def create(cls, entity_id, creator_id, note_text, score = 0, image_data = None):
        if image_data != None:
            _figure_obj = cls.Figure.create(image_data)
            _figure = _figure_obj.key
        else:
            _figure = ''
        _note_obj = NoteModel.objects.create(
            entity_id = entity_id,
            creator_id = creator_id,
            note = note_text,
            score = int(score),
            figure = _figure
        )

        _inst = cls(_note_obj.id)
        _inst.note_obj = _note_obj
        return _inst
    
    
    def update(self, note_text, image_data):
        self.__ensure_note_obj()
        self.note_obj.note_text = note_text
        self.note_obj.save()
        
        if image_data != None:
            self.__ensure_figure_obj()
            _figure = self.Figure.create(image_data)
            if self.figure_obj == None:
                _figure_obj = NoteFigureModel.objects.create(
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
        _context["content"] = self.note_obj.note
        _context["score"] = self.note_obj.score
        _context["poker_id_list"] = map(lambda x : x.user_id, NotePokeModel.objects.filter(note_id = self.note_id))
        _context["poke_count"] = len(_context["poker_id_list"]) 
        _context["comment_id_list"] = map(lambda x : x.id, NoteCommentModel.objects.filter(note_id = self.note_id))
        _context["comment_count"] = len(_context["comment_id_list"]) 
        _context["created_time"] = self.note_obj.created_time
        _context["updated_time"] = self.note_obj.updated_time
        if len(self.note_obj.figure) > 0:
            _context['figure'] = self.Figure(self.note_obj.figure).read_origin_link()

        return _context

#    def get_entity_of_note(self):
#        try:
#            _obj = EntityNoteModel.objects.get(note_id = self.note_id)
#            return _obj.entity_id
#        except EntityNoteModel.DoesNotExist, e:
#            pass
#        return None
        
    def read(self, json = False):
        _context = self.__load_note_context()
        if json:
            _context['created_time'] = time.mktime(_context["created_time"].timetuple())
            _context['updated_time'] = time.mktime(_context["updated_time"].timetuple())
        return _context

    def poke(self, user_id):
        try:
            NotePokeModel.objects.create(
                note_id = self.note_id,
                user_id = user_id
            )
            
            self.__ensure_note_obj()
            _message = NotePokeMessage(
                user_id = self.note_obj.creator_id,
                note_id = self.note_id, 
                poker_id = user_id, 
                created_time = datetime.datetime.now()
            )
            _message.save()
            return True
        except: 
            pass
        return False

    def depoke(self, user_id):
        try:
            _obj = NotePokeModel.objects.get(
                note_id = self.note_id,
                user_id = user_id
            )
            _obj.delete()
            return True
        except: 
            pass
        return False

    def poke_already(self, user_id):
        if NotePokeModel.objects.filter(note_id = self.note_id, user_id = user_id).count() > 0:
            return True
        return False

    def read_comment(self, comment_id, json = False):
        if not self.comments.has_key(comment_id):
            self.comments[comment_id] = NoteCommentModel.objects.get(pk = comment_id)
        _context = {}
        _context["comment_id"] = self.comments[comment_id].id
        _context["content"] = self.comments[comment_id].comment
        _context["creator_id"] = self.comments[comment_id].creator_id
       
        _context['reply_to_comment_id'] = self.comments[comment_id].reply_to_comment_id
        _context['reply_to_user_id'] = self.comments[comment_id].reply_to_user_id
        
        _context["created_time"] = self.comments[comment_id].created_time
        if json:
            _context['created_time'] = time.mktime(_context["created_time"].timetuple())
        return _context
    
    def add_comment(self, comment_text, creator_id, reply_to_comment_id = None, reply_to_user_id = None):
        _obj = NoteCommentModel.objects.create(
            note_id = self.note_id,
            comment = comment_text, 
            creator_id = creator_id,
            reply_to_comment_id = reply_to_comment_id,
            reply_to_user_id = reply_to_user_id
        )
        self.comments[_obj.id] = _obj
            
        self.__ensure_note_obj()
        _message = NoteCommentMessage(
            user_id = self.note_obj.creator_id,
            note_id = self.note_id, 
            comment_id =  _obj.id, 
            comment_creator_id = creator_id, 
            created_time = datetime.datetime.now()
        )
        _message.save()

        if reply_to_user_id != None:
            _message = NoteCommentReplyMessage(
                user_id = reply_to_user_id,
                note_id = self.note_id, 
                comment_id = reply_to_comment_id, 
                replying_user_id = creator_id, 
                created_time = datetime.datetime.now()
            )
            _message.save()
        
        return _obj.id
    
    @staticmethod
    def get_user_last_note(user_id):
        _user_id = int(user_id)
        try:
            _note = NoteModel.objects.filter(creator_id = _user_id).order_by('-created_time')[0]
            return _note.id
        except:
            pass
        return None


