#encoding=utf-8
__author__ = 'root'

import jieba
from jieba import analyse
from gensim import similarities,models,corpora
import numpy
from numpy import *

class Similarity:

    def getDate(self,fileName):
        f=open(fileName,'r')
        lines=f.readlines()
        f.close()
        d={}
        for i in range(len(lines)):
            record=lines[i].split(':')
            b=record[1].split('``')
            d[record[0]]=b[0:len(b)-1]
        return d

    def getTag(self,fileName):
        d=self.getDate(fileName)
        tag={}
        for s in d.keys():
            tag[s]=[]
            for b in d[s]:
                bTag=jieba.cut(b,cut_all=False)
                tag[s].extend(bTag)
            for j in tag[s]:
                if j==' 'or j=='.':
                    tag[s].remove(j)
        return tag


    def getSi(self,fileName):
        tag=self.getTag(fileName)
        sT={}
        i=0
        texts=[]
        for key in tag.keys():
            sT[i]=key
            i+=1
            texts.append(tag[key])
        dictionary=corpora.Dictionary(texts)
        corpus=[dictionary.doc2bow(text)for text in texts]
        tfidf=models.TfidfModel(corpus)
        corpus_tfidf=tfidf[corpus]
        lsi=models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=20)
        corpus_lsi = lsi[corpus_tfidf]
        index=similarities.MatrixSimilarity(lsi[corpus])
        simi=zeros((len(texts),len(texts)))
        for i in range(len(texts)):
            query=texts[i]
            query_bow=dictionary.doc2bow(query)
            query_lsi=lsi[query_bow]
            sims=index[query_lsi]
            l=list(enumerate(sims))
            for j in range(len(l)):
                simi[i][l[j][0]]=l[j][1]
        return sT,simi



s=Similarity()
sT,simi=s.getSi('2012student_record.txt')
print sT
for i in range(len(simi)):
    print simi[i]