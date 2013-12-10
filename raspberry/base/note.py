# coding=utf8
from models import Note as NoteModel
from models import Note_Comment as NoteCommentModel
from models import Note_Poke as NotePokeModel
from message import NotePokeMessage, NoteCommentReplyMessage, NoteCommentMessage
from django.conf import settings
from django.core.cache import cache
import datetime
import time
from image import Image
from tag import Tag 
from user import User 



class Note(object):
    
    class CommentDoesNotExist(Exception):
        def __init__(self, comment_id):
            self.__message = "comment %s does not exist"%comment_id
        def __str__(self):
            return repr(self.__message)
    
    def __init__(self, note_id):
        self.note_id = int(note_id)
        self.comments = {} 

    def __ensure_note_obj(self):
        if not hasattr(self, 'note_obj'):
            self.note_obj = NoteModel.objects.get(pk = self.note_id)
    
    @classmethod
    def count(cls, timestamp = None, entity_id = None, category_id = None, creator_set = None, selection = 0, status = 0):
        _hdl = NoteModel.objects.all()
        if entity_id != None:
            _hdl = _hdl.filter(entity_id = entity_id)
        if category_id != None:
            _hdl = _hdl.filter(entity__neo_category_id = category_id)
        if timestamp != None:
            _hdl = _hdl.filter(created_time__lt = timestamp)
        if creator_set != None:
            _hdl = _hdl.filter(creator_id__in = creator_set)
        if selection > 0:
            _hdl = _hdl.filter(selector_id__isnull = False)
        elif selection < 0:
            _hdl = _hdl.filter(selector_id__isnull = True)
        if status < 0:
            _hdl = _hdl.filter(weight__lt = 0)
        elif status > 0:
            _hdl = _hdl.filter(weight__gte = 0)
        return _hdl.count() 
    
    @classmethod
    def find(cls, timestamp = None, entity_id = None, category_id = None, creator_set = None, offset = None, count = None, sort_by = None, selection = 0, status = 0):
        _hdl = NoteModel.objects.all()
        if entity_id != None:
            _hdl = _hdl.filter(entity_id = entity_id)
        if category_id != None:
            _hdl = _hdl.filter(entity__neo_category_id = category_id)
        if timestamp != None:
            _hdl = _hdl.filter(created_time__lt = timestamp)
        if creator_set != None:
            _hdl = _hdl.filter(creator_id__in = creator_set)
        if selection > 0:
            _hdl = _hdl.filter(selector_id__isnull = False)
        elif selection < 0:
            _hdl = _hdl.filter(selector_id__isnull = True)
        if status < 0:
            _hdl = _hdl.filter(weight__lt = 0)
        elif status > 0:
            _hdl = _hdl.filter(weight__gte = 0)
            
        
        if sort_by == 'poke':
            _hdl = _hdl.order_by('-poke_count')
        elif sort_by == 'selection_post_time':
            _hdl = _hdl.order_by('-post_time')
        else:
            _hdl = _hdl.order_by('-created_time')
            


        if offset != None and count != None:
            _hdl = _hdl[offset : offset + count]
        
        _list = map(lambda x: x.id, _hdl)
        return _list
    
    @classmethod
    def search(cls, query_string, offset = 0, count = 30):
        _query_set = NoteModel.search.query(query_string)
        _note_id_list = []
        for _result in _query_set[offset : offset + count]:
            _note_id_list.append(int(_result._sphinx["id"]))
        return _note_id_list
    
    def get_creator_id(self):
        self.__ensure_note_obj()
        return self.note_obj.creator_id
    
    @classmethod
    def create(cls, entity_id, creator_id, note_text, score = 0, image_data = None):
        _note_text = note_text.replace(u"＃", "#")
        if image_data != None:
            _image_obj = Image.create(
                source = 'note_uploaded', 
                image_data = image_data
            )
            _figure = _image_obj.image_id
        else:
            _figure = ''
        
        _note_obj = NoteModel.objects.create(
            entity_id = entity_id,
            creator_id = creator_id,
            note = _note_text,
            score = int(score),
            figure = _figure
        )

        _inst = cls(_note_obj.id)
        _inst.note_obj = _note_obj
        
        _tags = Tag.Parser.parse(_note_text)
        for _tag in _tags:
            Tag.add_entity_tag(
                entity_id = _note_obj.entity_id,
                user_id = creator_id,
                tag = _tag
            )
        
        return _inst
    
    
    def update_selection_info(self, selector_id, selected_time, post_time):
        if selector_id != None:
            _selector_id = int(selector_id)
        else:
            _selector_id = None 

        self.__ensure_note_obj()
        self.note_obj.selector_id = _selector_id 
        self.note_obj.selected_time = selected_time 
        self.note_obj.post_time = post_time
        self.note_obj.save()

        
        _context = self.__load_note_context_from_cache()
        if _context != None:
            _context['selector_id'] = _selector_id 
            _context['selected_time'] = selected_time 
            _context['post_time'] = post_time 
            if _selector_id != None:
                _context["is_selected"] = 1
            else:
                _context["is_selected"] = 0 
            self.__reset_note_context_to_cache(_context)


        
    
    def update(self, score = None, note_text = None, image_data = None, weight = None):
        _context = self.__load_note_context_from_cache()
        self.__ensure_note_obj()
        
        if image_data != None:
            _image_obj = Image.create(
                source = 'note_uploaded', 
                image_data = image_data
            )
            if _image_obj.image_id != self.note_obj.figure:
                self.note_obj.figure = _image_obj.image_id
            if _context != None:
                _context['figure'] = Image(_image_obj.image_id).getlink()
        
        if score != None:
            self.note_obj.score = score 
        
        if note_text != None:
            _note_text = note_text.replace(u"＃", "#")
            _old_text = self.note_obj.note
            _new_text = _note_text

            self.note_obj.note = _note_text
            if _context != None:
                _context['content'] = _note_text 
        
            _new_tags = Tag.Parser.parse(_new_text)
            _old_tags = Tag.Parser.parse(_old_text)
            for _tag in _new_tags:
                if not _tag in _old_tags:
                    Tag.add_entity_tag(
                        entity_id = self.note_obj.entity_id,
                        user_id = self.note_obj.creator_id,
                        tag = _tag
                    )
            for _tag in _old_tags:
                if not _tag in _new_tags:
                    Tag.del_entity_tag(
                        entity_id = self.note_obj.entity_id,
                        user_id = self.note_obj.creator_id,
                        tag = _tag
                    )
                    
        
        if weight != None:
            _weight = int(weight)
            self.note_obj.weight = _weight 
            if _context != None:
                _context['weight'] = _weight  
        self.note_obj.save()
       
        if _context != None:
            self.__reset_note_context_to_cache(_context)
            
        
    def delete(self):
        self.__ensure_note_obj()
        self.note_obj.delete() 
    
    def __load_note_context_from_cache(self):
        _cache_key = 'note_%s_context'%self.note_id
        _context = cache.get(_cache_key)
        return _context
    
    def __reset_note_context_to_cache(self, context = None):
        _cache_key = 'note_%s_context'%self.note_id
        if context == None:
            self.__ensure_note_obj()
            _context = {} 
            _context["note_id"] = self.note_obj.id
            _context["entity_id"] = self.note_obj.entity_id
            _context["creator_id"] = self.note_obj.creator_id
            _context["content"] = self.note_obj.note
            _context["score"] = self.note_obj.score
            if self.note_obj.selector_id != None:
                _context["is_selected"] = 1
            else:
                _context["is_selected"] = 0 
            _context["poker_id_list"] = map(lambda x : x.user_id, NotePokeModel.objects.filter(note_id = self.note_id))
            _context["poke_count"] = len(_context["poker_id_list"]) 
            _context["comment_id_list"] = map(lambda x : x.id, NoteCommentModel.objects.filter(note_id = self.note_id).order_by('created_time'))
            _context["comment_count"] = len(_context["comment_id_list"]) 
            _context["created_time"] = self.note_obj.created_time
            _context["updated_time"] = self.note_obj.updated_time
            _context["weight"] = self.note_obj.weight
            if len(self.note_obj.figure) > 0:
                _context['figure'] = Image(self.note_obj.figure).getlink()
            else:
                _context['figure'] = None
            
            _context["selector_id"] = self.note_obj.selector_id
            _context["selected_time"] = self.note_obj.selected_time
            _context["post_time"] = self.note_obj.post_time
        else:
            _context = context
        cache.set(_cache_key, _context, 864000)
        
        
        ## CLEAN_OLD_CACHE ## 
        cache.delete("note_context_%s"%self.note_id)

        return _context
    
    def __read_note_context(self):
        _context = self.__load_note_context_from_cache()
        if _context == None:
            _context = self.__reset_note_context_to_cache()
        return _context

    def get_entity_id(self):
        self.__ensure_note_obj()
        return self.note_obj.entity_id 
        
    def read(self, json = False):
        _context = self.__read_note_context()
        if json:
            _context['created_time'] = time.mktime(_context["created_time"].timetuple())
            _context['updated_time'] = time.mktime(_context["updated_time"].timetuple())
            if _context['selected_time'] != None:
                _context['selected_time'] = time.mktime(_context["selected_time"].timetuple())
            if _context['post_time'] != None:
                _context['post_time'] = time.mktime(_context["post_time"].timetuple())
        return _context

    def poke(self, user_id):
        try:
            _user_id = int(user_id)
            NotePokeModel.objects.create(
                note_id = self.note_id,
                user_id = user_id
            )
            
            _context = self.__load_note_context_from_cache()
            if _context != None:
                if _user_id not in _context['poker_id_list']:
                    _context['poker_id_list'].append(_user_id)
                    _context['poke_count'] = len(_context['poker_id_list'])
                    _context = self.__reset_note_context_to_cache(_context)
            User(user_id).update_user_entity_note_poke_count(delta = 1)
           
            self.__ensure_note_obj()
            if self.note_obj.creator_id != user_id:
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
            _user_id = int(user_id)
            _obj = NotePokeModel.objects.get(
                note_id = self.note_id,
                user_id = user_id
            )
            _obj.delete()
            User(user_id).update_user_entity_note_poke_count(delta = -1)
            
            _context = self.__load_note_context_from_cache()
            if _context != None:
                if _user_id in _context['poker_id_list']:
                    _context['poker_id_list'].remove(_user_id)
                    _context['poke_count'] = len(_context['poker_id_list'])
                    _context = self.__reset_note_context_to_cache(_context)
            
            return True
        except: 
            pass
        return False

    def poke_already(self, user_id):
        if NotePokeModel.objects.filter(note_id = self.note_id, user_id = user_id).count() > 0:
            return True
        return False

    def read_comment(self, comment_id, json = False):
        _cache_key = 'note_comment_%s_context'%comment_id
        _context = cache.get(_cache_key)
        if _context == None: 
            if not self.comments.has_key(comment_id):
                self.comments[comment_id] = NoteCommentModel.objects.get(pk = comment_id)
            _context = {}
            _context["comment_id"] = self.comments[comment_id].id
            _context["entity_id"] = self.get_entity_id()
            _context["note_id"] = self.comments[comment_id].note_id
            _context["content"] = self.comments[comment_id].comment
            _context["creator_id"] = self.comments[comment_id].creator_id
           
            _context['reply_to_comment_id'] = self.comments[comment_id].replied_comment_id
            _context['reply_to_user_id'] = self.comments[comment_id].replied_user_id
            
            _context["created_time"] = self.comments[comment_id].created_time
            cache.set(_cache_key, _context, 864000)
        
        if json:
            _context['created_time'] = time.mktime(_context["created_time"].timetuple())
        
        return _context
    
    def add_comment(self, comment_text, creator_id, reply_to_comment_id = None, reply_to_user_id = None):
        _comment_text = comment_text.replace(u"＃", "#")
        _obj = NoteCommentModel.objects.create(
            note_id = self.note_id,
            comment = _comment_text, 
            creator_id = creator_id,
            replied_comment_id = reply_to_comment_id,
            replied_user_id = reply_to_user_id
        )
        self.comments[_obj.id] = _obj
        
        _context = self.__load_note_context_from_cache()
        if _context != None:
            _context['comment_id_list'].append(_obj.id)
            _context['comment_count'] = len(_context['comment_id_list'])
            _context = self.__reset_note_context_to_cache(_context)

        self.__ensure_note_obj()
        _tags = Tag.Parser.parse(_comment_text)
        for _tag in _tags:
            Tag.add_entity_tag(
                entity_id = self.note_obj.entity_id,
                user_id = creator_id,
                tag = _tag
            )
            
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
                replying_comment_id = _obj.id, 
                replying_user_id = creator_id, 
                created_time = datetime.datetime.now()
            )
            _message.save()
        
        return _obj.id
    
    def del_comment(self, comment_id):
        _comment_id = int(comment_id)
        if not self.comments.has_key(_comment_id):
            try:
                self.comments[_comment_id] = NoteCommentModel.objects.get(pk = _comment_id)
            except NoteCommentModel.DoesNotExist, e:
                raise Note.CommentDoesNotExist(_comment_id)
        
        _comment_text = self.comments[_comment_id].comment
        _creator_id = self.comments[_comment_id].creator_id
        self.comments[_comment_id].delete()
       

        _context = self.__load_note_context_from_cache()
        if _context != None:
            if _comment_id in _context['comment_id_list']:
                _context['comment_id_list'].remove(_comment_id)
                _context['comment_count'] = len(_context['comment_id_list'])
                self.__reset_note_context_to_cache(_context)
        
        self.__ensure_note_obj()
        _tags = Tag.Parser.parse(_comment_text)
        for _tag in _tags:
            Tag.del_entity_tag(
                entity_id = self.note_obj.entity_id,
                user_id = _creator_id,
                tag = _tag
            )
            
            
         
    
    @staticmethod
    def get_user_last_note(user_id):
        _user_id = int(user_id)
        try:
            _note = NoteModel.objects.filter(creator_id = _user_id).order_by('-created_time')[0]
            return _note.id
        except:
            pass
        return None


