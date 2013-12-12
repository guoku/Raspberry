fi = open('cats_matching.txt', 'r')
for line in fi.readlines():
    tokens = line.strip().split('\t')
    taobao_category_id = tokens[0]
    neo_category_id = tokens[1]
    print "INSERT INTO base_taobao_item_neo_category_mapping SET taobao_category_id=%s, neo_category_id=%s;"%(taobao_category_id, neo_category_id)
