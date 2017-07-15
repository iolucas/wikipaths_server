from django.contrib import admin

# Register your models here.

from .models import WikiArticle, ArticleLink, WikiUrl, JsonCache

admin.site.register(WikiArticle)
admin.site.register(ArticleLink)
admin.site.register(WikiUrl)
admin.site.register(JsonCache)