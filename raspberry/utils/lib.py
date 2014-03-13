# coding=utf8
import random 
import string

def roll(tot, num):
    if tot > num * 10:
        _rslt = []
        for i in range(0, num - 1):
            while True:
                k = random.randint(0, tot - 1)
                if not k in _rslt:
                    _rslt.append(k)
                    break
    else:
        _rslt = []
        for i in range(0, num - 1):
            _rslt.append(i)
    return _rslt

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_random_string(length, case_sensitive = False):
    s = ""
    charset = string.ascii_lowercase + string.digits
    if case_sensitive:
        charset = string.letters + string.digits
    for i in range(length):
        s += random.choice(charset)
    return s
