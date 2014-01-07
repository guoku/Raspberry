import datetime
import MySQLdb

conn_gk = MySQLdb.Connection("localhost", "root", "123456", "guoku_12_12")
cur_gk = conn_gk.cursor()
cur_gk.execute("SET names utf8")


fi = open('jump_log_12_31.txt', 'r')
fo = open('jump_log_12_31_analyzed.txt', 'w')
#fo.write("ID\tTBID\tCNT\tBND\tTTL\tLKE\tNTE\t\n")
for line in fi.readlines():
    tokens = line.strip().split('\t')
    entity_id = tokens[0]
    taobao_id = tokens[1]
    jump_count = tokens[2]
    if int(jump_count) < 100:
        break
    fo.write("%s\t%s\t%s"%(entity_id, taobao_id, jump_count))
    
    try:
        sql_query = "SELECT brand, title, category_id, neo_category_id, like_count, price from base_entity where id=%s;"%entity_id
        cur_gk.execute(sql_query)
        row = cur_gk.fetchone()
        brand = row[0]
        title = row[1]
        category_id = row[2]
        neo_category_id = row[3]
        like_count = row[4]
        price = row[5]
        
        sql_query = "SELECT title from base_category where id=%d;"%category_id
        cur_gk.execute(sql_query)
        row = cur_gk.fetchone()
        category_title = row[0]
        
        sql_query = "SELECT title from base_neo_category where id=%d;"%neo_category_id
        cur_gk.execute(sql_query)
        row = cur_gk.fetchone()
        neo_category_title = row[0]
        
        fo.write("\t%s\t%s\t%s\t%s\t%d\t%s"%(brand, title, category_title, neo_category_title, like_count, price))
    except:
        fo.write("\t-\t-\t-")
    
    try:
        sql_query = "SELECT COUNT(*) from base_note where entity_id=%s;"%entity_id
        cur_gk.execute(sql_query)
        row = cur_gk.fetchone()
        fo.write("\t%d"%row[0])
    except:
        fo.write("\t-")
    
    try:
        sql_query = "SELECT post_time, poke_count from base_note where entity_id=%s AND selector_id is not NULL;"%entity_id
        cur_gk.execute(sql_query)
        row = cur_gk.fetchone()
        post_time = row[0]
        poke_count = row[1]
        fo.write("\t%s\t%d"%(post_time, poke_count))
    except:
        fo.write("\t-\t-")

    fo.write("\n")
    
fi.close()
fo.close()


