# coding=utf8
from common.user import RBUser
from mobile.lib.http import SuccessJsonResponse
from mobile.models import Session_Key 

def login(request):
    if request.method == "POST":
        _email = request.POST.get('email', None)
        _password = request.POST.get('password', None)
        _api_key = request.POST.get('api_key', None)

        _user = RBUser.login(
            email = _email, 
            password = _password
        )
        _session = Session_Key.objects.generate_session(
            user_id = _user.get_user_id(),
            username = _user.get_username(),
            email = _email,
            api_key = _api_key
        )
        
        _data = {
            'user' : _user.read(),
            'session' : _session.session_key
        }
        return SuccessJsonResponse(_data)

def register(request):
    _req_uri = request.get_full_path()

    if request.method == "POST":
        _email = request.POST.get('email', None)
        _password = request.POST.get('password', None)
        _nickname = request.POST.get('nickname', None)
        _api_key = request.POST.get('api_key', None)
        #_dev_token = request.POST.get('dev_token', None)
        
        _user = RBUser.create(
            email = _email, 
            password = _password
        )
        _user.set_profile(
            nickname = _nickname
        )
        _session = Session_Key.objects.generate_session(
            user_id = _user.get_user_id(),
            username = _user.get_username(),
            email = _email,
            api_key = _api_key
        )

        _data = {
            'user' : _user.read(),
            'session' : _session.session_key
        }
        return SuccessJsonResponse(_data)

#def logout(request):
#    _req_uri = request.get_full_path()
#    if request.method == "POST":
#        _session = request.POST.get('session', None)
#        _dev_token = request.POST.get('dev_token', None)
#        logger.info("%s" % _session)
#        _res = Account.logout(session=_session, dev_token=_dev_token)
#        # _res = []
#        return SuccessV2JsonResponse(data=_res, req_uri=_req_uri)
#
#
#def forget_passwd(request):
#    _req_uri = request.get_full_path()
#    _host = request.get_host()
#    if request.method == "POST":
#        _email = request.POST.get('email', None)
#        try:
#            _user = Account(email=_email)
#            _user.forget_passwd(host=_host)
#            return SuccessV2JsonResponse(req_uri=_req_uri)
#        except Account.AbsentEmailError, e:
#            return ErrorJsonResponse(ecode=EMAIL_NOT_EXIST, emsg=e.message, req_uri=_req_uri)
