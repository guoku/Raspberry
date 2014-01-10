# coding=utf-8
from base.user import User
from base.entity import Entity


def get_request_user_context(request_user):
    _user_context = None

    if request_user.is_authenticated():
        _user_context = User(request_user.id).read()

    return _user_context


def user_already_like_entity(user_id, entity_id):
    if entity_id is None or user_id is None:
        return False

    return Entity(entity_id).like_already(user_id)