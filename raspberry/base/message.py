# coding=utf-8
from mongoengine import *
import datetime

class Message(Document):
    user_id = IntField(required = True) 
    created_time = DateTimeField(required = True)
    meta = {
        "indexes" : [ 
            "user_id",
            "created_time",
        ],
        "allow_inheritance" : True
    }


class UserFollowMessage(Message):
    follower_id = IntField(required = True) 
    meta = {
        "indexes" : [ 
            "follower_id" 
        ]
    }

class NotePokeMessage(Message):
    note_id = IntField(required = True)
    poker_id = IntField(required = True)
    meta = {
        "indexes" : [ 
            "note_id", 
            "poker_id", 
        ]
    }

class NoteCommentMessage(Message):
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

class NoteCommentReplyMessage(Message):
    note_id = IntField(required = True)
    comment_id = IntField(required = True)
    replying_user_id = IntField(required = True)
    meta = {
        "indexes" : [ 
            "note_id", 
            "comment_id", 
            "replying_user_id", 
        ]
    }

