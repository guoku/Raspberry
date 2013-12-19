# coding=utf8
from base.report import EntityReport, EntityNoteReport 
from lib.http import SuccessJsonResponse, ErrorJsonResponse
from lib.sign import check_sign
from mobile.models import Session_Key
import datetime


@check_sign
def report_entity(request, entity_id):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        if _session != None:
            _reporter_id = Session_Key.objects.get_user_id(_session)
        else:
            _reporter_id = -1

        _comment = request.POST.get('comment', '')
        _report = EntityReport(
            reporter_id = _reporter_id,
            comment = _comment,
            entity_id = int(entity_id),
            created_time = datetime.datetime.now(),
            updated_time = datetime.datetime.now(),
        )
        _report.save()
        return SuccessJsonResponse({ "status" : 1 })

            
@check_sign
def report_entity_note(request, note_id):
    if request.method == "POST":
        _session = request.POST.get('session', None)
        if _session != None:
            _reporter_id = Session_Key.objects.get_user_id(_session)
        else:
            _reporter_id = -1

        _comment = request.POST.get('comment', '')
        _report = EntityNoteReport(
            reporter_id = _reporter_id,
            comment = _comment,
            note_id = int(note_id),
            created_time = datetime.datetime.now(),
            updated_time = datetime.datetime.now(),
        )
        _report.save()
        return SuccessJsonResponse({ "status" : 1 })

            
