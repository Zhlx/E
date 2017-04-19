__author__ = 'carrie'
# coding=utf-8
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','E.settings')
import django
django.setup()
import re
import chardet
from urllib import urlopen, urlretrieve
from DataManager.models import Article

class PatXEUrl:

    def getHttp(self, cattwo):
        Http = []
        if cattwo == 'CET4':
            http = "http://www.en8848.com.cn/cet4/words/hmsy/index.html"
            Http.append(http)
        if cattwo == 'Anecdotes':
            for i in range(2, 12):
                http = 'http://www.en8848.com.cn/read/bi/oddnews/index_%s.html' % i
                # print http
                Http.append(http)
        return Http

    def getText(self, cattwo):
        total_url = self.getHttp(cattwo)
        Text = []
        for total_url in total_url:
            text = urlopen(total_url).read()
            text = str(text).replace('\n', '')
            # print text
            Text.append(text)
        return Text

    def getURL(self, cattwo):
        text_list = self.getText(cattwo)
        url_list = []
        for text in text_list:
            if cattwo == 'CET4':
                pattern = re.compile('http://www.en8848.com.cn/cet4/words/hmsy/.*?html')
            if cattwo == 'Anecdotes':
                pattern = re.compile('http://www.en8848.com.cn/read/bi/oddnews/.*?html')
            url_list = url_list + re.findall(pattern, text)
        return url_list

class PatXE:

    def getText(self, url):
        text = urlopen(url).read()
        text = str(text).replace('\r\n', '')  # one
        # text = text.replace('\r\n', '')   #two
        # 积累知识1 one 和 two 功能相同
        text = text.replace('&amp;', '&').replace('&rsquo;', "'").replace('&lsquo;', "'").replace('\\\'',"'")
        text = text.replace('&mdash;', '-').replace('&nbsp;', ' ').replace('&middot;', '·')
        text = text.replace('&ldquo;', '“').replace('&rdquo;', '”').replace('&ndash;', '-').replace('&rarr;', '→')
        text = text.replace('&hellip;', '……').replace('&quot;', '"').replace('&atilde;', 'ã').replace('&ccedil;','ç')
        # print text
        return text

    def getTitle(self, text):
        pattern = re.compile('<h1 id="toph1bt">.*?</h1>')
        title = re.search(pattern, text)
        if title.group() != '':
            title = re.sub('<.*?>', '', title.group()).replace('双语阅读：','').replace(' 英语世界奇闻','')
            title = title.replace('（双语阅读）','').replace('双语奇闻异事集锦,','').replace('奇闻：','')
            title = title.replace('奇闻异事：','').replace('双语：','').replace('双语奇闻：','')
            title = title.replace('双语奇观：','')
            return title
        else:
            return ''

    def getTime(self, text):
        pattern = re.compile('<div class="adwenzi">.*?</div>')
        time = re.findall(pattern, text)
        if time != []:
            # print time[0]
            time = re.sub('<.*?>', '', time[0])
            # print time
            time = re.findall('于(.*?)发布', time)
            # print time
            return time[0]
        else:
            return ''

    def getTag(self, cattwo):
        if cattwo == 'CET4':
            tag = '胡敏读双语故事背四级单词'
        if cattwo == 'Anecdotes':
            tag = '奇闻异事'
        return tag

    def getSource(self):
        source = '小e英语'
        # print source
        return source

    def getCategoryOne(self, catone):
        category_one = catone
        # print category_one
        return category_one

    def getCategoryTwo(self, cattwo):
        category_two = cattwo
        # print category_two
        return category_two

    def getContent(self, text, cattwo):
        pattern = re.compile('<div id="articlebody" class="jxa_content">.*?<div class="clr">', re.S)
        #积累知识2  re.compile有无re.S区别
        content = re.findall(pattern, text)
        # print content
        content_en = ''
        content_zg = ''
        if content != []:
            content = content[0]
            # print content
            if cattwo == 'CET4':
                content_list = re.split('<br />', content)
                for content in content_list:
                    if len(content) >= 215:
                        if content_en == '':
                            content_en = re.sub('<.*?>', '', content)
                            content_en = re.sub(' {3,}', '', content_en)
                        else:
                            if content_zg == '':
                                content_zg = re.sub('<.*?>', '', content)
                                content_zg = re.sub(' {3,}', '', content_zg)
            if cattwo == 'Anecdotes':
                if(re.findall('<a href="/read/bi/oddnews/.*?">3</a>',content)) == []:
                    content = re.sub('<div id="pageurl">.*?</div>', '', content)
                    content = content.replace('</p>', '###').replace('<br />','###')\
                        .replace('</P>', '###').replace('<br>', '###').replace('\n', '')
                    content = re.sub('<BR.*?>','###',content)
                    content = re.sub(' {3,}', '', content)
                    content = re.sub('<span.*?</span>', '', content)
                    content = re.sub('<.*?>', '', content)
                    content_list = re.split('###', content)
                    for content in content_list:
                        if content != '':
                            # print content
                            content = content.decode('utf-8')
                            zg = re.findall(u'[\u4e00-\u9fa5]', content)
                            if len(zg) < 5:
                                content_en = content_en + content + u'###'
                            else:
                                content_zg = content_zg + content + u'###'
                    if len(re.findall('[a-zA-Z]', content_en)) < 20:
                        content_zg = ''
                        for content in content_list:
                            content = content.decode('utf-8')
                            en_list = re.findall(u'([a-zA-Z"\'].*?)[\u4e00-\u9fa5]', content)
                            if en_list != []:
                                for en in en_list:
                                    if len(en) > 50:
                                        content_en = content_en + en + u'###'
                                        content = content.replace(en, '###')
                                content_zg = content
                    content_en = content_en.encode('utf-8')
                    content_en = re.sub("#{3,}", '\n', content_en)
                    content_en = content_en.replace('Vocabulary:', '')
                    content_zg = content_zg.encode('utf-8')
                    content_zg = re.sub("#{3,}", '\n', content_zg)
        # print content_en
        # print content_zg
        dict = {'en': content_en, 'zg': content_zg}
        return dict

    def getPicture(self, text, cattwo, id):
        save_path = ''
        if cattwo == 'Anecdotes':
            pic = re.findall('/d/file/20.*?jpg', text)
            if pic != [] :
                picture = 'http://www.en8848.com.cn' + pic[0]
                save_path = './picture/' + str(id) + '.jpg'
                urlretrieve(picture,save_path)
                save_path = '/picture/' + str(id) + '.jpg'
        return save_path

    def getAll(self, id, url, text, cattwo, catone):
        content_dict = self.getContent(text, cattwo)
        if content_dict['en'] != '':
            title = self.getTitle(text)
            time = self.getTime(text)
            tag = self.getTag(cattwo)
            source = self.getSource()
            category_one = self.getCategoryOne(catone)
            category_two = self.getCategoryTwo(cattwo)
            content_en = content_dict['en']
            content_zg = content_dict['zg']
            picture = self.getPicture(text, cattwo, id)
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


# if __name__ == "__main__":
    # catone_list = ['Study', 'Fun']
    # cattwo_list = ['CET4', 'Anecdotes']
    # for i in range(0, len(catone_list)):
    #     catone = catone_list[i]
    #     cattwo = cattwo_list[i]
    #     a = PatXEUrl()
    #     url_list = a.getURL()
    #     print len(url_list)
    #     for url in url_list:
    #         b = PatXE()
    #         print url
    #         text = b.getText()
    #         # print b.getTitle()
    #         # print b.getTime()
    #         # dict = b.getContent()
    #         # print b.getPicture()
    #         b.getAll()
