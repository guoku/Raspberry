# coding=utf8
from lib.entity import RBMobileNote
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from mobile.models import Session_Key
import datetime

def note_detail(request, note_id):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None

        _rslt = RBMobileNote(note_id).read_note_full_context(_request_user_id)
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


