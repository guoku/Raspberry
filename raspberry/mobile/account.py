# coding=utf8
from lib.user import MobileUser
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key 

def login(request):
    if request.method == "POST":
        _email = request.POST.get('email', None)
        _password = request.POST.get('password', None)
        _api_key = request.POST.get('api_key', None)
        
        try:
            _user = MobileUser.login(
                email = _email, 
                password = _password
            )
            _session = Session_Key.objects.generate_session(
                user_id = _user.user_id,
                username = _user.get_username(),
                email = _email,
                api_key = _api_key
            )
            
            _data = {
                'user' : _user.read(_user.user_id),
                'session' : _session.session_key
            }
            return SuccessJsonResponse(_data)
        except MobileUser.LoginEmailDoesNotExist, e:
            return ErrorJsonResponse(
                data = {
                    'type' : 'email',
                    'message' : str(e),
                },
                status = 400
            )
        except MobileUser.LoginPasswordIncorrect, e:
            return ErrorJsonResponse(
                data = {
                    'type' : 'password',
                    'message' : str(e),
                },
                status = 400
            )
            

def register(request):
    _req_uri = request.get_full_path()

    if request.method == "POST":
        _email = request.POST.get('email', None)
        _password = request.POST.get('password', None)
        _nickname = request.POST.get('nickname', None)
        _api_key = request.POST.get('api_key', None)
        #_dev_token = request.POST.get('dev_token', None)
        
        try:
            _user = MobileUser.create(
                email = _email, 
                password = _password
            )
        except MobileUser.EmailExistAlready, e:
            return ErrorJsonResponse(
                data = {
                    'type' : 'email',
                    'message' : str(e),
                },
                status = 409
            )
            

        try:
            _user.set_profile(
                nickname = _nickname
            )
        except MobileUser.NicknameExistAlready, e:
            _user.delete()
            return ErrorJsonResponse(
                data = {
                    'type' : 'nickname',
                    'message' : str(e),
                },
                status = 409
            )
        
        _session = Session_Key.objects.generate_session(
            user_id = _user.user_id,
            username = _user.get_username(),
            email = _email,
            api_key = _api_key
        )
        
        _image_file = request.FILES.get('image', None)
        if _image_file != None:
            if hasattr(_image_file, 'chunks'):
                _image_data = ''.join(chunk for chunk in _image_file.chunks())
            else:
                _image_data = _image_file.read()
            _user.upload_avatar(_image_data)

        _data = {
            'user' : _user.read(_user.user_id),
            'session' : _session.session_key
        }
        return SuccessJsonResponse(_data)

def logout(request):
    _req_uri = request.get_full_path()
    if request.method == "POST":
        _session = request.POST.get('session', None)
        _session_obj = Session_Key.objects.get(session_key = _session)
        _session_obj.delete()
        
        return SuccessJsonResponse("1")


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
