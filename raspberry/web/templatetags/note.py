# coding=utf-8
from django import template

register = template.Library()


def display_comment_item(comment):
    return {
        'comment_context': comment['comment_context'],
        'creator_context': comment['creator_context'],
        'note_context' : comment['note_context'],
        'user_context' : comment['user_context']
    }

register.inclusion_tag("note/note_comment.html")(display_comment_item)