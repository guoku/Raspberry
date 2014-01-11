# coding=utf8
import random 

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
