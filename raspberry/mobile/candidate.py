# coding=utf8
from lib.candidate import RBMobileCandidate
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key
import datetime


def create_candidate(request):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _note_text = request.POST.get('note', None)
        _score = int(request.POST.get('score', '0'))
        _brand = request.POST.get('brand', '')
        _title = request.POST.get('title', '')
        _category_id = request.POST.get('category_id', None)
        if _category_id != None:
            _category_id = int(_category_id)
        _category_text = request.POST.get('category_text', '')
        
        _image_file = request.FILES.get('image', None)
        if _image_file == None:
            _image_data = None
        else:
            if hasattr(_image_file, 'chunks'):
                _image_data = ''.join(chunk for chunk in _image_file.chunks())
            else:
                _image_data = _image_file.read()
        
        _candidate = RBMobileCandidate.create(
            creator_id = _request_user_id, 
            category_id = _category_id, 
            category_text = _category_text, 
            brand = _brand, 
            title = _title, 
            score = _score, 
            note_text = _note_text, 
            image_data = _image_data
        )
        return SuccessJsonResponse(_candidate.read())
            

        
