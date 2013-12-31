# coding=utf-8
from base.user import User


def get_user_context(request_user):
    _user_context = None

    if request_user.is_authenticated():
        _user_context = User(request_user.id).read()

    return _user_context