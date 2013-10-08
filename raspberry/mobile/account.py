__author__ = 'edison'

from django.utils.log import logger
from mobile.core.decorators import _check_sign as check_sign
from mobile.core.v2_res_code import *
from mobile.core.http import SuccessV2JsonResponse, ErrorJsonResponse
from mobile.lib.accounts import Account, Session
# from mobile.lib.users import UserManagerV2
from mobile.lib.three_part import WeiBo, Taobao
from mobile.tasks import UpdateUserToken

@check_sign
def login(request):
    _req_uri = request.get_full_path()

    if request.method == "POST":
        _email = request.POST.get('email', None)
        _passwd = request.POST.get('passwd', None)
        _api_key = request.POST.get('api_key', None)
        _dev_token = request.POST.get('dev_token', None)
        logger.info("user email %s and passwd %s" % (_email, _passwd))

        _user = Account(email=_email)
        try:
            _profile =  _user.login(passwd=_passwd, api_key=_api_key)
            UpdateUserToken.delay(user_id=_profile['user_id'], dev_token=_dev_token)
            return SuccessV2JsonResponse(data=_profile, req_uri=_req_uri)
        except Account.AbsentUserError, e:
            return ErrorJsonResponse(ecode=e.code, emsg=e.message, req_uri=_req_uri)
        except Account.UserPasswdError, e:
            return ErrorJsonResponse(ecode=PASSWD_NOT_MATCH, emsg=e.message, req_uri=_req_uri)

@check_sign
def register(request):
    _req_uri = request.get_full_path()

    if request.method == "POST":
        _email = request.POST.get('email', None)
        _passwd = request.POST.get('passwd', None)
        _nickname = request.POST.get('nickname', None)
        _api_key = request.POST.get('api_key', None)
        _dev_token = request.POST.get('dev_token', None)
        _user = Account(email=_email)
        try:
            _profile = _user.create(passwd=_passwd, nickname=_nickname, api_key=_api_key)
            UpdateUserToken.delay(user_id=_profile['user_id'], dev_token=_dev_token)
            return SuccessV2JsonResponse(data=_profile, req_uri=_req_uri)
            # logger.info(_profile)
        except Account.NicknameIsUsed, e:
            return ErrorJsonResponse(ecode=NICK_IS_USED, emsg=e.message, req_uri=_req_uri)
        except Account.EmailIsExist, e:
            return ErrorJsonResponse(ecode=EMAIL_IS_REGISTER, emsg=e.message, req_uri=_req_uri)

@check_sign
def logout(request):
    _req_uri = request.get_full_path()
    if request.method == "POST":
        _session = request.POST.get('session', None)
        _dev_token = request.POST.get('dev_token', None)
        logger.info("%s" % _session)
        _res = Account.logout(session=_session, dev_token=_dev_token)
        # _res = []
        return SuccessV2JsonResponse(data=_res, req_uri=_req_uri)


@check_sign
def forget_passwd(request):
    _req_uri = request.get_full_path()
    _host = request.get_host()
    if request.method == "POST":
        _email = request.POST.get('email', None)
        try:
            _user = Account(email=_email)
            _user.forget_passwd(host=_host)
            return SuccessV2JsonResponse(req_uri=_req_uri)
        except Account.AbsentEmailError, e:
            return ErrorJsonResponse(ecode=EMAIL_NOT_EXIST, emsg=e.message, req_uri=_req_uri)


