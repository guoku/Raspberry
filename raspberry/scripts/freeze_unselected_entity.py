import datetime
import MySQLdb


conn_gk = MySQLdb.Connection("localhost", "root", "123456", "guoku_11_21")
cur_gk = conn_gk.cursor()
cur_gk.execute("SET names utf8")


cur_gk.execute("select id from base_entity where weight >= 0 and id < 200000") 
entity_list = [] 
for row in cur_gk.fetchall():
    entity_id = row[0]
    entity_list.append(entity_id)


_tot = 0
for entity_id in entity_list:
    _note_count = 0
    _is_selected = False
    cur_gk.execute("select id, selected_time from base_note where entity_id=%d"%entity_id)
    for row in cur_gk.fetchall():
        _note_count += 1
        _note_id= row[0]
        _selected_time = row[1]
        if _selected_time != None:
            _is_selected = True

    if _note_count == 0 or _is_selected == False:
        _tot += 1
        print "UPDATE base_entity set weight=-1 where id=%d;"%entity_id
        #cur_gk.execute(_sql_query)
    
    

