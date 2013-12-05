# coding=utf-8
from mongoengine import *
from models import NoteSelection
from entity import Entity
import datetime

def _available_for_selection(selected, cand):
    i = len(selected) - 1
    while (i >= len(selected) - 3) and (i >= 0):
        if cand['root_category_id'] == selected[i]['root_category_id']:
            return False
        i -= 1
    return True

def arrange(select_count, start_time, interval_secs):
    _freezing_time = datetime.datetime(2099, 1, 1) 
    
    _selection_cands = []
    for _doc in NoteSelection.objects.filter(post_time__gt = _freezing_time).order_by("selected_time"):
        _selection_cands.append({
            'entity_id' : _doc.entity_id,
            'note_id' : _doc.note_id,
            'selector_id' : _doc.selector_id,
            'selected_time' : _doc.selected_time,
            'root_category_id' : _doc.root_category_id
        })
    
    _selected = []
    f = True
    while f:
        i = 0
        f = False
        while i < len(_selection_cands): 
            if _available_for_selection(_selected, _selection_cands[i]):
                _selection = _selection_cands.pop(i)
                _selected.append(_selection)
                
                f = True
                if len(_selected) >= select_count:
                    f = False
                    break
            else:
                i += 1
   
    _post_time = start_time
    for _selection in _selected:
        Entity(_selection['entity_id']).update_note_selection_info(
            note_id = _selection['note_id'],
            selector_id = _selection['selector_id'],
            selected_time = _selection['selected_time'],
            post_time = _post_time
        )
        _post_time += datetime.timedelta(seconds = interval_secs)
        print "[%s:%s] arraged @ [%s]"%(_selection['entity_id'], _selection['note_id'], _post_time)

