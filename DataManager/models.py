from django.db import models

# Create your models here.

class Article(models.Model):
    articleId=models.CharField(max_length=15,primary_key=True)
    articleTitle=models.CharField(max_length=50)
    articleSource=models.CharField(max_length=50,default='')
    articleTag=models.CharField(max_length=50,blank=True)
    articleType1=models.CharField(max_length=20,blank=True)
    articleType2=models.CharField(max_length=20,blank=True)
    articleDate=models.CharField(max_length=20,blank=True)
    articleImgUrl=models.CharField(max_length=80)
    articleEnglishText=models.CharField(max_length=2000)
    articleChineseText=models.CharField(max_length=2000)


    def __unicode__(self):
        return self.articleId


class User(models.Model):
    userId=models.CharField(max_length=25,primary_key=True)
    userNickName=models.CharField(max_length=25,blank=True)
    password=models.CharField(max_length=20,default="")
    userFavorite=models.ManyToManyField(Article)

    def __unicode__(self):
        return self.user


class UserArticleBehavior(models.Model):
    user=models.ForeignKey(User)
    article=models.ForeignKey(Article)
    isCollected=models.BooleanField(default=False)
    isGood=models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.userId



