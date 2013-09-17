fi = open('category.txt', 'r')
count = 1
pid = None
for line in fi.readlines():
    line = line.strip()
    if line == '#':
        pid = pttl = None
    else:
        if pid == None:
            pid = count
        cid = count
        ttl = line
        if pid == cid:
            level = 1
        else:
            level = 2
        print "INSERT INTO common_category(id, pid, title, level, status) VALUES (%d, %d, '%s', %d, 1);"%(cid, pid, ttl, level)
        count += 1
        
        
        
