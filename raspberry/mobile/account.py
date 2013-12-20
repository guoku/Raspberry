# coding=utf8
from lib.apns import Apns 
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from lib.sign import check_sign
from lib.user import MobileUser
from mobile.models import Session_Key 
from tasks import RetrievePasswordTask 

@check_sign
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
            

#@check_sign
def login_by_sina(request):
    if request.method == "POST":
        _sina_id = request.POST.get('sina_id', None)
        _sina_token = request.POST.get('sina_token', None)
        _screen_name = request.POST.get('screen_name', None)
        _api_key = request.POST.get('api_key', None)
        
        try:
            _user = MobileUser.login_by_sina(
                sina_id = _sina_id,
                sina_token = _sina_token,
                screen_name = _screen_name
            )
            _session = Session_Key.objects.generate_session(
                user_id = _user.user_id,
                username = _user.get_username(),
                email = _user.get_email(),
                api_key = _api_key
            )
            
            _data = {
                'user' : _user.read(_user.user_id),
                'session' : _session.session_key
            }
            return SuccessJsonResponse(_data)
        except MobileUser.LoginSinaIdDoesNotExist, e:
            return ErrorJsonResponse(
                data = {
                    'type' : 'sina_id',
                    'message' : str(e),
                },
                status = 400
            )


@check_sign
def login_by_taobao(request):
    if request.method == "POST":
        _taobao_id = request.POST.get('taobao_id', None)
        _taobao_token = request.POST.get('taobao_token', None)
        _api_key = request.POST.get('api_key', None)
        
        try:
            _user = MobileUser.login_by_taobao(
                taobao_id = _taobao_id,
                taobao_token = _taobao_token
            )
            _session = Session_Key.objects.generate_session(
                user_id = _user.user_id,
                username = _user.get_username(),
                email = _user.get_email(),
                api_key = _api_key
            )
            
            _data = {
                'user' : _user.read(_user.user_id),
                'session' : _session.session_key
            }
            return SuccessJsonResponse(_data)
        except MobileUser.LoginTaobaoIdDoesNotExist, e:
            return ErrorJsonResponse(
                data = {
                    'type' : 'taobao_id',
                    'message' : str(e),
                },
                status = 400
            )


@check_sign
def register(request):
    if request.method == "POST":
        _email = request.POST.get('email', None)
        _password = request.POST.get('password', None)
        _nickname = request.POST.get('nickname', None)
        _api_key = request.POST.get('api_key', None)
        
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
        
        try:
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
        except Exception, e: 
            _user.delete()
            return ErrorJsonResponse(
                data = {
                    'type' : 'image',
                    'message' : str(e),
                },
                status = 409
            )
        return SuccessJsonResponse(_data)


@check_sign
def register_by_sina(request):
    if request.method == "POST":
        _email = request.POST.get('email', None)
        _password = request.POST.get('password', None)
        _nickname = request.POST.get('nickname', None)
        _api_key = request.POST.get('api_key', None)
        _sina_id = request.POST.get('sina_id', None)
        _sina_token = request.POST.get('sina_token', None)
        _screen_name = request.POST.get('screen_name', None)

        try:
            _user = MobileUser.create_by_sina(
                sina_id = _sina_id,
                sina_token = _sina_token,
                screen_name = _screen_name,
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
        except MobileUser.SinaIdExistAlready, e:
            return ErrorJsonResponse(
                data = {
                    'type' : 'sina_id',
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
        
        try:
            _image_file = request.FILES.get('image', None)
            if _image_file != None:
                if hasattr(_image_file, 'chunks'):
                    _image_data = ''.join(chunk for chunk in _image_file.chunks())
                else:
                    _image_data = _image_file.read()
                _user.upload_avatar(_image_data)
        except Exception, e: 
            _user.delete()
            return ErrorJsonResponse(
                data = {
                    'type' : 'avatar',
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
        
        _data = {
            'user' : _user.read(_user.user_id),
            'session' : _session.session_key
        }
        return SuccessJsonResponse(_data)

@check_sign
def register_by_taobao(request):
    if request.method == "POST":
        _email = request.POST.get('email', None)
        _password = request.POST.get('password', None)
        _nickname = request.POST.get('nickname', None)
        _api_key = request.POST.get('api_key', None)
        _taobao_id = request.POST.get('taobao_id', None)
        _taobao_token = request.POST.get('taobao_token', None)
        _screen_name = request.POST.get('screen_name', None)
        
        
        try:
            _user = MobileUser.create_by_taobao(
                taobao_id = _taobao_id,
                taobao_token = _taobao_token,
                screen_name = _screen_name,
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
        except MobileUser.TaobaoIdExistAlready, e:
            return ErrorJsonResponse(
                data = {
                    'type' : 'taobao_id',
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
        
        
        try:
            _image_file = request.FILES.get('image', None)
            if _image_file != None:
                if hasattr(_image_file, 'chunks'):
                    _image_data = ''.join(chunk for chunk in _image_file.chunks())
                else:
                    _image_data = _image_file.read()
                _user.upload_avatar(_image_data)
        except Exception, e: 
            _user.delete()
            return ErrorJsonResponse(
                data = {
                    'type' : 'avatar',
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
        
        _data = {
            'user' : _user.read(_user.user_id),
            'session' : _session.session_key
        }
        return SuccessJsonResponse(_data)

@check_sign
def logout(request):
    _req_uri = request.get_full_path()
    if request.method == "POST":
        _session = request.POST.get('session', None)
        _session_obj = Session_Key.objects.get(session_key = _session)
        _session_obj.delete()
        
        return SuccessJsonResponse("1")


@check_sign
def forget_password(request):
    if request.method == "POST":
        _email = request.POST.get('email', None)
        _user_id = MobileUser.get_user_id_by_email(_email)
        if _user_id == None:
            return ErrorJsonResponse(
                data = {
                    'type' : 'email',
                    'message' : 'email does not exist', 
                },
                status = 400
            )
        RetrievePasswordTask.delay(_user_id)

        return SuccessJsonResponse("1")

@check_sign
def apns_token(request):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        
        _dev_token = request.POST.get('dev_token', None)
        _dev_name = request.POST.get('dev_name', None)
        _dev_model = request.POST.get('dev_model', None)
        _sys_ver = request.POST.get('sys_ver', None)
        _app_name = request.POST.get('app_name', None)
        _app_ver = request.POST.get('app_ver', None)
        _push_badge = request.POST.get('push_badge', False)
        _push_alert = request.POST.get('push_alert', False)
        _push_sound = request.POST.get('push_sound', False)
        _development = request.POST.get('development', False)
       
        if _dev_token != None:
            _apns = Apns(_dev_token)
            _apns.create( 
                user_id = _request_user_id,
                dev_name = _dev_name,
                dev_models = _dev_model,
                sys_ver = _sys_ver,
                app_ver = _app_ver,
                push_badge = _push_badge,
                push_alert = _push_alert,
                push_sound = _push_sound,
                development = _development
            )

        return SuccessJsonResponse({ 'success' : '1' }) 
