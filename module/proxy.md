## 正向代理
### "代理" 为用户转递信息给服务器，并且根据服务的返回结果回复给用户。
user access http://www.google.com
=> user---->proxy------>http://www.google.com

user access http://www.google.com/abc
=> user---->proxy------>http://www.google.com/abc

user access http://www.google.com/def
=> user---->proxy------>http://www.google.com/def


## 方向代理
### "反向代理" 为访问的服务器进行重定向或负载均衡到实际到服务器端来完成数据到处理返回。
user access http://www.baidu.com
=> user--->virtual IP of (http://www.baidu.com)-->real server1

user access http://www.baidu.com/abc
=> user--->virtual IP of (http://www.baidu.com)-->real server2

user access http://www.baidu.com/def
=> user--->virtual IP of (http://www.baidu.com)-->real server3

