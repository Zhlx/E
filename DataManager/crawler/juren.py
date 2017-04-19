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


# 爬取 巨人英语网 Daily和Travel这两部分，其中，daily有540篇，travel有200篇
# 这个网站是中英混合在一起的，没有把中英分开

class PatJurenUrl:

    def getHttp(self, type):
        Http = []
        if type == 'Daily':
            for i in range(2, 3):
                http = 'http://yingyu.juren.com/yingyuxuexi/shenghuo/richang/index_%s.html' % i
                # print http
                Http.append(http)
        if type == 'Travel':
            for i in range(2, 22):   # 因为有一个title无法写进file，所以改了range，只能爬2-21页
                http = 'http://yingyu.juren.com/yingyuxuexi/shenghuo/lvyou/index_%s.html' % i
                # print http
                Http.append(http)
        return Http

    def getText(self, type):
        total_url = self.getHttp(type)
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

    def getTotalUrl(self, type):
        text = self.getText(type)
        Url = []
        for text in text:
            pattern1_url = re.compile('<h3>.*?</h3>')
            url_list = re.findall(pattern1_url, text)
            pattern2_url = re.compile('http.*?html')
            url_list = str(url_list)
            url_list = re.findall(pattern2_url, url_list)
            for url_list in url_list:
                # print url_list
                Url.append(url_list)
        # print Url
        return Url

class PatJuren():

    def getPage(self,url):
        page = urlopen(url).read()
        # print page
        page = str(page).replace('\n', '').replace('\r', '').replace('\t', '')
        page = page.replace('&amp;', '&').replace('&rsquo;', '\'').replace('&lsquo;', '\'')
        page = page.replace('&mdash;', '-').replace('&nbsp;', ' ').replace('&middot;', '--')
        page = page.replace('&ldquo;', '“').replace('&rdquo;', '”').replace('&ndash;', '-').replace('&rarr;', '→')
        page = page.replace('&hellip;', '……').replace('&#39;', '\'').replace('&quot;', '')
        # print page
        return page

    def getTitle(self, page):
        pattern_title = re.compile('<title>.*?</title>')
        title = re.findall(pattern_title, page)
        for title in title:
            pattern_unuse = re.compile('<.*?>')
            title = re.sub(pattern_unuse, '', str(title)).replace('_英语网', '')
            # print title
            return title

    def getTime(self, page):
        pattern_time = re.compile('<div class="text">.*?<span class="right">', re.S)
        time = re.findall(pattern_time, page)
        for time in time:
            pattern_unuse = re.compile('<.*?>')
            time = re.sub(pattern_unuse, '', time).strip()
            time = re.sub('[0-9]{2}:[0-9]{2}', '', time)#去除时分钟
            # print time
            return time

    def getTag(self, page):
        pattern_tag = re.compile('<div class="tag">.*?</div>', re.S)
        tag_list = re.findall(pattern_tag, page)
        tag = ''
        for content in tag_list:
            pattern = re.compile('<a.*?</a>', re.S)
            list = re.findall(pattern, content)
            for i in list:
                i = re.sub('<.*?>', '', i)
                tag = tag + i + ' '
        return tag.strip()

    def getSource(self):
        source = '巨人网英语'
        # print source
        return source

    def getCategoryOne(self):
        category_one = 'Fun'
        # print category_one
        return category_one

    def getCategoryTwo(self, type):
        category_two = type
        # print category_two
        return category_two

    def getContent(self, page):
        pattern_content = re.compile('<div class="mainContent">.*?<div class="aboutNews">', re.S)
        content = re.findall(pattern_content, page)
        # print content
        for content in content:
            content = content.replace('</p>', '\n')
            pattern_unuse1 = re.compile('<tbody>.*?</tbody>', re.S)  # 去掉多余的内容--广告
            pattern_unuse2 = re.compile('<div id="page">.*?</div>', re.S)  # 去掉多余的内容--1\2\3、下一页这些
            pattern_unuse3 = re.compile('<.*?>')
            content = re.sub(pattern_unuse1, '', content)
            content = re.sub(pattern_unuse2, '', content)
            content = re.sub(pattern_unuse3, '', content)
            content = content.replace('[Photo/IC]', '').replace('　　', '')
            content_en = content.strip()
            # print content_en
        count_letter = re.findall('[a-zA-Z]',content_en)
        if len(count_letter) <= 100:
            content_en = ''
        content_zg = ''
        dict = {'en': content_en, 'zg': content_zg}
        return dict

    def getAll(self, id, url, page, type):
        content_dict = self.getContent(page)
        if content_dict['en'] != '':
            title = self.getTitle(page)
            time = self.getTime(page)
            tag = self.getTag(page)
            source = self.getSource()
            category_one = self.getCategoryOne()
            category_two = self.getCategoryTwo(type)
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
            id = id +1
        return id

# if __name__ == '__main__':
#     type_list = ['Daily', 'Travel']
#     for type in type_list:
#         b = PatJurenUrl()
#         url_list = b.getTotalUrl()
#         print len(url_list)
#         for url in url_list:
#             g = PatJuren()
#         #     print url
#             page = g.getPage()
#         #     g.getTag()
#         #     g.getTime()
#         #     g.getTitle()
#         #     g.getContent()
#             g.getAll()