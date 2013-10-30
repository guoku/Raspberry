# coding=utf8
from models import Candidate as RBCandidateModel
from models import Candidate_Note as RBCandidateNoteModel
from django.conf import settings
from django.db.models import Sum
from mango.client import MangoApiClient
from note import RBNote
from hashlib import md5
import datetime
import urllib
import time



class RBCandidate(object):

    def __init__(self, candidate_id):
        self.candidate_id = candidate_id 
    
    def get_candidate_id(self):
        return self.candidate_id
    
    @classmethod
    def create(cls, creator_id, category_id, category_text, brand, title, 
               score, note_text, image_data):
        _category_id = int(category_id)
        _creator_id = int(creator_id)
        _score = int(score)
       
        _candidate_obj = RBCandidateModel.objects.create(
            brand = brand,
            title = title,
            category_id = _category_id,
            category_text = category_text,
            creator_id = _creator_id
        )
        _note = RBNote.create(
            creator_id = _creator_id,
            note_text = note_text,
            image_data = image_data
        )
        _candidate_note_obj = RBCandidateNoteModel.objects.create(
            candidate_id = _candidate_obj.id,
            note_id = _note.note_id,
            score = _score,
            creator_id = _creator_id
        )
         
        _inst = cls(_candidate_obj.id)
        _inst.candidate_obj = _candidate_obj
        return _inst

    
    
    def __ensure_candidate_obj(self):
        if not hasattr(self, 'candidate_obj'):
            self.candidate_obj = RBCandidateModel.objects.get(pk = self.candidate_id)
    
    def __ensure_candidate_note_obj(self):
        if not hasattr(self, 'candidate_note_obj'):
            self.candidate_note_obj = RBCandidateNoteModel.objects.get(candidate_id = self.candidate_id)

    def __load_candidate_context(self):
        self.__ensure_candidate_obj()
        _context = {}
        _context["candidate_id"] = self.candidate_obj.id
        _context["category_id"] = self.candidate_obj.category_id
        _context["creator_id"] = self.candidate_obj.creator_id
        _context["category_text"] = self.candidate_obj.category_text
        _context["brand"] = self.candidate_obj.brand
        _context["title"] = self.candidate_obj.title
        _context["entity_id"] = self.candidate_obj.entity_id
        _context["created_time"] = self.candidate_obj.created_time
        _context["updated_time"] = self.candidate_obj.updated_time
        

        self.__ensure_candidate_note_obj()
        _context["note_id"] = self.candidate_note_obj.note_id
        _context["score"] = self.candidate_note_obj.score

        return _context
        
    def get_note(self):
        self.__ensure_candidate_note_obj()
        return self.candidate_note_obj.note_id
    

    def read(self, json = False):
        _context = self.__load_candidate_context()
        if json:
            _context['created_time'] = time.mktime(_context["created_time"].timetuple())
            _context['updated_time'] = time.mktime(_context["updated_time"].timetuple())
        return _context    
    
    
    def update(self, category_id = None, category_text = None, brand = None, title = None, 
               score = None, note_text = None, entity_id = None, image_data = None):
                
        if category_id != None or category_text != None or brand != None or title != None or entity_id != None:
            self.__ensure_candidate_obj()
            if category_id != None: 
                self.candidate_obj.category_id = int(category_id)
            if category_text != None: 
                self.candidate_obj.category_text = category_text
            if brand != None: 
                self.candidate_obj.brand = brand 
            if title != None: 
                self.candidate_obj.title = title 
            if entity_id != None:
                self.candidate_obj.entity_id = entity_id 
            self.candidate_obj.save()
       
        if score != None: 
            self.__ensure_candidate_note_obj()
            self.candidate_note_obj.score = int(score)
            self.candidate_note_obj.save()

        if note_text != None or image_data != None:
            self.__ensure_candidate_note_obj()
            _note = RBNote(self.candidate_note_obj.note_id)
            _note.update(
                note_text = note_text,
                image_data = image_data
            )
    
    def delete(self):
        self.__ensure_candidate_obj()
        self.candidate_obj.delete()
        
   
    @classmethod
    def find(cls, creator_id = None, category_id = None, timestamp = None, offset = 0, count = 30, pending_only = False, approve_already = False):
        _hdl = RBCandidateModel.objects
        if category_id != None:
            _hdl = _hdl.filter(category_id = category_id)
        if creator_id != None:
            _hdl = _hdl.filter(creator_id = creator_id)
        if timestamp != None:
            _hdl = _hdl.filter(created_time__lt = timestamp)
        if pending_only == True:
            _hdl = _hdl.filter(entity_id = '')
        if approve_already == True:
            _hdl = _hdl.exclude(entity_id = '')
            
        _hdl = _hdl.order_by('-created_time')[offset : offset + count]
        _candidate_id_list = map(lambda x: x.id, _hdl)
        return _candidate_id_list
        
    @classmethod
    def count(cls, category_id = None, creator_id = None):
        _hdl = RBCandidateModel.objects
        if category_id != None:
            _hdl = _hdl.filter(category_id = category_id)
        if creator_id != None:
            _hdl = _hdl.filter(creator_id = creator_id)
            
        return _hdl.count()
    
