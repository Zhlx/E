from django.shortcuts import render
from django.http import HttpResponse
from models import User,Article,UserArticleBehavior
import simplejson,json
import re
from DataManager.recmd import Recommend
import math
import random
import os
# Create your views here.


# Study:CET4,CET6,TOEFL,IELTS
# Fun:Travel,Joke,Daily,Fashion,Anecdotes
# News:BBCNews,FunnyBBC
# ipAddress='http://139.129.33.178:8089'
ipAddress='http://192.168.235.118:8000'


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
def showImg(req,ID):
    art=Article.objects.get(articleId=ID)
    imgUrl=art.articleImgUrl
    if imgUrl=="":
        number=random.randint(0,22)
        imgUrl=BASE_DIR+'/DataManager/crawler/picture/default'+str(number)+'.jpg'
        print imgUrl
        img_data=open(imgUrl,"rb").read()
    else:
        img_data =open(BASE_DIR+'/DataManager/crawler'+imgUrl, "rb").read()

    return HttpResponse(img_data, imgUrl)

def getArticle(request):
    if request.method=='POST':
        data=simplejson.loads(request.body)
        try:
            article=Article.objects.get(articleId=data['articleId'])
            user=User.objects.get(userId=data['userId'])
            try:
                uab=UserArticleBehavior.objects.get(article=article,user=user)
            except:
                uab=UserArticleBehavior(article=article,user=user)
                uab.save()
            if uab.isGood==True:
                good='true'
            else:
                good='false'
            if uab.isCollected==True:
                collect='true'
            else:
                collect='false'
            dict={'articleChineseText':article.articleChineseText,
                  'articleEnglishText':article.articleEnglishText,
                  'isGood':good,'isCollected':collect}
            return_dict={'error_code':'0','reason':'return successfully','data':dict}

            return HttpResponse(simplejson.dumps(return_dict))
        except:

            return_dict={'error_code':'1','reason':'No corresponding data in database','data':[]}
            return HttpResponse(simplejson.dumps(return_dict))
    else:
        return HttpResponse(simplejson.dumps({'error_code':'1','reason':'NO POST!'}))

def One(request):
    if request.method=='POST':
        data=simplejson.loads(request.body)
        try:
            style=data['style']
            a=Recommend()
            if style=='Home' or style=='Study' or style=='News' or style=='Fun':
                articles=a.get_recmd(data['userId'],style)
                article_list=[]
                for article in articles:
                    dict={'articleId':article.articleId,'articleTitle':article.articleTitle,
                          'articleSource':article.articleSource,'articleDate':article.articleDate,
                          'articleImgUrl':'%s/showImg/%s/'%(ipAddress,article.articleId),
                          'articleType':article.articleType1}
                    # if article.articleImgUrl=='':
                    #     dict['articleImgUrl']=''
                    article_list.append(dict)
                return_dict={'error_code':'0','reason':'return successfully','data':article_list}

                return HttpResponse(simplejson.dumps(return_dict))

            else:
                articles=Article.objects.filter(articleType2=style).order_by('?')[:20]
                article_list=[]
                for article in articles:
                    dict={'articleId':article.articleId,'articleTitle':article.articleTitle,
                          'articleSource':article.articleSource,'articleDate':article.articleDate,
                          'articleImgUrl':'%s/showImg/%s/'%(ipAddress,article.articleId),
                          'articleType':article.articleType1}
                    # if article.articleImgUrl=='':
                    #     dict['articleImgUrl']=''
                    article_list.append(dict)
                return_dict={'error_code':'0','reason':'return successfully','data':article_list}

                return HttpResponse(simplejson.dumps(return_dict))


        except:

            return_dict={'error_code':'1','reason':'No corresponding data in database','data':[]}
            return HttpResponse(simplejson.dumps(return_dict))
    else:
        return HttpResponse(simplejson.dumps({'error_code':'1','reason':'NO POST!'}))

