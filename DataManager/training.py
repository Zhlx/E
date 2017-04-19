#coding=utf-8
__author__ = 'root'
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','E.settings')
import django
django.setup()
import urllib2
import simplejson
from DataManager.models import Article,User
import re

server_url='http://192.168.235.118:8000/One/'
data={'userId':'3','style':'Home'}
data2=simplejson.dumps(data)
request = urllib2.Request(url=server_url,data=data2)

response = urllib2.urlopen(request)
get_response_string = response.read()
d=simplejson.loads(get_response_string)
print d
# a=d['data']
# for l in a:
#     print l.articleType

#
server_url='http://192.168.235.118:8000/getArticle/'
data={'userId':'965202810@qq','articleId':'201605224694'}
data2=simplejson.dumps(data)
request = urllib2.Request(url=server_url,data=data2)

response = urllib2.urlopen(request)
get_response_string = response.read()
d=simplejson.loads(get_response_string)
print d
#
# server_url='http://192.168.235.118:8000/Register/'
# data={'userId':'965202810@qq','password':'965202810@qq','userNickName':'hsuan'}
# data2=simplejson.dumps(data)
# request = urllib2.Request(url=server_url,data=data2)
#
# response = urllib2.urlopen(request)
# get_response_string = response.read()
# d=simplejson.loads(get_response_string)
# print d


#
# server_url='http://192.168.235.118:8000/Collect/'
# data={'userId':'965202810@qq','articleId':'1'}
# data2=simplejson.dumps(data)
# request = urllib2.Request(url=server_url,data=data2)
#
# response = urllib2.urlopen(request)
# get_response_string = response.read()
# d=simplejson.loads(get_response_string)


# server_url='http://192.168.235.118:8000/getCollect/'
# data={'userId':'123456789@163.com'}
# data2=simplejson.dumps(data)
# request = urllib2.Request(url=server_url,data=data2)
#
# response = urllib2.urlopen(request)
# get_response_string = response.read()
# d=simplejson.loads(get_response_string)
# print d
