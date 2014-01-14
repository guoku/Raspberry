# coding=utf-8
from base.user import User
from base.entity import Entity


def get_request_user(request_user_id):
    if request_user_id is None:
        return None
    return User(request_user_id)


def get_request_user_context(user):
    if user is None:
        return None
    return user.read()


def user_already_like_entity(user_id, entity_id):
    if entity_id is None or user_id is None:
        return False

    return Entity(entity_id).like_already(user_id)