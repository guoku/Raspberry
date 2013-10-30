import MySQLdb

conn_rspy = MySQLdb.Connection('localhost', 'root', '123456', 'raspberry')
cur_rspy = conn_rspy.cursor()
cur_rspy.execute("SET names utf8")

conn_gk = MySQLdb.Connection('localhost', 'root', '123456', 'guoku_08_03_slim')
cur_gk = conn_gk.cursor()
cur_gk .execute("SET names utf8")


cur_rspy.execute("SELECT id, title from common_category;")
categories = {}
for row in cur_rspy.fetchall():
    for token in row[1].split('/'):
        if len(token) > 3:
            categories[token] = {
                'category_id' : row[0],
                'count' : 0
            }

cur_gk.execute("select base_entity.id, base_entity.title, base_entity_note.note_id from base_entity inner join base_entity_note on base_entity.id=base_entity_note.entity_id where base_entity_note.selected_time is not null;")
count = 0
for row in cur_gk.fetchall():
    entity_id = row[0]
    title = row[1]
    note_id = row[2]
    if title != None: 
        for category in categories.keys():
            if category in title:
                count += 1
                categories[category]['count'] += 1
                print "%d\t%d\t%d\t%s\t%s"%(entity_id, note_id, categories[category]['category_id'], category, title)

for category in categories.keys():
    print "%s\t%d\t%s"%(category, categories[category]['category_id'], categories[category]['count'])
print count


