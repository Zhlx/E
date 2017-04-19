#coding=utf-8
__author__ = 'root'
import jieba
import jieba.analyse
import math

class ContentBasedRecommend:

    def get_news_words(self,m,address):
        news_words={}
        for d in range(1,m+1):
            news_words[str(d)]={}
            address1=address+'/%s.txt'%d
            f=open(address1,'r')
            text=f.read()
            f.close()
            for j in jieba.analyse.extract_tags(text,10,True):
                news_words[str(d)][j[0]]=j[1]
        return news_words

    def get_user_behave(self,url):
        user_behave={}
        f=open(url,'r')
        text=f.readlines()
        f.close()
        for i in range(1,len(text)):
            text[i]=text[i].strip().split(':')
            if text[i][0] not in user_behave.keys():
                user_behave[text[i][0]]=[]
            user_behave[text[i][0]].append(text[i][1])
        return user_behave

    def get_single_similarity(self,news1,news2,news_words):
        w=0
        w1=0
        w2=0
        for word1,weight1 in news_words[news1].items():
            w1+=weight1*weight1
            for word2,weight2 in news_words[news2].items():
                w2+=weight2*weight2
                if word1==word2:
                    w+=weight1*weight2
            similarity=w/(math.sqrt(w1)*math.sqrt(w2))
        return similarity

    def get_similarity(self,news_words):
        S={}
        for news1 in news_words.keys():
            S[news1]={}
            for news2 in news_words.keys():
                if news1==news2:
                    continue
                s=self.get_single_similarity(news1,news2,news_words)
                if s==0.0:
                    continue
                S[news1][news2]=s
        return S

    def single_recommend(self,user,user_behave,S,r_num=10,k=5):
        r={}
        for i in user_behave[user]:
            sor1=sorted(S[i].iteritems(),key=lambda x:x[1],reverse=True)
            if k>len(sor1):
                for j in range(len(sor1)):
                    c=sor1[j][0]
                    if c in user_behave[user]:
                        continue
                    if c not in r.keys():
                        r[c]=0
                    r[c]+=S[i][c]
            else:
                for j in range(k):
                    c=sor1[j][0]
                    if c in user_behave[user]:
                        continue
                    if c not in r.keys():
                        r[c]=0
                    r[c]+=S[i][c]
        sor=sorted(r.iteritems(),key=lambda x:x[1],reverse=True)
        rec={}
        if r_num>len(sor):
            for x in range(len(sor)):
                rec[sor[x][0]]=sor[x][1]
        else:
            for x in range(r_num):
                rec[sor[x][0]]=sor[x][1]
        return rec

    def recommend(self,m,address,url,r_num=10,k=5):
        recom={}
        news_words=self.get_news_words(m,address)
        user_behave=self.get_user_behave(url)
        S=self.get_similarity(news_words)
        for i in user_behave.keys():
            recom[i]=self.single_recommend(i,user_behave,S)
        return recom

# m=500
# address='/home/zlx/下载/news/dataset'
# url='/home/zlx/下载/news/user_behave.txt'
# r=ContentBasedRecommend()
# recom=r.recommend(m,address,url)
# print recom['1']
