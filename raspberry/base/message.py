# coding=utf-8
from mongoengine import *
import datetime
from utils.apns_notification import APNSWrapper

class NeoMessage(Document):
    user_id = IntField(required = True) 
    created_time = DateTimeField(required = True)
    meta = {
        "indexes" : [ 
            "user_id",
            "created_time",
        ],
        "allow_inheritance" : True
    }


class UserFollowMessage(NeoMessage):
    follower_id = IntField(required = True) 
    meta = {
        "indexes" : [ 
            "follower_id" 
        ]
    }

class NotePokeMessage(NeoMessage):
    note_id = IntField(required = True)
    poker_id = IntField(required = True)
    meta = {
        "indexes" : [ 
            "note_id", 
            "poker_id", 
        ]
    }

class NoteCommentMessage(NeoMessage):
    note_id = IntField(required = True)
    comment_id = IntField(required = True)
    comment_creator_id = IntField(required = True)
    meta = {
        "indexes" : [ 
            "note_id", 
            "comment_id", 
            "comment_creator_id", 
        ]
    }

class NoteCommentReplyMessage(NeoMessage):
    note_id = IntField(required = True)
    comment_id = IntField(required = True)
    replying_comment_id = IntField(required = True)
    replying_user_id = IntField(required = True)
    meta = {
        "indexes" : [ 
            "note_id", 
            "comment_id", 
            "replying_comment_id", 
            "replying_user_id", 
        ]
    }

class EntityLikeMessage(NeoMessage):
    entity_id = IntField(required = True)
    liker_id  = IntField(required = True)
    meta = {
        "indexes" : [ 
            "entity_id", 
            "liker_id", 
        ]
    }

class EntityNoteMessage(NeoMessage):
    entity_id = IntField(required = True)
    note_id = IntField(required = True)
    meta = {
        "indexes" : [ 
            "entity_id", 
            "note_id", 
        ]
    }
    
    @classmethod
    def create(cls, user_id, user_unread_message_count, entity_id, note_id):
        _doc = cls(
            user_id = user_id, 
            entity_id = entity_id,
            note_id = note_id, 
            created_time = datetime.datetime.now()
        )
        _doc.save()
            
        _apns = APNSWrapper(user_id = user_id)
        _apns.badge(badge = user_unread_message_count) 
        _apns.alert(u"你添加的商品收到了一条新点评")
        _apns.message(message = {
            'entity_id' : entity_id, 
            'note_id' : note_id, 
            'type' : 'new_note' 
        })
        _apns.push()

class NoteSelectionMessage(NeoMessage):
    entity_id = IntField(required = True)
    note_id = IntField(required = True)
    meta = {
        "indexes" : [ 
            "entity_id", 
            "note_id", 
        ]
    }

