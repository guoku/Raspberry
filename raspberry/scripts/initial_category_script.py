fi = open('category.txt', 'r')
i_group = 1
i_cat = 1
gtitle = None
clist = []
for line in fi.readlines():
    line = line.strip()
    if line == '#':
        print "INSERT INTO common_category_group(id, title, status) VALUES (%d, '%s', 1);"%(i_group, gtitle)
        for title in clist: 
            print "INSERT INTO common_category(id, group_id, title, status) VALUES (%d, %d, '%s', 1);"%(i_cat, i_group, title)
            i_cat += 1
        i_group += 1
        gtitle = None
        clist = []
    else:
        if gtitle == None:
            gtitle = line
        else:   
            clist.append(line)
        
        
