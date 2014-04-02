import MySQLdb
import datetime


fo = open('guoku_click_log_2013.arff', 'w')
fo.write('@relation guoku_click_log_2013\n\n') 

fo.write('@attribute price NUMERIC\n')
for i in range(1, 13):
    fo.write('@attribute is_c%d {false,true}\n'%i)
for i in range(1, 42):
    fo.write('@attribute is_nc%d {false,true}\n'%i)
fo.write('@attribute click NUMERIC\n')




#sql_query = "select price, category_id, category_parent_id, neo_category_id, neo_category_group_id"
#cur.execute(sql_query)
#for row in cur.fetchall():
#    price = row[0]
#    category_id = row[1]
#    category_parent_id = row[2]
#    neo_category_id = row[3]
#    neo_category_group_id = row[4]
#conn.commit()

fo.close() 


