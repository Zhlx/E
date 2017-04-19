# coding=utf-8
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','E.settings')
import django
django.setup()
import re
import chardet
from urllib import urlopen, urlretrieve
from DataManager.models import Article


class PatBBCNewsUrl:

    def getHttp(self, type):
        Http = []
        if type == 'BBC News':
            for i in range(1, 13):
                if i<10:
                    http = 'http://www.24en.com/bbc-world-news/20150%s/' % i
                else:
                    http = 'http://www.24en.com/bbc-world-news/2015%s/' % i
                # print http
                Http.append(http)
        if type == 'Funny BBC':
            for i in range(2, 5):  # range改了
                http = 'http://www.24en.com/bbc/bbc2/index_%s.html' % i
                # print http
                Http.append(http)
        return Http

    def getText(self,type):
        total_url = self.getHttp(type)
        Text = []
        for url in total_url:
            text = urlopen(url).read()
            c = chardet.detect(text)
            code = c['encoding']
            text = str(text).decode(code, 'ignore').encode('utf-8')
            Text.append(text)
        return Text

    def getTotalUrl(self, type):
        text = self.getText(type)
        Url = []
        if type == 'BBC News':
            for text in text:
                pattern1_url = re.compile('<div class="cnt_list">.*?<!-- TAOBAO JS-->', re.S)
                url_list = re.findall(pattern1_url, text)
                pattern2_url = re.compile('http://www.24en.com/bbc-world-news/.*?\.html')
                url_list = re.findall(pattern2_url, str(url_list))
                for url_list in url_list:
                    # print url_list
                    Url.append(url_list)
        if type == 'Funny BBC':
            for text in text:
                pattern1_url = re.compile('<li><a title.*?href.*?</a></li>')
                url_list = re.findall(pattern1_url, text)
                pattern2_url = re.compile('http.*?html')
                url_list = re.findall(pattern2_url, str(url_list))
                for url_list in url_list:
                    # print url_list
                    Url.append(url_list)
        # print len(Url)
        return Url

