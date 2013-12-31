import datetime
import MySQLdb

conn_gk = MySQLdb.Connection("localhost", "root", "123456", "guoku_12_09")
cur_gk = conn_gk.cursor()
cur_gk.execute("SET names utf8")

seed_users = {} 

cur_gk.execute("select user_id, count(*) as tot from guoku_entity_like group by user_id having tot > 2000;")
for row in cur_gk.fetchall():
    user_id = row[0]
    like_count = row[1]
    if not seed_users.has_key(user_id):
        seed_users[user_id] = {
            'like_count' : like_count,
            'poke_count' : 0,
            'fan_count' : 0
        }


cur_gk.execute("select followee_id, count(*) as tot from base_user_follow group by followee_id having tot > 20;")
for row in cur_gk.fetchall():
    user_id = row[0]
    fan_count = row[1]
    if not seed_users.has_key(user_id):
        seed_users[user_id] = {
            'like_count' : 0,
            'poke_count' : 0,
            'fan_count' : fan_count 
        }
    else:
        seed_users[user_id]['fan_count'] = fan_count

cur_gk.execute("select creator_id, count(*) as tot from base_note inner join base_note_poke on base_note.id=base_note_poke.note_id group by creator_id having tot > 30;")
for row in cur_gk.fetchall():
    user_id = row[0]
    poke_count = row[1]
    if not seed_users.has_key(user_id):
        seed_users[user_id] = {
            'like_count' : 0,
            'poke_count' : poke_count,
            'fan_count' : 0,
        }
    else:
        seed_users[user_id]['poke_count'] = poke_count 

print "DELETE FROM base_seed_user;"
for user_id, values in seed_users.items():
#    print "%d\t%d\t%d\t%d"%(user_id, values['like_count'], values['poke_count'], values['fan_count'])
    print "INSERT INTO base_seed_user SET user_id=%d, weight=0;"%user_id



