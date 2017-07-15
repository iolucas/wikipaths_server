from django.db import models

# Create your models here.

class JsonCache(models.Model):
    url = models.CharField(max_length=200, unique=True)
    json = models.TextField()

    def __str__(self):
        return self.url


class WikiArticle(models.Model):
    title = models.CharField(max_length=200, unique=True)
    pageid = models.IntegerField()
    links = models.ManyToManyField('ArticleLink')

    def __str__(self):
        return self.title

class ArticleLink(models.Model):
    link = models.ForeignKey("WikiUrl")
    score = models.FloatField()

    def __str__(self):
        return self.link.url

class WikiUrl(models.Model):
    url = models.CharField(max_length=200, unique=True)
    article = models.ForeignKey("WikiArticle", null=True)

    def __str__(self):
        return self.url

