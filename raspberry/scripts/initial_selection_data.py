import sys
sys.path.append("..")
from base.selection import NoteSelection 
from mongoengine import connect
import datetime
import MySQLdb


_start_time = datetime.datetime.now()
if len(sys.argv) >= 6:
    mysql_host = sys.argv[1] 
    mysql_user = sys.argv[2] 
    mysql_password = sys.argv[3] 
    mysql_database = sys.argv[4] 
    mongo_database = sys.argv[5]
    mongo_host = sys.argv[6]
else:
    mysql_host = "localhost" 
    mysql_user = "root" 
    mysql_password = "123456" 
    mysql_database = "guoku_11_06_slim" 
    mongo_database = "guoku" 
    mongo_host = "localhost" 

connect(mongo_database, host = mongo_host)
conn = MySQLdb.Connection(mysql_host, mysql_user, mysql_password, mysql_database)
cur = conn.cursor()
cur.execute("SET names utf8")


cur.execute("SELECT id, group_id FROM base_neo_category;") 
neo_category_mapping = {}
for row in cur.fetchall():
    neo_category_id = row[0]
    group_id = row[1]
    neo_category_mapping[neo_category_id] = group_id


cur.execute("SELECT id, pid from base_category;") 
root_category_mapping = {}
for row in cur.fetchall():
    category_id = row[0]
    pid = row[1]
    if pid == 0:
        pid = category_id
    root_category_mapping[category_id] = pid

NoteSelection.drop_collection()
cur.execute("SELECT base_entity_note.note_id, base_entity_note.entity_id, base_entity_note.selector_id, base_entity_note.post_time, base_entity_note.selected_time, base_entity.category_id, base_entity.neo_category_id FROM base_entity_note INNER JOIN base_entity WHERE base_entity_note.selector_id is not NULL AND base_entity_note.entity_id=base_entity.id ORDER BY base_entity_note.post_time DESC LIMIT 20000;")
count = 0
for row in cur.fetchall():
    note_id = row[0]
    entity_id = row[1]
    selector_id = row[2]
    post_time = row[3]
    selected_time = row[4]
    category_id = row[5]
    neo_category_id = row[6]
    neo_category_group_id = neo_category_mapping[neo_category_id]
    root_category_id = root_category_mapping[category_id] 
    note_selection = NoteSelection( 
        selector_id = selector_id,
        selected_time = selected_time, 
        post_time = post_time,
        entity_id = entity_id,
        note_id = note_id,
        root_category_id = root_category_id,
        neo_category_id = neo_category_id,
        neo_category_group_id = neo_category_group_id,
        category_id = category_id 
    )
    note_selection.save()
    count += 1
conn.commit()
_end_time = datetime.datetime.now()
print "%d selections processed...%s"%(count, str(_end_time - _start_time))
