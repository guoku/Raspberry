# coding=utf-8

from django import template
import datetime
register = template.Library()


def format_time(value):
    time_interval = (datetime.datetime.now() - value).total_seconds()
    if time_interval < 60:
        return "%d 秒前" % (time_interval)
    elif time_interval < 60 * 60:
        return "%d 分钟前" % ((time_interval / 60) + 1)
    elif time_interval < 60 * 60 * 24:
        return "%d 小时前" % (time_interval / (60 * 60) + 1)
    elif time_interval < 60 * 60 * 48:
        return "昨天"
    elif time_interval < 60 * 60 * 72:
        return "前天"
    return "%d 年 %d 月 %d 日" % (value.year, value.month, value.day)

register.filter(format_time)


def display_web_paginator(paginator):
    return {
        "paginator" : paginator
    }

register.inclusion_tag("common/web_paginator.html")(display_web_paginator)


# for note ---
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


# for user ---
def display_user_entity(entity_list):
    return {
        'entity_list' : entity_list
    }

register.inclusion_tag("user/partial/display_entity.html")(display_user_entity)


def display_user_notes(note_list):
    return {
        'note_list' : note_list
    }

register.inclusion_tag("user/partial/display_note.html")(display_user_notes)


def display_user_tags(tag_list):
    return {
        'tag_list' : tag_list
    }

register.inclusion_tag("user/partial/display_tag.html")(display_user_tags)


def display_user_users(user_list):
    return {
        'user_list' : user_list
    }

register.inclusion_tag("user/partial/display_user.html")(display_user_users)


# for account
def display_avatar_update(user_context):
    return {
        'user_context' : user_context
    }

register.inclusion_tag("account/partial/display_avatar_update.html")(display_avatar_update)