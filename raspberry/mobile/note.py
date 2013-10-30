# coding=utf8
from lib.entity import RBMobileEntity
from lib.note import RBMobileNote
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key
import datetime

def update_note(request, note_id):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _note_text = request.POST.get('note', None)
        _score = int(request.POST.get('score', None))

        _image_file = request.FILES.get('image', None)
        if _image_file == None:
            _image_data = None
        else:
            if hasattr(_image_file, 'chunks'):
                _image_data = ''.join(chunk for chunk in _image_file.chunks())
            else:
                _image_data = _image_file.read()
        
        ## There's no authorize confirmation yet ##
        
        _entity_id = RBMobileNote(note_id).get_entity_of_note()
        _entity = RBMobileEntity(_entity_id)
        _note = _entity.update_note(
            note_id = note_id,
            score = _score,
            note_text = _note_text,
            image_data = _image_data
        )
        _rslt = _note.read(_request_user_id)
        return SuccessJsonResponse(_rslt)

def note_detail(request, note_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        
        _rslt = {}
        _rslt = RBMobileNote(note_id).read_note_full_context(_request_user_id)
        if _rslt['note'].has_key('entity_id'):
            _rslt['entity'] = RBMobileEntity(_rslt['note']['entity_id']).read()
        return SuccessJsonResponse(_rslt)

def poke_note(request, note_id, target_status):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        
        _request_user_id = Session_Key.objects.get_user_id(_session)
        _rslt = { 
            'note_id' : note_id 
        }
        if target_status == '1':
            RBMobileNote(note_id).poke(_request_user_id)
            _rslt['poke_already'] = 1
        else:
            RBMobileNote(note_id).depoke(_request_user_id)
            _rslt['poke_already'] = 0
        return SuccessJsonResponse(_rslt)

def comment_note(request, note_id):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        _comment_text = request.POST.get('comment', None)
        
        _request_user_id = Session_Key.objects.get_user_id(_session)
        
        _note = RBMobileNote(note_id)
        _comment_id = _note.add_comment(
            comment_text = _comment_text, 
            creator_id = _request_user_id, 
            reply_to = None,
        )
        _context = _note.read_comment(_comment_id)
        return SuccessJsonResponse(_context)


