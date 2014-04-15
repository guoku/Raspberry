import MySQLdb


conn = MySQLdb.Connection('localhost', 'root', '123456', 'guoku_02_11')
cur = conn.cursor()
cur.execute("SET names utf8")

cur.execute("SELECT user_id, tag from base_recommend_user_tag") 
recommend_tags = {}
for row in cur.fetchall():
    user_id = row[0]
    tag = row[1]
    if not recommend_tags.has_key(user_id):
        recommend_tags[user_id] = {}
    if not recommend_tags[user_id].has_key(tag):
        recommend_tags[user_id][tag] = None


cur.execute("select user_id, tag_text, last_tagged_time from base_entity_tag")
for row in cur.fetchall():
    user_id = row[0]
    tag = row[1]
    last_tagged_time = row[2]
    if recommend_tags.has_key(user_id):
        if recommend_tags[user_id].has_key(tag):
            if recommend_tags[user_id][tag] == None or last_tagged_time > recommend_tags[user_id][tag]:
                recommend_tags[user_id][tag] = last_tagged_time

for user_id, tags in recommend_tags.items():
    for tag, last_tagged_time in tags.items():
        sql_query = "UPDATE base_recommend_user_tag SET created_time='%s' WHERE user_id=%d and tag='%s';"%(last_tagged_time, user_id, tag)
        cur.execute(sql_query)
conn.commit()
