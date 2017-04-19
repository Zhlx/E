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
from DataManager.models import Article,UserArticleBehavior

info=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if 'DataManager' in info:
    filename=info+'/stopwords.txt'
else:
    filename=info+'/DataManager/stopwords.txt'
f=open(filename,'r')
t=f.read().strip('\n')
stopwords=t.split()
f.close()

class Recommend:
    def get_recmd(self,id,type):
        texts1=self.get_behaviors(id,type)         #get user's behaviors
        if texts1==[]:
            print "user's behavior is null"
            if type=='Home':
                return_articles=Article.objects.all().order_by('?')[:20]
            else:
                return_articles=Article.objects.filter(articleType1=type).order_by('?')[:20]
            return return_articles
        else:
            print "user has behavior"
            if type=='Home':
                num=len(texts1)
                study=0
                news=0
                fun=0
                for i in texts1:
                    # ????
                    t=Article.objects.get(articleId=i).articleType1
                    if t=='Study':
                        study+=1
                    else:
                        if t=='News':
                            news+=1
                        else:
                            fun+=1
                s_num=(int)(1.0*study/num*20)
                n_num=(int)(1.0*news/num*20)
                f_num=(int)(1.0*fun/num*20)
                return_articles=[]
                return_articles.extend(Article.objects.filter(articleType1='Study').order_by('?')[0:s_num])
                return_articles.extend(Article.objects.filter(articleType1='News').order_by('?')[0:n_num])
                return_articles.extend(Article.objects.filter(articleType1='Fun').order_by('?')[0:f_num])
                return return_articles

            else:
                texts=[]
                articles=Article.objects.filter(articleType1=type)
                dict={}
                i=0
                for article in articles:
                    dict[i]=article.articleId
                    i+=1
                    l=article.articleEnglishText.lower().replace(','," ").replace('.'," ").replace('"'," ").split()
                    new_l=[word for word in l if word not in stopwords]
                    texts.append(new_l)
                dictionary=corpora.Dictionary(texts)
                corpus = [dictionary.doc2bow(text) for text in texts]
                tfidf=models.TfidfModel(corpus)
                corpus_tfidf = tfidf[corpus]
                lsi=models.LsiModel(corpus_tfidf,id2word=dictionary,num_topics=10)
                corpus_lsi=lsi[corpus_tfidf]
                index = similarities.MatrixSimilarity(lsi[corpus])
                simi=zeros((len(texts1),len(texts)))
                for i in range(len(texts1)):
                    query=texts[i]
                    query_bow=dictionary.doc2bow(query)
                    query_lsi=lsi[query_bow]
                    sims=index[query_lsi]
                    l=list(enumerate(sims))
                    for j in range(len(l)):
                        simi[i][l[j][0]]=l[j][1]
                simi1=zeros(len(texts))
                s1=numpy.array(simi1)
                for i in range(len(simi)):
                    s1+=numpy.array(simi[i])
                for i in s1:
                    i=i/len(texts1)
                simi1=s1
                d1={}
                for i in range(len(simi1)):
                    d1[dict[i]]=simi1[i]
                sorted_dict=sorted(d1.iteritems(),key=lambda x:x[1],reverse=True)
                return_articles=[]
                for i in range(20):
                    return_articles.append(Article.objects.get(articleId=sorted_dict[i][0]))
                return return_articles


    def get_behaviors(self,id,type):
        lists=UserArticleBehavior.objects.filter(user=id)

        if lists==[]:
            return []
        else:
            if type=='Home':
                return_list=[]
                for a in lists:
                    return_list.append(a.article.articleId)
                return return_list
            else:
                lists3=[]
                for a in lists:
                    if a.article.articleType1==type:
                        lists3.append(a)
                lists=lists3
                if lists==[]:
                    return []
                else:
                    texts=[]
                    for b in lists:
                        list=Article.objects.get(articleId=b.article).articleEnglishText.lower().replace(','," ").replace('.'," ").replace('"'," ").split()
                        new_list=[word for word in list if word not in stopwords]
                        texts.append(new_list)
                    return texts


# a=Recommend()
# a.get_recmd('1','Study')