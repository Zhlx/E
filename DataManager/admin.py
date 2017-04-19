from django.contrib import admin
from DataManager.models import Article,User,UserArticleBehavior
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('articleId','articleTitle','articleType1','articleDate')

class UserAdmin(admin.ModelAdmin):
    list_display = ('userId','userNickName')

class UserArticleBehaviorAdmin(admin.ModelAdmin):
    list_display = ('isCollected','isGood',)

admin.site.register(Article,ArticleAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(UserArticleBehavior,UserArticleBehaviorAdmin)