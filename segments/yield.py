#!/usr/bin/python
#coding:utf-8   # correct
#coding : utf-8 # incorrect

def test_yield():
    a = 1
    print ('before yield')
    yield a
    ret = yield a #first next,it will stop on yield a, second next or send, it will continue from 'ret = 'sends values''
    print ('after yield, ret=', ret)

t1 = test_yield()
''' 可迭代对象
j=iter(t1) 
for i in j:
    print (i)
    break
print (j)
'''
#t1.next() which is not used in python2
next(t1)
t1.send('中文支持1 sending value to return')
t1.send('中文支持2 sending value to return')
t1.__next__()

'''
$chmod +x yield.py
===python3:
FeideMacBook-Pro:py feicheng$ python3 yield.py
before yield
after yield, ret= 中文支持2 sending value to return
Traceback (most recent call last):
  File "yield.py", line 16, in <module>
    t1.send('中文支持2 sending value to return')
StopIteration

===python2:
$./yield.py

FeideMacBook-Pro:py feicheng$ ./yield.py
before yield
('after yield, ret=', '\xe4\xb8\xad\xe6\x96\x87\xe6\x94\xaf\xe6\x8c\x812 sending value to return')
Traceback (most recent call last):
  File "./yield.py", line 15, in <module>
    t1.send('中文支持2 sending value to return')
StopIteration
'''
