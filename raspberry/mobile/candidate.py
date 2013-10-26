# coding=utf8
from lib.candidate import RBMobileCandidate
from lib.note import RBMobileNote
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
        _category_id = int(request.POST.get('category_id', '0'))
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
        _note_id = _candidate.get_note()
        _note = RBMobileNote(_note_id)
        return SuccessJsonResponse(_note.read())
            
def category_candidate(request, category_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        
        _candidate_id_list = RBMobileCandidate.find(
            category_id = category_id
        )
        _rslt = []
        for _candidate_id in _candidate_id_list:
            _note_id = RBMobileCandidate(_candidate_id).get_note()
            _note = RBMobileNote(_note_id)
            _rslt.append(
                _note.read(_request_user_id)
            )
            
        return SuccessJsonResponse(_rslt)

