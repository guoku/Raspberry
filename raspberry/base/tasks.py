# coding=utf-8
from celery.task import Task
from celery.task import PeriodicTask 
from django.conf import settings

from message import EntityNoteMessage, NoteSelectionMessage, UserFollowMessage, NotePokeMessage, NoteCommentMessage, NoteCommentReplyMessage
import popularity
import datetime
import time

POPULAR_ENTITY_RUN_INTERVAL_SECS = getattr(settings, 'POPULAR_ENTITY_RUN_INTERVAL_SECS', 600)
MAX_RETRIES = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRIES', 5)
RETRY_DELAY = getattr(settings, 'QUEUED_REMOTE_STORAGE_RETRY_DELAY', 60)

class CalPopularEntity(PeriodicTask):
    ignore_result = True
    time_limit = 600
    run_every = datetime.timedelta(seconds = POPULAR_ENTITY_RUN_INTERVAL_SECS) 
    queue = "main"
    
    def run(self):
        t_start = datetime.datetime.now()
        popularity.generate_popular_entity()
        print "popular entity updated...%s secs cost" % str(datetime.datetime.now() - t_start)

class CreateEntityNoteMessageTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, user_id, user_unread_message_count, entity_id, note_id): 
        EntityNoteMessage.create(
            user_id = user_id, 
            user_unread_message_count = user_unread_message_count, 
            entity_id = entity_id,
            note_id = note_id
        )

class CreateNoteSelectionMessageTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, user_id, user_unread_message_count, entity_id, note_id):
        NoteSelectionMessage.create(
            user_id = user_id, 
            user_unread_message_count = user_unread_message_count, 
            entity_id = entity_id,
            note_id = note_id
        )

class CreateUserFollowMessageTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, user_id, user_unread_message_count, follower_id, follower_nickname):
        UserFollowMessage.create(
            user_id = user_id, 
            user_unread_message_count = user_unread_message_count,
            follower_id = follower_id,
            follower_nickname = follower_nickname
        )

class CreateNotePokeMessageTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, user_id, user_unread_message_count, note_id, poker_id, poker_nickname):
        NotePokeMessage.create(
            user_id = user_id, 
            user_unread_message_count = user_unread_message_count,
            note_id = note_id,
            poker_id = poker_id,
            poker_nickname = poker_nickname
        )

class CreateNoteCommentMessageTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, user_id, user_unread_message_count, note_id, comment_id, comment_creator_id, comment_creator_nickname):
        NoteCommentMessage.create(
            user_id = user_id, 
            user_unread_message_count = user_unread_message_count,
            note_id = note_id,
            comment_id = comment_id,
            comment_creator_id = comment_creator_id,
            comment_creator_nickname = comment_creator_nickname
        )

class CreateNoteCommentReplyMessageTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, user_id, user_unread_message_count, note_id, comment_id, replying_comment_id, replying_user_id, replying_user_nickname): 
        NoteCommentReplyMessage.create(
            user_id = user_id, 
            user_unread_message_count = user_unread_message_count,
            note_id = note_id,
            comment_id = comment_id,
            replying_comment_id = replying_comment_id,
            replying_user_id = replying_user_id,
            replying_user_nickname = replying_user_nickname
        )

class CleanNoteMessageTask(Task):
    ignore_result = True
    time_limit = 60
    max_retries = MAX_RETRIES
    default_retry_delay = RETRY_DELAY
    queue = "main"
    
    def run(self, entity_id, note_id): 
        for _doc in EntityNoteMessage.objects.filter(entity_id = entity_id, note_id = note_id):
            _doc.delete()
        
        for _doc in NotePokeMessage.objects.filter(note_id = note_id):
            _doc.delete()
        
        for _doc in NoteCommentMessage.objects.filter(note_id = note_id):
            _doc.delete()
        
        for _doc in NoteCommentReplyMessage.objects.filter(note_id = note_id):
            _doc.delete()
        
        for _doc in NoteSelectionMessage.objects.filter(note_id = note_id):
            _doc.delete()

