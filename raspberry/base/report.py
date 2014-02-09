# coding=utf-8
from mongoengine import *
import datetime

class Report(Document):
    reporter_id = IntField(required = True) 
    comment = StringField(required = True)
    created_time = DateTimeField(required = True)
    updated_time = DateTimeField(required = True)
    meta = {
        'db_alias' : 'guoku-db',
        'indexes' : [ 
            'reporter_id' 
        ],
        'allow_inheritance' : True
    }

class EntityReport(Report):
    entity_id = IntField(required = True) 
    meta = {
        'indexes' : [ 
            'entity_id' 
        ],
    }

class EntityNoteReport(Report):
    note_id = IntField(required = True) 
    meta = {
        'indexes' : [ 
            'note_id' 
        ],
    }
