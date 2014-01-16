# coding=utf-8
from django import template
register = template.Library()


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
        'user_list' : user_list,
    }

register.inclusion_tag("user/partial/display_user.html")(display_user_users)