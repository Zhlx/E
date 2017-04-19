__author__ = 'carrie'
# coding=utf-8
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','E.settings')
import django
django.setup()
import re
import chardet
from urllib import urlopen
from DataManager.models import Article
# 爬取英语阅读网双语笑话1-55页的http，网页源代码以及每一页的url

class PatJokeUrl:

    def getHttp(self):
        Http = []
        for i in range(1, 57):
            http = 'http://www.enread.com/humors/shuangyu/list_%s.html' % i
            # print http
            Http.append(http)
        return Http

    def getText(self):
        total_url = self.getHttp()
        Text = []
        for total_url in total_url:
            # print total_url
            text = urlopen(total_url).read()
            c = chardet.detect(text)
            code = c['encoding']
            # print code   # 查询网页的编码方式，code 为utf-8
            text = str(text).decode(code, 'ignore').encode('utf-8')
            # print text
            Text.append(text)
        return Text

    def getTotalUrl(self):
        text = self.getText()
        Url = []
        for text in text:
            pattern1_url_list = re.compile('<h2>.*?</h2>')
            url_list = re.findall(pattern1_url_list, text)
            pattern2_url_list = re.compile('/humors.*?html')
            url_list = str(url_list)
            url_list = re.findall(pattern2_url_list, url_list)
            for url_list in url_list:
                url_list = 'http://www.enread.com'+url_list
                # print url_list
                Url.append(url_list)
        # print Url
        return Url

class PatJoke():

    def getPage(self, url):
        page = urlopen(url).read()
        charset = chardet.detect(page)
        cod = charset['encoding']
        # print(cod)
        page = str(page).decode(cod, 'ignore').encode("utf-8")
        page = str(page).replace('\r\n','')  # 为什么这里就不行 ？？？？
        page = page.replace('&quot;', '"').replace('&ldquo;', '“').replace('&rdquo;', '”').replace('&#39;','\'')
        page = page.replace('&rsquo;', '\'').replace('&lsquo;', '\'').replace('&nbsp;', '').\
            replace('&hellip;', '...').replace('&mdash;', '—').replace('&Prime;', '″')
        return page

    def getTitle(self, page):
        pattern_title = re.compile('<title>.*?</title>')
        title = re.findall(pattern_title, page)
        for title in title:
            pattern_unuse = re.compile('<.*?>')
            title = re.sub(pattern_unuse, '', str(title))
            title = title.replace('_英文阅读网', '')
            # print title
            return title

    def getTime(self, page):
        pattern_time = re.compile('发布时间.*?字体')
        time = re.findall(pattern_time, page)
        for time in time:
            time = time.replace('发布时间：', '').replace('字体', '').strip()
            time = re.sub('[0-9]{2}:[0-9]{2}', '', time)#去除时分钟
            # print time
        return time

    def getTag(self):
        return '笑话'

    def getSource(self):
        source = '英文阅读网'
        # print source
        return source

    def getCategoryOne(self):
        category_one = 'Fun'
        # print category_one
        return category_one

    def getCategoryTwo(self):
        category_two = 'Joke'
        # print category_two
        return category_two

    def getContent(self, page):
        pattern_content = re.compile('<div id="dede_content">.*?<div class="dede_pages">', re.S)
        content = re.findall(pattern_content, page)
        content_zg = ''
        content_en = ''
        for content in content:
            pattern_unuse = re.compile('<.*?>')
            content = content.replace('</div>', '###').replace('\n', '')
            content = re.sub(pattern_unuse, '', content)
            content = re.sub(" {3,}", '', content)  # 积累知识：  把三个或以上连续空格删去
            # print content
            content = content.decode('utf-8')
            english_list = re.findall(u'(.*?)[\u4e00-\u9fa5]', content) #找出英文
            if english_list != []:
                if len(english_list) == 1:
                    content_en = english_list[0]
                    content = re.sub(content_en, '', content)
                else:
                    for en in english_list:
                        if len(en) > 20:
                            en = en.replace(u'......”###', '').replace(u'？“###', '').replace(u'！”###','')
                            #避免中文中的标点符号被替换到英文中
                            # print en
                            content_en = content_en + en
                            content = content.replace(en, '')
                content_en = content_en.encode('utf-8')
                content_en = re.sub("#{3,}", '\n', content_en)
                content_zg = content.encode('utf-8')
                content_zg = re.sub("#{3,}", '\n', content_zg)
            # print content_en
            # print content_zg
        dict = {'en': content_en, 'zg': content_zg}
        return dict

    def getAll(self, id, url, page):
        content_dict = self.getContent(page)
        if content_dict['en'] != '':
            title = self.getTitle(page)
            time = self.getTime(page)
            tag = self.getTag()
            source = self.getSource()
            category_one = self.getCategoryOne()
            category_two = self.getCategoryTwo()
            content_en = content_dict['en']
            content_zg = content_dict['zg']
            picture = ''
            print 'id: ', id
            print 'url: ', url
            print 'title:', title
            print 'time: ', time
            print 'tag: ', tag
            print 'source: ', source
            print 'category_one: ', category_one
            print 'category_two: ', category_two
            print 'content_en: ', content_en
            print 'content_zg: ', content_zg
            print '\n'
            try:
                article=Article(articleId='20160522'+str(id).zfill(4),articleTitle=title,
                                articleSource=source,articleTag=tag,articleType1=category_one,
                                articleType2=category_two,articleDate=time,articleImgUrl=picture,
                                articleEnglishText=content_en,articleChineseText=content_zg)
                article.save()
            except:
                print 'create article faily'
            id  = id + 1
        return id

# if __name__ == '__main__':
#     b = PatJokeUrl()
#     url_list = b.getTotalUrl()
#     print len(url_list)
#     for url in url_list:
#         g = PatJoke()
#         page = g.getPage()
#         print url
#         # g.getTitle()
#         # g.getTime()
#         # g.getTag()
#         # g.getContent()
#         g.getAll()