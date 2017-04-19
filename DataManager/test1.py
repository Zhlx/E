#coding=utf-8
__author__ = 'root'
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','E.settings')
import django
django.setup()
import jieba
import jieba.analyse
import math
import gensim
import numpy
from numpy import *
from gensim import corpora, models, similarities
from DataManager.models import Article,User,UserArticleBehavior
# import sys
# articles=Article.objects.all()
# for article in articles:
#     title=article.articleTitle
#     article.articleTitle=title.strip()
#     date=article.articleDate
#     article.articleDate=date.strip()
#     article.save()
# print 'ok'

# Article.objects.all().delete()

# info=os.getcwd()
# if 'DataManager' in info:
#     filename=info+'/stopwords.txt'
# else:
#     filename=info+'/DataManager/stopwords.txt'
# f=open(filename,'r')
# t=f.read().strip('\n')
# stopwords=t.split()
# f.close()
# def get_behaviors(id,type):
#     lists=UserArticleBehavior.objects.filter(user=id)
#
#     if lists==[]:
#         return []
#     else:
#         if type=='':
#             return_list=[]
#             for a in lists:
#                 return_list.append(a.article.articleId)
#             return return_list
#         else:
#             lists3=[]
#             for a in lists:
#                 if a.article.articleType1==type:
#                     lists3.append(a)
#             lists=lists3
#             if lists==[]:
#                 return []
#             else:
#                 texts=[]
#                 for b in lists:
#                     list=Article.objects.get(articleId=b.article).articleEnglishText.lower().replace(','," ").replace('.'," ").replace('"'," ").split()
#                     new_list=[word for word in list if word not in stopwords]
#                     texts.append(new_list)
#                 return texts
#
# behaviors=get_behaviors('1','Fun')
# print behaviors

# b=User.objects.get(userId='22')
# # b.userFavorite.add(Article.objects.get(articleId='8885'))
# b.userFavorite.remove(Article.objects.get(articleId='1'))
# a=b.userFavorite.all()
# print a
# print b
# try:
#     u=User.objects.get(userId='57684534')
# except:
#     print 'no this user'
#
# uab=UserArticleBehavior.objects.get(article=Article.objects.get(articleId='1'),
#                                               user=User.objects.get(userId='22'),
#
#                                               )
#
# uab.save()

# Article.objects.all().delete()
