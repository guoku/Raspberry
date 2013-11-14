# coding=utf-8
from mongoengine import *
import datetime

class Selection(Document):
    selector_id = IntField(required = True) 
    selected_time = DateTimeField(required = True)
    post_time = DateTimeField(required = True)
    meta = {
        "indexes" : [ 
            "selector_id", 
            "post_time" 
        ],
        "allow_inheritance" : True
    }

class NoteSelection(Selection):
    entity_id = IntField(required = True) 
    note_id = IntField(required = True) 
    root_category_id = IntField(required = True) 
    neo_category_group_id = IntField(required = True) 
    neo_category_id = IntField(required = True) 
    category_id = IntField(required = True) 
    meta = {
        "indexes" : [ 
            "entity_id", 
            "note_id",
            "root_category_id",
            "neo_category_group_id",
            "neo_category_id",
            "category_id" 
        ]
    }

