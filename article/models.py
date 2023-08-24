from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from markdown import Markdown


# Create your models here.

class Tag(models.Model):
    text = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text


class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ['-created']

    def __str__(self):  # 定义了将模型显示为字符串时的内容。
        return self.title


class Article(models.Model):
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='articles'  # 用来给模型间的反向关系命名， 表示从 User 模型访问关联的 Article 对象时,可以通过 user.articles 来查询。
    )
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    updated = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )

    tag = models.ManyToManyField(
        Tag,
        null=True,
        blank=True,
        related_name='articles'
    )

    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ],
        )
        md_body = md.convert(self.body)
        return md_body, md.toc

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
