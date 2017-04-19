__author__ = 'carrie'
# coding=utf-8
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','E.settings')
import django
django.setup()
import re
import urllib2
from urllib import urlretrieve
from DataManager.models import Article
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}


class PatHJUrl:

    def getHttp(self):
        Http = []
        Http.append('http://www.hjenglish.com/new/tag/')
        for i in range(2, 6):
            http = 'http://www.hjenglish.com/new/tag/page%s/'% i
            Http.append(http)
            # print http
        return Http

    def getText(self):
        Text = []
        Http = self.getHttp()
        # content = u'时尚潮流/'
        # content = content.encode('utf-8')
        # content = urllib2.quote(content)
        for http in Http:
            http = http + '%E6%97%B6%E5%B0%9A%E6%BD%AE%E6%B5%81/'
            # print http
            request = urllib2.Request(url=http, headers= headers)  #积累知识 对于反爬虫的网站
            text = urllib2.urlopen(request).read()
            # text = urllib2.urlopen(http).read() #这个不行
            # print text
            text = str(text).replace('\r\n', '')
            Text.append(text)
        return Text

    def getUrl(self):
        Text = self.getText()
        Url = []
        Time = []
        for text in Text:
            text = re.findall('<ul id="article_list">.*?<!--end: main_article_list -->', text)
            if text != []:
                pattern = re.compile('<span class="green">(.*?)，')
                time_list = re.findall(pattern, text[0])
                url_list = re.findall('http://www.hjenglish.com/new/p[0-9]+/', text[0])
                # print url_list
                if url_list != []:
                    Url = Url + url_list
                if time_list != []:
                    Time = Time + time_list
        return {'url':Url, 'time':Time}


class PatHJ:

    def getPage(self, url):
        request = urllib2.Request(url=url, headers=headers)
        page = urllib2.urlopen(request).read()
        page = str(page).replace('\r\n', '')
        page = page.replace('&amp;', '&').replace('&rsquo;',"'").replace('&lsquo;',"'")
        page = page.replace('&mdash;', '-').replace('&nbsp;', ' ').replace('&middot;', '--')
        page = page.replace('&ldquo;', '“').replace('&rdquo;', '”').replace('&ndash;', '-').replace('&rarr;', '→')
        page = page.replace('&hellip;', '……').replace('&apos;',"'").replace('&bull;', '•').replace('&quot;','“')
        page = page.replace('&#39;', "'")
        return page

    def getTitle(self, page):
        title = re.findall('<div class="page_title">(.*?)</div>', page)
        if title != []:
            return title[0]
        else:
            return ''

    def getTime(self, time):
        time = re.sub('[0-9]{2}:[0-9]{2}:[0-9]{2}', '', time) #去除时分钟
        time = re.sub('[0-9]{2}:[0-9]{2}', '', time)
        return time

    def getTag(self, page):
        pattern = re.compile('<input type="hidden" id="articleTag" value="(.*?)" />')
        tag = re.findall(pattern, page)
        if tag != []:
            tag = tag[0].replace('|', ' ')
            return tag
        else:
            return '时尚潮流'

    def getSource(self):
        source = '沪江英语网'
        # print source
        return source

    def getCategoryOne(self):
        category_one = 'Fun'
        # print category_one
        return category_one

    def getCategoryTwo(self):
        category_two = 'Fashion'
        # print category_two
        return category_two

    def getContent(self, page):
        content_en = ''
        content_zg = ''
        # picture = re.findall('http://i[0-9]+.w.yun.hjfile.cn/doc/.*?jpg', page)
        # print len(picture)
        # if len(picture) >= 1 and len(picture) <= 3:
        pattern_en = re.compile('<div class="langs_en">(.*?)</div>')
        pattern_zg = re.compile('<div class="langs_cn">(.*?)</div>')
        en_list = re.findall(pattern_en, page)
        zg_list = re.findall(pattern_zg, page)
        for en in en_list:
            en = re.sub('<span>.*?</span>', '', en)
            en = re.sub('<.*?>','', en)
            content_en = content_en + en + '\n'
        for zg in zg_list:
            zg = re.sub('<span>.*?</span>', '', zg)
            zg = re.sub('<.*?>','', zg)
            content_zg = content_zg + zg + '\n'
        if content_en == '':
            content = re.findall('<div class="main_article">.*?<div class="main_article_icon">', page)
            if content != []:
                content = re.sub('<span.*?</span>', '', content[0]).replace('</p>', '###')\
                    .replace('<br />', '###')
                content = re.sub('<.*?>','',content)
                content = content.decode('utf-8')
                content_list = re.split(u'###', content)
                for content in content_list:
                    if len(re.findall(u'[\u4e00-\u9fa5]', content)) < 5:
                        content_en = content_en + content + u'###'
                    else:
                        content_zg = content_zg + content + u'###'
                content_zg = content_zg.replace(u'一页显示全部                提示：使用键盘键 ← →切换',u'')
                content_en = content_en.encode('utf-8')
                content_en = re.sub("#{3,}", '\n', content_en)
                content_zg = content_zg.encode('utf-8')
                content_zg = re.sub("#{3,}", '\n', content_zg)
                content_en = re.sub(' {3,}\n','',content_en)
        # print len(content_en)
        return {'en': content_en, 'zg':content_zg}

    def getPicture(self, page, id):
        picture = ''
        save_path = ''
        pic = re.findall('<div class="ad-thumbs">.*?</div>', page)
        if pic!= []:
            pic = re.findall('http.*?jpg', pic[0])
            picture = pic[0]
        else:
            pic = re.findall('http://i2.w.yun.hjfile.cn/doc/20.*?jpg', page)
            if pic != []:
                picture = pic[0]
            else:
                pic = re.findall('http://i1.w.hjfile.cn/doc/20.*?jpg', page)
                if pic != []:
                    picture = pic[0]
        if picture != '':
            save_path = './picture/' + str(id) + '.jpg'
            urlretrieve(picture,save_path)
            save_path='/picture/' + str(id) + '.jpg'
        return save_path

    def getAll(self, id, url, page, time):
        content_dict = self.getContent(page)
        if (content_dict['en'] != '') and (len(content_dict['en'])>30):
            title = self.getTitle(page)
            time = self.getTime(time)
            tag = self.getTag(page)
            source = self.getSource()
            category_one = self.getCategoryOne()
            category_two = self.getCategoryTwo()
            content_en = content_dict['en']
            content_zg = content_dict['zg']
            picture = self.getPicture(page, id)
            print 'id: ', id
            print 'url: ', url
            print 'title: ', title
            print 'time: ', time
            print 'tag: ', tag
            print 'source: ', source
            print 'category_one: ', category_one
            print 'category_two: ', category_two
            print 'content_en: ', content_en
            print 'content_zg: ', content_zg
            print 'picture: ', picture
            print '\n'
            try:
                article=Article(articleId='20160522'+str(id).zfill(4),articleTitle=title,
                                articleSource=source,articleTag=tag,articleType1=category_one,
                                articleType2=category_two,articleDate=time,articleImgUrl=picture,
                                articleEnglishText=content_en,articleChineseText=content_zg)
                article.save()
            except:
                print 'create article faily'
            id = id + 1
        return id




