class PatBBCNews():

    def getPage(self,url):
        page = urlopen(url).read()
        charset = chardet.detect(page)
        cod = charset['encoding']
        # print(cod)
        page = str(page).decode(cod, 'ignore').encode("utf-8")
        page = page.replace('\r\n', '')
        page = page.replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&rsquo;', "'").replace('&#9642;','')
        page = page.replace('&bull;', '.').replace('&nbsp;', '').replace('&quot;', '"').replace('&aacute;', '')
        page = page.replace('&hellip;', '……').replace('&quot;', '"').replace('&#8217;', "'").replace('&lt;','')
        page = page.replace('&#34;', '"').replace('&#0148;', '"').replace('&#8216;', "'").replace('&#39;',"'")
        page = page.replace('&nbsp;', '').replace('&gt;', '').replace('&#0147;', '"').replace('&amp;','&')
        return page

    def getTitle(self, page):
        title = re.findall('<h1>.*?</h1>', page)
        if title != []:
            title = title[0]
            title = re.sub('\[.*?\]', '', title).replace('附文本','')
            title = re.sub('<.*?>', '', title)
        else:
            title = ''
            title_list = re.findall('<p class="ingress">.*?</p>', page)
            title_list = re.findall('<span>.*?</span>', title_list[0])
            for t in title_list:
                t = re.sub('<.*?>', '' , t)
                title = title + t
        # print title
        return title

    def getTime(self, type, page):
        if type == 'BBC News':
            title = self.getTitle(page)
            time = re.sub('BBC World News ', '', title)
        if type == 'Funny BBC':
            time = re.findall('<div class="from">.*?</div>', page)
            if time != []:
                time = re.sub('<span>.*?</span>', '', time[0])
                time = re.sub('<.*?>', '', time).replace('更新时间：', '')
            else:
                time = ''
        time = re.sub('[0-9]{2}:[0-9]{2}:[0-9]{2}', '', time) #去除时分钟
        time = re.sub('[0-9]{2}:[0-9]{2}', '', time)
        # print time
        return time

    def getTag(self):
        return '新闻'

    def getSource(self):
        source = '爱思英语网'
        # print source
        return source

    def getCategoryOne(self):
        category_one = 'News'
        # print category_one
        return category_one

    def getCategoryTwo(self, type):
        category_two = type
        # print category_two
        return category_two

    def getContent(self, type, page):
        content_zg = ''
        content_en = ''
        if type == 'BBC News':
            pattern_content = re.compile('<div class="cnt_article_body">.*?<!-- AD JS-->')
            content = re.findall(pattern_content, page)
            en_list = re.findall('<div id="con_four_1" >(.*?)</div></div>', content[0])
            en_list = re.sub('<a href="http://www.24en.com/".*?</a>', '', en_list[0])
            en_list = re.findall('<p>.*?</p>', en_list)
            for en in en_list:
                en = re.sub('<.*?>', '', en)
                content_en = content_en + en + '\n'
            # print content_en
            zg_list = re.findall('<div id="con_four_2" style="display:none">(.*?)</div></div>', content[0])[0]
            zg_list = zg_list.decode('utf-8')
            zg_list = re.findall(u'[\u4e00-\u9fa5].*?</p>', zg_list)
            for zg in zg_list:
                # print zg
                zg = re.sub('<.*?>', '', zg)
                zg = zg.encode('utf-8')
                content_zg = content_zg + zg + '\n'
            if content_zg == '抱歉，暂无中文翻译\n':
                content_zg = ''
            # print content_zg
        if type == 'Funny BBC':
            pattern_content = re.compile('<div class="bodytext">.*?<!--bodytext end-->', re.S)
            content = re.findall(pattern_content, page)
            for content in content:
                content = content.replace('</p>', '\n').replace('</font>', '\n')
                content = re.sub('<a href=http://dict.24en.com/w/.*?</a>','',content)
                content = re.sub('<a.*?</a>', '', content)
                content = re.sub('<h2.*?</h2>', '', content)
                content = re.sub('<li.*?</li>', '', content)
                # print content
                pattern_unuse = re.compile('<.*?>')
                content = re.sub(pattern_unuse, '', content)
                # print content
                content = content.replace('GLOSSARY', '\n').replace('(收听发音, 请单击英语单词)', '\n')
                content = content.replace('mp3">', '--').replace('Glossary', '\n').replace('            ','')
                content = content.replace('（点击单词收听发音）', '').replace('音频下载', '')
                content = content.replace('收听与下载 ','').replace('(点击收听发音)', '')
                content = content.replace('下载材料中不仅包括阅读, , 语法等练习, 还有单词搜索等游戏. '
                                          '帮助你英语读写能力, 了解相关的背景知识和语言环境','')
                content = content.replace('下载相关辅导材料(PDF格式)','')
                content_en = content.replace('   ', '').replace('\n 表', '')
                # print content_en
        if len(content_en) <= 200:
            content_en = ''
        dict = {'en': content_en, 'zg': content_zg}
        return dict

    def getPicture(self, page, id, type):
        save_path = ''
        if type == 'Funny BBC':
            picture = ''
            pattern = re.compile('http://www.24en.com/d/file/bbc/bbc2.*?jpg')
            pic = re.findall(pattern, page)
            if pic != []:
               picture = pic[0]
            else:
                pic = re.findall('/d/file/bbc/bbc2.*?jpg', page)
                if pic != []:
                    picture = 'http://www.24en.com' + pic[0]
            if picture != '':
                save_path = './picture/' + str(id) + '.jpg'
                urlretrieve(picture, save_path)
                save_path = '/picture/' + str(id) + '.jpg'
            # print picture
        return save_path

    def getAll(self, id, url, type, page):
        content_dict = self.getContent(type, page)
        if content_dict['en'] != '':
            title = self.getTitle(page)
            time = self.getTime(type, page)
            tag = self.getTag()
            source = self.getSource()
            category_one = self.getCategoryOne()
            category_two = self.getCategoryTwo(type)
            content_en = content_dict['en']
            content_zg = content_dict['zg']
            picture = self.getPicture(page, id, type)
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


# if __name__ == '__main__':
#     type_list = {'BBC News', 'Funny BBC'}
#     for type in type_list:
#         b = PatBBCNewsUrl()
#         b.getTotalUrl()
#         for url in b.getTotalUrl():
#             g = PatDetail()
#             print url
#             page = g.getPage()
#             # g.getTitle()
#             # g.getTime()
#             # g.getContent()
#             # g.getPicture()
#             g.getAll()