# coding=utf8
from lib.entity import MobileEntity
from lib.note import MobileNote
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from lib.sign import check_sign
from mobile.models import Session_Key
from share.tasks import DeleteEntityNoteCommentTask, PokeEntityNoteTask, DepokeEntityNoteTask
from tasks import MobileLogTask 
from utils.lib import get_client_ip
import datetime
import time 

@check_sign
def category_entity_note(request, category_id):
    _start_at = datetime.datetime.now()
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _sort_by = request.GET.get('sort', 'poke')
        if _sort_by == '':
            _sort_by = 'poke'
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        
        _note_id_list = MobileNote.find(
            category_id = category_id,
            offset = _offset,
            count = _count,
            sort_by = _sort_by
        )
        _rslt = []
        for _note_id in _note_id_list:
            _note_context = MobileNote(_note_id).read(_request_user_id)
            if _note_context.has_key('entity_id'):
                _entity = MobileEntity(_note_context['entity_id'])
                _rslt.append({
                    'entity' : _entity.read(_request_user_id),
                    'note' : _note_context,
                })
            
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'CATEGORY_NOTE_LIST', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'neo_category_id' : int(category_id),
                'result_notes' : _note_id_list
            },
        )
        return SuccessJsonResponse(_rslt)

@check_sign
def search_entity_note(request):
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None

        _query_string = request.GET.get('q')
        _offset = int(request.GET.get('offset', '0'))
        _count = int(request.GET.get('count', '30'))
        _note_id_list = MobileNote.search(
            query_string = _query_string
        )
        
        _rslt = []
        for _note_id in _note_id_list:
            _note_context = MobileNote(_note_id).read(_request_user_id)
            if _note_context.has_key('entity_id'):
                _entity = MobileEntity(_note_context['entity_id'])
                _rslt.append({
                    'entity' : _entity.read(_request_user_id),
                    'note' : _note_context,
                })
        
        return SuccessJsonResponse(_rslt)
        
@check_sign
def update_entity_note(request, note_id):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        _note_text = request.POST.get('note', None)
        _image_file = request.FILES.get('image', None)
        if _image_file == None:
            _image_data = None
        else:
            if hasattr(_image_file, 'chunks'):
                _image_data = ''.join(chunk for chunk in _image_file.chunks())
            else:
                _image_data = _image_file.read()
        
        ## There's no authorize confirmation yet ##
        
        _note = MobileNote(note_id)
        _note.update(
            note_text = _note_text,
            image_data = _image_data
        )
        _rslt = _note.read(_request_user_id)
        return SuccessJsonResponse(_rslt)

@check_sign
def entity_note_detail(request, note_id):
    _start_at = datetime.datetime.now()
    if request.method == "GET":
        _session = request.GET.get('session', None)
        if _session != None:
            _request_user_id = Session_Key.objects.get_user_id(_session)
        else:
            _request_user_id = None
        
        _rslt = {}
        _rslt = MobileNote(note_id).read_note_full_context(_request_user_id)
        if _rslt['note'].has_key('entity_id'):
            _rslt['entity'] = MobileEntity(_rslt['note']['entity_id']).read(_request_user_id)
        
        _duration = datetime.datetime.now() - _start_at
        MobileLogTask.delay(
            duration = _duration.seconds * 1000000 + _duration.microseconds, 
            view = 'NOTE', 
            request = request.REQUEST, 
            ip = get_client_ip(request), 
            log_time = datetime.datetime.now(),
            request_user_id = _request_user_id,
            appendix = { 
                'note_id' : int(note_id), 
            },
        )
        return SuccessJsonResponse(_rslt)

@check_sign
def poke_entity_note(request, note_id, target_status):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        
        _request_user_id = Session_Key.objects.get_user_id(_session)
        _rslt = { 
            'note_id' : int(note_id) 
        }
        if target_status == '1':
            PokeEntityNoteTask.delay(note_id, _request_user_id)
            _rslt['poke_already'] = 1
        else:
            DepokeEntityNoteTask.delay(note_id, _request_user_id)
            _rslt['poke_already'] = 0
        return SuccessJsonResponse(_rslt)

@check_sign
def comment_entity_note(request, note_id):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        _comment_text = request.POST.get('comment', None)
        _reply_to_comment_id = request.POST.get('reply_to_comment', None)
        _reply_to_user_id = request.POST.get('reply_to_user', None)
        
        _request_user_id = Session_Key.objects.get_user_id(_session)
        
        _note = MobileNote(note_id)
        _comment_id = _note.add_comment(
            comment_text = _comment_text, 
            creator_id = _request_user_id, 
            reply_to_comment_id = _reply_to_comment_id,
            reply_to_user_id = _reply_to_user_id,
        )
        _context = _note.read_comment(_comment_id, _request_user_id)
        return SuccessJsonResponse(_context)

@check_sign
def delete_entity_note_comment(request, note_id, comment_id):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        DeleteEntityNoteCommentTask.delay(note_id, comment_id)
        return SuccessJsonResponse({ 'delete_already' : 1 })

