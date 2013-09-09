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
        print "INSERT INTO raspberry_category(id, pid, title, status) VALUES (%d, %d, %s, 1);"%(cid, pid, ttl)
        count += 1
        
        
        
