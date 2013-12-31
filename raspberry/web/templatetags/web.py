# coding=utf-8

from django import template
import datetime
from base.note import Note
from base.user import User

register = template.Library()


# note ---
def display_note(note, entity_context, user_context):
    return {
        'note_context' : note['note_context'],
        'creator_context' : note['creator_context'],
        'comment_list' : note['comment_list'],
        'entity_context' : entity_context,
        'user_context' : user_context
    }

register.inclusion_tag("main/partial/display_note.html")(display_note)


def display_note_comment(comment, user_context, note_context):
    return {
        'comment_context' : comment['comment_context'],
        'creator_context' : comment['creator_context'],
        'user_context' : user_context,
        'note_context' : note_context,
    }

register.inclusion_tag("main/partial/display_note_comment.html")(display_note_comment)


# user ---
def display_user_entities(entity_list):
    return {

    }

register.inclusion_tag("user/partial/display_entity.html")(display_user_entities)


def display_user_notes(note_list):
    return {

    }

register.inclusion_tag("user/partial/display_note.html")(display_user_notes)


def display_user_tags(tag_list):
    return {

    }

register.inclusion_tag("user/partial/display_tag.html")(display_user_tags)


def display_user_users(user_list):
    return {

    }

register.inclusion_tag("user/partial/display_user.html")(display_user_users)

