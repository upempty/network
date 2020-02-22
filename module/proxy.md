## 代理
user access http://www.google.com
=> user---->proxy------>http://www.google.com

user access http://www.google.com/abc
=> user---->proxy------>http://www.google.com/abc

user access http://www.google.com/def
=> user---->proxy------>http://www.google.com/def


## 方向代理
user access http://www.baidu.com
=> user--->virtual IP of (http://www.baidu.com)-->real server1

user access http://www.baidu.com/abc
=> user--->virtual IP of (http://www.baidu.com)-->real server2

user access http://www.baidu.com/def
=> user--->virtual IP of (http://www.baidu.com)-->real server3