#print "DATE\tUSR\tENTY\tCRWL\tSLC\tLKE\tTAG\tNTE\tCMNT\tPOKE"
#for i in range(0, 30):
#    start_time = datetime.datetime.now() - datetime.timedelta(hours = 24 * (30 - i))
#    end_time = datetime.datetime.now() - datetime.timedelta(hours = 24 * (29 - i))
#    
#    sql_query = "SELECT count(*) FROM auth_user WHERE date_joined > '%s' AND date_joined < '%s'"%(start_time, end_time)
#    cur_gk.execute(sql_query)
#    user_count_delta = cur_gk.fetchone()[0]
#    
#    sql_query = "SELECT count(*) FROM base_entity WHERE creator_id is not NULL AND created_time > '%s' AND created_time < '%s'"%(start_time, end_time)
#    cur_gk.execute(sql_query)
#    entity_count_delta = cur_gk.fetchone()[0]
#    
#    sql_query = "SELECT count(*) FROM base_entity WHERE creator_id is NULL AND created_time > '%s' AND created_time < '%s'"%(start_time, end_time)
#    cur_gk.execute(sql_query)
#    entity_crawler_count_delta = cur_gk.fetchone()[0]
#    
#    sql_query = "SELECT count(*) FROM base_note WHERE post_time > '%s' AND post_time < '%s'"%(start_time, end_time)
#    cur_gk.execute(sql_query)
#    selection_count_delta = cur_gk.fetchone()[0]
#    
#    sql_query = "SELECT count(*) FROM guoku_entity_like WHERE created_time > '%s' AND created_time < '%s'"%(start_time, end_time)
#    cur_gk.execute(sql_query)
#    like_count_delta = cur_gk.fetchone()[0]
#    
#    sql_query = "SELECT count(*) FROM base_entity_tag WHERE created_time > '%s' AND created_time < '%s'"%(start_time, end_time)
#    cur_gk.execute(sql_query)
#    tag_count_delta = cur_gk.fetchone()[0]
#    
#    sql_query = "SELECT count(*) FROM base_note WHERE created_time > '%s' AND created_time < '%s'"%(start_time, end_time)
#    cur_gk.execute(sql_query)
#    note_count_delta = cur_gk.fetchone()[0]
#    
#    sql_query = "SELECT count(*) FROM base_note_comment WHERE created_time > '%s' AND created_time < '%s'"%(start_time, end_time)
#    cur_gk.execute(sql_query)
#    comment_count_delta = cur_gk.fetchone()[0]
#    
#    sql_query = "SELECT count(*) FROM base_note_poke WHERE created_time > '%s' AND created_time < '%s'"%(start_time, end_time)
#    cur_gk.execute(sql_query)
#    poke_count_delta = cur_gk.fetchone()[0]
#
#    print "%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d"%(i - 30, user_count_delta, entity_count_delta, entity_crawler_count_delta, selection_count_delta, like_count_delta, tag_count_delta, note_count_delta, comment_count_delta, poke_count_delta)
#
#sql_query = "SELECT count(*) FROM auth_user"
#cur_gk.execute(sql_query)
#user_count = cur_gk.fetchone()[0]
#
#sql_query = "SELECT count(*) FROM base_entity WHERE creator_id is not NULL"
#cur_gk.execute(sql_query)
#entity_count = cur_gk.fetchone()[0]
#
#sql_query = "SELECT count(*) FROM base_entity WHERE creator_id is NULL"
#cur_gk.execute(sql_query)
#entity_crawler_count = cur_gk.fetchone()[0]
#
#sql_query = "SELECT count(*) FROM base_note"
#cur_gk.execute(sql_query)
#selection_count = cur_gk.fetchone()[0]
#
#sql_query = "SELECT count(*) FROM guoku_entity_like"
#cur_gk.execute(sql_query)
#like_count = cur_gk.fetchone()[0]
#
#sql_query = "SELECT count(*) FROM base_entity_tag"
#cur_gk.execute(sql_query)
#tag_count = cur_gk.fetchone()[0]
#
#sql_query = "SELECT count(*) FROM base_note"
#cur_gk.execute(sql_query)
#note_count = cur_gk.fetchone()[0]
#
#sql_query = "SELECT count(*) FROM base_note_comment"
#cur_gk.execute(sql_query)
#comment_count = cur_gk.fetchone()[0]
#
#sql_query = "SELECT count(*) FROM base_note_poke"
#cur_gk.execute(sql_query)
#poke_count = cur_gk.fetchone()[0]
#
#print "TOT\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d"%(user_count, entity_count, entity_crawler_count, selection_count, like_count, tag_count, note_count, comment_count, poke_count)
#
#cur_gk.execute("SELECT gender, COUNT(*) FROM base_user_profile GROUP BY gender;")
#print "\nGENDER\tCOUNT"
#for row in cur_gk.fetchall():
#    gender = row[0]
#    count = row[1]
#    print "%s\t%d"%(gender, count)
#
#start_time = datetime.datetime.now() - datetime.timedelta(hours = 24 * 30)
#sql_query = "select count(*) from ( select user_id, count(*) as tot from guoku_entity_like where created_time > '%s' group by user_id having tot > 20 ) AS tmp;"%start_time
#cur_gk.execute(sql_query)
#like_20_user_count = cur_gk.fetchone()[0]
#print "\nIn [%s - %s]\nthere are %d user with more than 20 like count"%(start_time, datetime.datetime.now(), like_20_user_count) 
#
#print "\nTop like user:"
#sql_query = "select user_id, count(*) as tot from guoku_entity_like where created_time > '%s' group by user_id order by tot desc;"%(start_time)
#cur_gk.execute(sql_query)
#user_like_list = [] 
#for row in cur_gk.fetchall():
#    user_id = row[0]
#    like_count = row[1]
#    user_like_list.append({
#        'user_id' : user_id,
#        'like_count' : like_count
#    })
#    if len(user_like_list) > 100:
#        break
#
#for user in user_like_list:
#    cur_gk.execute("SELECT nickname from base_user_profile where user_id=%d;"%user['user_id'])
#    nickname = cur_gk.fetchone()[0]
#    cur_gk.execute("SELECT screen_name from base_sina_token where user_id=%d;"%user['user_id'])
#    try:
#        sina_screen_name = cur_gk.fetchone()[0]
#    except:
#        sina_screen_name = '-'
#    cur_gk.execute("SELECT date_joined from auth_user where id=%d;"%user['user_id'])
#    date_joined = cur_gk.fetchone()[0]
#    print "%d\t%s\t%d\t%s\t%s"%(user['user_id'], nickname, user['like_count'], sina_screen_name, date_joined)
#
#
#print "\nTop note user:"
#sql_query = "select creator_id, count(*) as tot from base_note where created_time > '%s' group by creator_id order by tot desc;"%(start_time)
#cur_gk.execute(sql_query)
#user_note_list = [] 
#for row in cur_gk.fetchall():
#    user_id = row[0]
#    note_count = row[1]
#    user_note_list.append({
#        'user_id' : user_id,
#        'note_count' : note_count
#    })
#    if len(user_note_list) > 100:
#        break
#
#for user in user_note_list:
#    cur_gk.execute("SELECT nickname from base_user_profile where user_id=%d;"%user['user_id'])
#    nickname = cur_gk.fetchone()[0]
#    cur_gk.execute("SELECT screen_name from base_sina_token where user_id=%d;"%user['user_id'])
#    try:
#        sina_screen_name = cur_gk.fetchone()[0]
#    except:
#        sina_screen_name = '-'
#    cur_gk.execute("SELECT date_joined from auth_user where id=%d;"%user['user_id'])
#    date_joined = cur_gk.fetchone()[0]
#    print "%d\t%s\t%d\t%s\t%s"%(user['user_id'], nickname, user['note_count'], sina_screen_name, date_joined)
#
#print "\nTop poke user:"
#sql_query = "select user_id, count(*) as tot from base_note_poke where created_time > '%s' group by user_id order by tot desc;"%(start_time)
#cur_gk.execute(sql_query)
#user_poke_list = [] 
#for row in cur_gk.fetchall():
#    user_id = row[0]
#    poke_count = row[1]
#    user_poke_list.append({
#        'user_id' : user_id,
#        'poke_count' : poke_count
#    })
#    if len(user_poke_list) > 100:
#        break
#
#for user in user_poke_list:
#    cur_gk.execute("SELECT nickname from base_user_profile where user_id=%d;"%user['user_id'])
#    nickname = cur_gk.fetchone()[0]
#    cur_gk.execute("SELECT screen_name from base_sina_token where user_id=%d;"%user['user_id'])
#    try:
#        sina_screen_name = cur_gk.fetchone()[0]
#    except:
#        sina_screen_name = '-'
#    cur_gk.execute("SELECT date_joined from auth_user where id=%d;"%user['user_id'])
#    date_joined = cur_gk.fetchone()[0]
#    print "%d\t%s\t%d\t%s\t%s"%(user['user_id'], nickname, user['poke_count'], sina_screen_name, date_joined)
