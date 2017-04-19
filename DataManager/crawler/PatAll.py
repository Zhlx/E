__author__ = 'carrie'
#coding=utf-8
from aisi import PatBBCNewsUrl, PatBBCNews
from enread import PatJoke, PatJokeUrl
from hjenglish import PatHJ, PatHJUrl
from juren import PatJuren, PatJurenUrl
from kekenet import PatKekenetUrl, PatKekenet
from xiao_e import PatXE, PatXEUrl

class PatAll:

    def aisi(self, id):
        # 'BBC News',
        type_list = ['BBC News','Funny BBC']
        for type in type_list:
            # print type
            b = PatBBCNewsUrl()
            url_list = b.getTotalUrl(type)
            for url in url_list:
                g = PatBBCNews()
                # print url
                page = g.getPage(url)
                id = g.getAll(id, url, type, page)
        return id

    def enread(self, id):
        b = PatJokeUrl()
        url_list = b.getTotalUrl()
        # print len(url_list)
        for url in url_list:
            g = PatJoke()
            page = g.getPage(url)
            # print url
            id  = g.getAll(id, url, page)
        return id

    def HJ(self, id):
        a = PatHJUrl()
        dict = a.getUrl()
        url_list = dict['url']
        time_list = dict['time']
        for i in range(len(url_list)):
            url = url_list[i]
            # print url
            time = time_list[i]
            b = PatHJ()
            page = b.getPage(url)
            id = b.getAll(id, url, page, time)
        return id

    def juren(self, id):
        type_list = ['Daily', 'Travel']
        for type in type_list:
            b = PatJurenUrl()
            url_list = b.getTotalUrl(type)
            # print len(url_list)
            for url in url_list:
            # for i in range(120,len(url_list)):
            #     url = url_list[i]
                g = PatJuren()
            #     print url
                page = g.getPage(url)
                # g.getTag(page)
                id = g.getAll(id, url, page, type)
        return id

    def kekenet(self, id):
        startnum = [1, 1, 2]
        endnum = [5, 10, 3]
        identifier_list = ['menu/13816/', 'menu/13504/', 'ielts/word/gushiyasi/']
        catTwo = ['CET6', 'TOEFL',  'IELTS']
        for i in range(0,len(startnum)):
            a = PatKekenetUrl()
            start = startnum[i]
            end = endnum[i]
            identifier = identifier_list[i]
            total_url = a.getUrl(start, end, identifier)
            # print len(total_url)
            if total_url != []: #判断url列表是否为空，不为空执行下列动作
                for url in total_url:
                    b = PatKekenet()
                    text = b.getText(url)
                    # print b.getTitle()
                    two = catTwo[i]
                    id = b.getAll(id, url, two, text)
        return id

    def xiao_e(self, id):
        catone_list = ['Study', 'Fun']
        cattwo_list = ['CET4', 'Anecdotes']
        #
        for i in range(len(catone_list)):
            catone = catone_list[i]
            cattwo = cattwo_list[i]
            a = PatXEUrl()
            url_list = a.getURL(cattwo)
            print len(url_list)
            # for url in url_list:
            for i in range(len(url_list)):
                url = url_list[i]
                # print url
                b = PatXE()
                text = b.getText(url)
                id = b.getAll(id, url, text, cattwo, catone)
        return id

if __name__ == '__main__':
    a = PatAll()
    id = 1915
    # id  = a.aisi(id)   #661
    # id = a.enread(id)     #1113
    # id = a.HJ(id)       #77
    # id = a.juren(id)     #185
    id = a.kekenet(id)      #246
    id = a.xiao_e(id)        #229

