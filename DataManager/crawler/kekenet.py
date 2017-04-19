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

class PatKekenetUrl:

    def getPageUrl(self, start, end, identifier):
        Http = []
        for i in range(start, end):
            http = 'http://www.kekenet.com/' + identifier + 'List_%s.shtml' % i
            Http.append(http)
        Http.append('http://www.kekenet.com/' + identifier)
        # print Http
        return Http

    def getText(self, start, end, identifier):
        page_list = self.getPageUrl(start, end, identifier)
        Text = []
        for page in page_list:
            text = urlopen(page).read()
            c = chardet.detect(text)
            code = c['encoding']
            # print code   # 查询网页的编码方式，code 为utf-8
            text = str(text).decode(code, 'ignore').encode('utf-8')
            # print text
            Text.append(text)
        return Text

    #获取每篇文章的url
    def getUrl(self, start, end, identifier):
        text_list = self.getText(start, end, identifier)
        Url = []
        for text in text_list:
            pattern1 = re.compile('<a href="http://www.kekenet.com/menu.*?shtml') #匹配文章url
            pattern2 = re.compile('<a href="http://www.kekenet.com/ielts.*?shtml')
            url_list = re.findall(pattern1, text)
            if url_list == []:
                url_list = re.findall(pattern2, text)
            for url in url_list:
                url = re.sub('<a href="', '', url)  #精简url
                # print url
                Url.append(url)
        return Url

class PatKekenet:

    def getText(self, url):
        text = urlopen(url).read()
        text = str(text).replace('\n', '')
        # c = chardet.detect(text)
        # code = c['encoding']
        # text = str(text).decode(code, 'ignore').encode('utf-8')
        text = text.replace('&amp;', '&').replace('&rsquo;', '\'').replace('&lsquo;', '\'').replace('&#39;', '\'')
        text = text.replace('&mdash;', '-').replace('&nbsp;', ' ').replace('&middot;', '--').replace('&quot;', '\"')
        text = text.replace('&ldquo;', '“').replace('&rdquo;', '”').replace('&ndash;', '-').replace('&rarr;', '→')
        text = text.replace('&hellip;', '……')
        # print text
        return text

    def getTitle(self, text):
        pattern_title = re.compile('<h1 id="nrtitle".*?</h1>')
        title = re.search(pattern_title, text)
        if title != None:
            title = title.group()
            title = re.sub('<.*?>', '', title)
        return title

    def getTime(self, text):
        pattern_time = re.compile('<time>.*?</time>')
        time = re.findall(pattern_time, text)
        for time in time:
            pattern_unuse = re.compile('<.*?>')
            time = re.sub(pattern_unuse, '', time).replace('时间:', '')
            time = re.sub('[0-9]{2}:[0-9]{2}:[0-9]{2}', '', time) #去除时分钟
            time = re.sub('[0-9]{2}:[0-9]{2}', '', time)
            # print time
        return time

    def getTag(self, text):
        pattern_tag = re.compile('<div class="sharebar">.*?</p>', re.S)
        tag = re.findall(pattern_tag, text)
        for tag in tag:
            pattern_unuse = re.compile('<.*?>')
            tag = re.sub(pattern_unuse, '', tag).strip()
            # print tag
            tag = tag.replace('关键字：', '')
        return tag

    def getSource(self):
        source = '可可英语'
        # print source
        return source

    def getCategoryOne(self):
        category_one = 'Study'
        # print category_one
        return category_one

    def getCategoryTwo(self, two):
        category_two = two
        # print category_two
        return category_two

    def getContent(self, two, text):
        English = ''
        Chinese = ''
        if two == 'IELTS':
            pattern = re.compile('<div id="article"><span id="article_eng">(.*?)单词详解')
            content = re.findall(pattern, text)
            # print content
            if content != []:
                content = re.sub('<span.*?>', ' ', content[0]).replace('<br />', '###')
                content = re.sub('<.*?>', '', content)
                content = re.sub(' {3,}', '', content)
                content = content.decode('utf-8')
                pattern_en = re.compile(u'(.*?)[\u4e00-\u9fa5]') # 知识点： 在unicode编码不能识别 \n
                content_en = re.findall(pattern_en, content)
                pattern_zg = content_en[0]
                content_zg = content.replace(pattern_zg, '') #为什么这里用sub不可以？
                English = content_en[0].encode('utf-8')
                English = English.replace('###', '\n')
                Chinese = content_zg.encode('utf-8')
                Chinese = Chinese.replace('###', '\n')
        else:
            pattern_en = re.compile('<div class="qh_en".*?</div>')
            pattern_zg = re.compile('<div class="qh_zg".*?</div>')
            content_en = re.findall(pattern_en, text)
            if content_en != []:
                for word in content_en:
                    word = re.sub('<.*?>', '', word)
                    English = English + word + ''
                content_zg = re.findall(pattern_zg, text)
                if content_zg != '':
                    for word in content_zg:
                        word = re.sub('<.*?>', '', word)
                        Chinese = Chinese + word + ''
            else:
                pattern = re.compile('<div id="article"><span id="article_eng">.*?</p>')
                content = re.findall(pattern, text)
                if content != []:
                    pattern_zg = re.compile('【.*?】')
                    content_zg = re.findall(pattern_zg, content[0])
                    if content_zg != []:
                        for word in content_zg:
                            word = re.sub('】', '', word).replace('【','')
                            Chinese = Chinese + word + ''
                        English = re.sub(pattern_zg, '', content[0]).replace('<br />', ' ')
                        English = re.sub('<.*?>', '', English)

        # print English
        # print Chinese
        if English != '' and Chinese != '' :
            dict = {'en':English, 'zg':Chinese}
        else:
            dict = {}
        return dict

    def getAll(self, id, url, two, text):
        content_dict = self.getContent(two, text)
        if content_dict != {}:
            title = self.getTitle(text)
            time = self.getTime(text)
            tag = self.getTag(text)
            source = self.getSource()
            category_one = self.getCategoryOne()
            category_two = self.getCategoryTwo(two)
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
            id = id + 1
        return id


# if __name__ == '__main__':
#     startnum = [1, 1, 2]
#     endnum = [5, 10, 3]
#     identifier_list = ['menu/13816/', 'menu/13504/', 'ielts/word/gushiyasi/']
#     catTwo = ['CET6', 'TOEFL', 'IELTS']
#     for i in range(0,len(startnum)):
#         a = PatKekenetUrl()
#         start = startnum[i]
#         end = endnum[i]
#         identifier = identifier_list[i]
#         total_url = a.getUrl()
#         # print len(total_url)
#         if total_url != []: #判断url列表是否为空，不为空执行下列动作
#             for url in total_url:
#                 b = PatKekenet()
#                 text = b.getText()
#                 # print b.getTitle()
#                 two = catTwo[i]
#                 b.getAll()


