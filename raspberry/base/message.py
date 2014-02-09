# coding=utf-8
from mongoengine import *
import datetime
from utils.apns_notification import APNSWrapper

class NeoMessage(Document):
    user_id = IntField(required = True) 
    created_time = DateTimeField(required = True)
    meta = {
        'db_alias' : 'guoku-db',
        'indexes' : [ 
            'user_id',
            'created_time',
        ],
        'allow_inheritance' : True
    }


class UserFollowMessage(NeoMessage):
    follower_id = IntField(required = True) 
    meta = {
        'indexes' : [ 
            'follower_id' 
        ]
    }
    
    @classmethod
    def create(cls, user_id, user_unread_message_count, follower_id, follower_nickname):
        _doc = cls(
            user_id = user_id, 
            follower_id = follower_id, 
            created_time = datetime.datetime.now()
        )
        _doc.save()
        
        _apns = APNSWrapper(user_id = user_id)
        _apns.badge(badge = user_unread_message_count + 1) 
        _apns.alert(u"%s 开始关注你"%follower_nickname)
        _apns.message(message = {
            'followee_id' : user_id,
            'follower_id' : follower_id,
            'type' : 'user_follow' 
        })
        _apns.push()


class NotePokeMessage(NeoMessage):
    note_id = IntField(required = True)
    poker_id = IntField(required = True)
    meta = {
        'indexes' : [ 
            'note_id', 
            'poker_id', 
        ]
    }
    
    @classmethod
    def create(cls, user_id, user_unread_message_count, note_id, poker_id, poker_nickname):
        _doc = cls(
            user_id = user_id, 
            note_id = note_id,
            poker_id = poker_id,
            created_time = datetime.datetime.now()
        )
        _doc.save()
            
        _apns = APNSWrapper(user_id = user_id)
        _apns.badge(badge = user_unread_message_count + 1) 
        _apns.alert(u"%s 赞了你的点评"%poker_nickname)
        _apns.message(message = {
            'note_id' : note_id, 
            'type' : 'note_poke' 
        })
        _apns.push()


class NoteCommentMessage(NeoMessage):
    note_id = IntField(required = True)
    comment_id = IntField(required = True)
    comment_creator_id = IntField(required = True)
    meta = {
        'indexes' : [ 
            'note_id', 
            'comment_id', 
            'comment_creator_id', 
        ]
    }
    
    @classmethod
    def create(cls, user_id, user_unread_message_count, note_id, comment_id, comment_creator_id, comment_creator_nickname):
        _doc = cls(
            user_id = user_id, 
            note_id = note_id,
            comment_id = comment_id,
            comment_creator_id = comment_creator_id,
            created_time = datetime.datetime.now()
        )
        _doc.save()
            
        _apns = APNSWrapper(user_id = user_id)
        _apns.badge(badge = user_unread_message_count + 1) 
        _apns.alert(u"%s 评论了你的点评"%comment_creator_nickname)
        _apns.message(message = {
            'note_id' : note_id, 
            'comment_id' : comment_id, 
            'type' : 'note_comment' 
        })
        _apns.push()

class NoteCommentReplyMessage(NeoMessage):
    note_id = IntField(required = True)
    comment_id = IntField(required = True)
    replying_comment_id = IntField(required = True)
    replying_user_id = IntField(required = True)
    meta = {
        'indexes' : [ 
            'note_id', 
            'comment_id', 
            'replying_comment_id', 
            'replying_user_id', 
        ]
    }
    
    @classmethod
    def create(cls, user_id, user_unread_message_count, note_id, comment_id, replying_comment_id, replying_user_id, replying_user_nickname): 
        _doc = cls(
            user_id = user_id, 
            note_id = note_id,
            comment_id = comment_id,
            replying_comment_id = replying_comment_id,
            replying_user_id = replying_user_id,
            created_time = datetime.datetime.now()
        )
        _doc.save()
            
        _apns = APNSWrapper(user_id = user_id)
        _apns.badge(badge = user_unread_message_count + 1) 
        _apns.alert(u"%s 回应了你的评论"%replying_user_nickname)
        _apns.message(message = {
            'note_id' : note_id, 
            'comment_id' : comment_id, 
            'replying_comment_id' : replying_comment_id, 
            'replying_user_id' : replying_user_id, 
            'type' : 'note_comment_reply' 
        })
        _apns.push()


class EntityLikeMessage(NeoMessage):
    entity_id = IntField(required = True)
    liker_id  = IntField(required = True)
    meta = {
        'indexes' : [ 
            'entity_id', 
            'liker_id', 
        ]
    }

class EntityNoteMessage(NeoMessage):
    entity_id = IntField(required = True)
    note_id = IntField(required = True)
    meta = {
        'indexes' : [ 
            'entity_id', 
            'note_id', 
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
        _apns.badge(badge = user_unread_message_count + 1) 
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
        'indexes' : [ 
            'entity_id', 
            'note_id', 
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
        _apns.badge(badge = user_unread_message_count + 1) 
        _apns.alert(u"你添加的商品被收录精选")
        _apns.message(message = {
            'entity_id' : entity_id, 
            'note_id' : note_id, 
            'type' : 'note_selected' 
        })
        _apns.push()