def Register(request):
    if request.method=='POST':
        data=simplejson.loads(request.body)
        try:
            user=User(userId=data['userId'],userNickName=data['userNickName'],password=data['password'])
            user.save()
            return_dict={'error_code':'0','reason':'create new user successfully'}
            return HttpResponse(simplejson.dumps(return_dict))
        except:
            return_dict={'error_code':'1','reason':'create new user unsuccessfully'}
            return HttpResponse(simplejson.dumps(return_dict))
    else:
        return HttpResponse(simplejson.dumps({'error_code':'1','reason':'NO POST!'}))

def Login(request):
    if request.method=='POST':
        data=simplejson.loads(request.body)
        print data
        try:
            user=User.objects.get(userId=data['userId'])
            if user.password==data['password']:
                return HttpResponse(simplejson.dumps({'error_code':0,'reason':'login successfully'}))
            else:
                return HttpResponse(simplejson.dumps({'error_code':1,'reason':'password is wrong'}))
        except:
            return HttpResponse(simplejson.dumps({'error_code':'1','reason':'no this user'}))

    else:
        return HttpResponse(simplejson.dumps({'error_code':'1','reason':'NO POST!'}))

def Good(request):
    if request.method=='POST':
        data=simplejson.loads(request.body)
        print data['userId']
        try:
            u=User.objects.get(userId=data['userId'])
            a=Article.objects.get(articleId=data['articleId'])
            uab=UserArticleBehavior.objects.get(user=u,article=a)
            uab.isGood=not uab.isGood
            uab.save()
            return HttpResponse(simplejson.dumps({'error_code':'0','reason':'click good successfully'}))
        except:
            return HttpResponse(simplejson.dumps({'error_code':'1','reason':'click good unsuccessfully'}))
    else:
        return HttpResponse(simplejson.dumps({'error_code':'1','reason':'NO POST!'}))

def Collect(request):
    if request.method=='POST':
        data=simplejson.loads(request.body)
        print data
        try:
            u=User.objects.get(userId=data['userId'])
            a=Article.objects.get(articleId=data['articleId'])
            uab=UserArticleBehavior.objects.get(user=u,article=a)
            uab.isCollected=not uab.isCollected
            uab.save()
            if uab.isCollected==True:
                u.userFavorite.add(a)
            else:
                u.userFavorite.remove(a)
            return HttpResponse(simplejson.dumps({'error_code':'0','reason':'click collect successfully'}))
        except:
            return HttpResponse(simplejson.dumps({'error_code':'1','reason':'click collect unsuccessfully'}))
    else:
        return HttpResponse(simplejson.dumps({'error_code':'1','reason':'NO POST!'}))

def getCollect(request):
    if request.method=='POST':
        data=simplejson.loads(request.body)
        print data
        try:
            u=User.objects.get(userId=data['userId'])
            print '1'
            articles=u.userFavorite.all()
            print '2'
            if articles==[]:
                print '3'
                return HttpResponse(simplejson.dumps({'error_code':'0','reason':'successfully','data':[]}))
            else:
                article_list=[]
                for article in articles:
                    dict={'articleId':article.articleId,'articleTitle':article.articleTitle,
                          'articleSource':article.articleSource,'articleDate':article.articleDate,
                          'articleImgUrl':'%s/showImg/%s/'%(ipAddress,article.articleId),
                          'articleType':article.articleType1}
                    # if article.articleImgUrl=='':
                    #     dict['articleImgUrl']=''
                    article_list.append(dict)
                return_dict={'error_code':'0','reason':'return successfully','data':article_list}
                print '4'
                return HttpResponse(simplejson.dumps(return_dict))
        except:
            return HttpResponse(simplejson.dumps({'error_code':'1','reason':'unsuccessfully','data':[]}))
    else:
        return HttpResponse(simplejson.dumps({'error_code':'1','reason':'NO POST!','data':[]}))

