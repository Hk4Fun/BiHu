from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='名称')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=128, verbose_name='问题名')
    desc = models.TextField(max_length=256, verbose_name='问题描述')
    view_nums = models.IntegerField(default=0, verbose_name='浏览量')
    asker = models.ForeignKey(User, related_name='questions', verbose_name='提问者', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    concerned_users = models.ManyToManyField(User, related_name='concerned_questions',   verbose_name='关注者')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    def likes(self):
        # 问题的关注数
        return self.concerned_users.all().count() if self.id else 0

    likes.short_description = '关注数'

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return self.title


class Article(models.Model):
    content = models.TextField(verbose_name='内容')
    up_nums = models.IntegerField(default=0, verbose_name='点赞量')
    down_nums = models.IntegerField(default=0, verbose_name='踩量')
    question = models.ForeignKey(Question, related_name='articles', verbose_name='问题', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='articles', verbose_name='作者', on_delete=models.CASCADE)
    collected_users = models.ManyToManyField(User, verbose_name='被收藏者')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def likes(self):
        # 文章的收藏数
        return self.collected_users.all().count() if self.id else 0

    likes.short_description = '收藏数'

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    content = models.TextField(max_length=256, verbose_name='内容')
    up_nums = models.IntegerField(default=0, verbose_name='点赞量')
    down_nums = models.IntegerField(default=0, verbose_name='踩量')
    reviewer = models.ForeignKey(User, related_name='comments', verbose_name='评论者', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments', verbose_name='文章', on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='发表时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return self.reviewer.username
