#encoding=utf8

from mobile.lib.sign import check_sign 
from datetime import datetime
from lib.user import *
from lib.entity import *
from lib.note import *
from lib.tag import *
from mobile.lib.http import SuccessJsonResponse

def general_stat(request):
    if request.method == "GET":
        start = request.GET.get("time_begin")
        end = request.GET.get("time_end")
        start_time = datetime.fromtimestamp(int(start))
        end_time = datetime.fromtimestamp(int(end))

        uctmp = UserStats.new_user_count(start_time, end_time)
        user_count = uctmp[0]["count"]

        folltmp = UserStats.new_follow_count(start_time, end_time)
        follow_count = folltmp[0]["count"]

        enttmp = EntityStats.new_entity_count(start_time, end_time)
        entity_count = enttmp[0]["count"]

        liketmp = EntityStats.new_like_count(start_time, end_time)
        like_count = liketmp[0]["count"]

        notetmp = NoteStats.new_note_count(start_time, end_time)
        note_count = notetmp[0]["count"]

        poketmp = NoteStats.new_poke_count(start_time, end_time)
        poke_count = poketmp[0]["count"]

        commenttmp = NoteStats.new_note_comment(start_time, end_time)
        comment_count = commenttmp[0]["count"]
        
        tagtmp = TagStats.new_tag_count(start_time, end_time)
        tag_count = tagtmp[0]["count"]
        
        resp = {
            "user_count":user_count,
            "like_count":like_count,
            "entity_count":entity_count,
            "note_count":note_count,
            "poke_count":poke_count,
            "tag_count":tag_count,
            "follow_count":follow_count,
            "comment_count":comment_count
            }

        return SuccessJsonResponse(resp)


def feature_stat(request, feature = "user"):
    if request.method == "GET":
        group = request.GET.get("group")
        start = request.GET.get("time_begin")
        end = request.GET.get("time_end")
        start_time = datetime.fromtimestamp(int(start))
        end_time = datetime.fromtimestamp(int(end))

        feature = feature.lower()
        if feature == "user":
            user = UserStats.new_user_count(
                                        start_time,
                                        end_time,
                                        group = group
                                    )
            return SuccessJsonResponse(user)
        
        elif feature == "like":
            like = EntityStats.new_like_count(
                                    start_time,
                                    end_time,
                                    group = group
                                )
            return SuccessJsonResponse(like)

        elif feature == "follow":
            follow = UserStats.new_follow_count(
                                        start_time,
                                        end_time,
                                        group = group
                                    )
            return SuccessJsonResponse(follow)

        elif feature == "entity":
            entity = EntityStats.new_entity_count(
                                        start_time,
                                        end_time,
                                        group = group
                                    )
            return SuccessJsonResponse(entity)

        elif feature == "note":
            note = NoteStats.new_note_count(
                                        start_time,
                                        end_time,
                                        group = group
                                    )
            return SuccessJsonResponse(note)

        elif feature == "poke":
            poke = NoteStats.new_poke_count(start_time,end_time,group = group)
            return SuccessJsonResponse(poke)

        elif feature == "tag":
            tag = TagStats.new_tag_count(start_time, end_time, group = group)
            return SuccessJsonResponse(tag)
        else:
            comment = NoteStats.new_note_comment(
                                            start_time,
                                            end_time,
                                            group = group
                                        )
            return SuccessJsonResponse(comment)



